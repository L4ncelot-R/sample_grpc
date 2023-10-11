import grpc
from concurrent import futures
import test_pb2 as pb2
import test_pb2_grpc as pb2_grpc

address = ("192.168.31.163", "50053")

# use TTL instead?
address_book = {
    "Topic A": [
        ("192.168.31.163", "50052"),
        ("192.168.31.163", "50051")
    ]
}

data = {
    "Topic A":
        {
            "What is the answer to this question?": ["A", "B", "C", "D"]
        }
}


class MyService(pb2_grpc.Service_tServicer):
    def Subscribe(self, request, context):
        update_address_book(request)
        return pb2.Received_t(success=True)

    def Unsubscribe(self, request, context):
        unsubscribe(request)
        return pb2.Received_t(success=True)

    # when received a published message
    def Publish(self, request, context):
        publish(request)
        return pb2.Received_t(success=True)


def update_address_book(request):
    if request.topic not in address_book.keys():
        address_book[request.topic] = []

    if (request.from_ip, request.from_port) not in address_book[request.topic]:
        address_book[request.topic].append((request.from_ip, request.from_port))


def unsubscribe(request):
    if request.topic not in address_book.keys():
        return

    if (request.from_ip, request.from_port) in address_book[request.topic]:
        address_book[request.topic].remove((request.from_ip, request.from_port))


def publish(request):
    received_dict = {}
    for key, value in request.message.items():
        received_dict[key] = [ans for ans in value.answer]

    if update_database(request.topic, received_dict):
        print(f"data updated: {data}")
        broadcast(request)


# TODO: change to use real database
def update_database(topic, received_dict):
    is_updated = False
    if topic not in data.keys():
        data[topic] = received_dict
        return True

    for key, value in received_dict.items():
        if key not in data[topic].keys():
            data[topic][key] = value
        else:
            for ans in value:
                if ans not in data[topic][key]:
                    data[topic][key].append(ans)
                    is_updated = True

    if is_updated:
        return True
    else:
        return False


def run_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_Service_tServicer_to_server(MyService(), server)
    server.add_insecure_port(f'{address[0]}:{address[1]}')
    server.start()
    print(f"Server started. Listening on port {address[1]}.")
    server.wait_for_termination()


def broadcast(message):
    if message.topic not in address_book.keys():
        return

    for ip, port in address_book[message.topic]:
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = pb2_grpc.Service_tStub(channel)
            try:
                stub.Publish(message)
            except grpc.RpcError as e:
                print(f"Error: {e}")


if __name__ == '__main__':
    run_server()
