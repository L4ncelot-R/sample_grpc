import grpc
from concurrent import futures
import test_pb2 as pb2
import test_pb2_grpc as pb2_grpc


def get_message(topic, question, answers):
    return pb2.message(topic=topic, message={question: pb2.answers(answer=answers)})


class Server:
    def __init__(self, ip=None, port=None):
        self.ip = ip
        self.port = port
        self.address_book = {}
        self.data = {}

    def Subscribe(self, request, context):
        self.update_address_book(request)
        return pb2.Received_t(success=True)

    def Unsubscribe(self, request, context):
        self.unsubscribe(request)
        return pb2.Received_t(success=True)

    # when received a published message
    def Publish(self, request, context):
        self.publish(request)
        return pb2.Received_t(success=True)

    def update_address_book(self, request):
        if request.topic not in self.address_book.keys():
            self.address_book[request.topic] = []

        if (request.ip, request.port) not in self.address_book[request.topic]:
            self.address_book[request.topic].append((request.ip, request.port))
            print(f"address book updated: {self.address_book}")

    def unsubscribe(self, request):
        if request.topic not in self.address_book.keys():
            return

        if (request.ip, request.port) in self.address_book[request.topic]:
            self.address_book[request.topic].remove((request.ip, request.port))
            print(f"address book updated: {self.address_book}")

    def publish(self, request):
        received_dict = {}
        for key, value in request.message.items():
            received_dict[key] = [ans for ans in value.answer]

        if self.update_database(request.topic, received_dict):
            print(f"data updated: {self.data}")
            self.broadcast(request)

    def update_database(self, topic, received_dict):
        is_updated = False
        if topic not in self.data.keys():
            self.data[topic] = received_dict
            return True

        for key, value in received_dict.items():
            if key not in self.data[topic].keys():
                self.data[topic][key] = value
            else:
                for ans in value:
                    if ans not in self.data[topic][key]:
                        self.data[topic][key].append(ans)
                        is_updated = True

        if is_updated:
            print(f"data updated: {self.data}")
            return True
        else:
            return False

    def broadcast(self, request):
        if request.topic not in self.address_book.keys():
            return
        for ip, port in self.address_book[request.topic]:
            with grpc.insecure_channel(f'{ip}:{port}') as channel:
                stub = pb2_grpc.Service_tStub(channel)
                stub.Publish(request)
                print(f"published to {ip}:{port}")

    def send_subscribe(self, subscription, ip, port):
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = pb2_grpc.Service_tStub(channel)
            stub.Subscribe(subscription)
            print(f"subscribed to {ip}:{port}")

    def send_unsubscribe(self, subscription, ip, port):
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = pb2_grpc.Service_tStub(channel)
            stub.Unsubscribe(subscription)
            print(f"unsubscribed to {ip}:{port}")

    def run(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        pb2_grpc.add_Service_tServicer_to_server(self, server)
        server.add_insecure_port(f"{self.ip}:{self.port}")
        server.start()
        print(f"Server started at {self.ip}:{self.port}")
        server.wait_for_termination()

    def get_subscription(self, topic):
        return pb2.subscription(topic=topic, ip=self.ip, port=self.port)