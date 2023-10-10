import hashlib
import pickle
import time
import grpc
from concurrent import futures
import test_pb2 as pb2
import test_pb2_grpc as pb2_grpc
import threading

address_book = [
    ("192.168.31.163", "50053"),  # first element is the ip address of the server
    ("192.168.31.163", "50052"),
    ("192.168.31.163", "50051"),
]

timeout_cache = {}

cache_lock = threading.Lock()


class MyService(pb2_grpc.Service_tServicer):
    def Send(self, request, context):
        forward_message(request)
        return pb2.Received_t(success=True)


def run_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_Service_tServicer_to_server(MyService(), server)
    server.add_insecure_port(f'{address_book[0][0]}:{address_book[0][1]}')  # Change the port as needed
    server.start()
    print(f"Server started. Listening on port {address_book[0][1]}.")
    server.wait_for_termination()


def forward_message(request):
    if not update_timeout(request.hash):
        return

    if request.to_ip == address_book[0][0] and request.to_port == address_book[0][1]:
        request = response_message(request)

    broadcast(request)


def response_message(request):
    print(f"Message received from {request.from_ip}:{request.from_port}: {request.message}")
    message = pb2.message(from_ip=request.to_ip,
                          from_port=request.to_port,
                          to_ip=request.from_ip,
                          to_port=request.from_port,
                          message="Hello from server reply")
    message.hash = hashlib.sha256(pickle.dumps(message)).digest()
    return message


def update_timeout(hash_val):
    with cache_lock:
        if hash_val in timeout_cache.keys():
            return False
        else:
            timeout_cache[hash_val] = int(time.mktime(time.gmtime())) + 300
            return True


def clear_timeout():
    while True:
        items_to_remove = []
        with cache_lock:
            for hash_val, timestamp in timeout_cache.items():
                if timestamp < int(time.mktime(time.gmtime())):
                    items_to_remove.append(hash_val)

        with cache_lock:
            for item in items_to_remove:
                timeout_cache.pop(item)
                print(f"removed {item[0]} from cache")

        time.sleep(10)


def broadcast(message):
    for address in address_book[1:]:
        with grpc.insecure_channel(f"{address[0]}:{address[1]}") as channel:
            stub = pb2_grpc.Service_tStub(channel)
            stub.Send(message)
            print(f"Message broadcast to {address[0]}:{address[1]}")



if __name__ == '__main__':
    server_thread = threading.Thread(target=run_server)
    cache_thread = threading.Thread(target=clear_timeout)

    server_thread.start()
    cache_thread.start()

    server_thread.join()
    cache_thread.join()
