import grpc
from concurrent import futures
import test_pb2 as pb2
import test_pb2_grpc as pb2_grpc

address_book = [
    ("127.0.0.1", "50051"),  # first element is the ip address of the server
    ("127.0.0.1", "50052"),
]


class MyService(pb2_grpc.Service_tServicer):
    def Communicate(self, request, context):
        peer_info = context.peer()
        forward_message(request.ip, request.port, request.message, peer_info)
        return pb2.Received_t(success=True)

def run_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_Service_tServicer_to_server(MyService(), server)
    server.add_insecure_port(f'{address_book[0][0]}:{address_book[0][1]}')  # Change the port as needed
    server.start()
    print(f"Server started. Listening on port {address_book[0][1]}.")
    server.wait_for_termination()


def forward_message(ip, port, message, peer_info):
    if ip == address_book[0][0] and port == address_book[0][1]:
        from_ip, from_port = peer_info.split(':')[1], peer_info.split(':')[2]
        print(f"Message received from {from_ip}:{from_port}: {message}")
    else:
        for address in address_book[1:]:
            with grpc.insecure_channel(f"{address[0]}:{address[1]}") as channel:
                stub = pb2_grpc.Service_tStub(channel)
                stub.Communicate(pb2.Message_t(ip=ip, port=port, message=message))
                print(f"Message forwarded to {address[0]}:{address[1]}")


if __name__ == '__main__':
    run_server()
