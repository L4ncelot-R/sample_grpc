import pickle
import grpc
import test_pb2 as pb2
import test_pb2_grpc as pb2_grpc
import hashlib


def run_client():
    # Connect to the gRPC server running on localhost:50051
    with grpc.insecure_channel('192.168.31.163:50051') as channel:
        # Create a stub (client) for the Service_t service
        stub = pb2_grpc.Service_tStub(channel)

        # Create a Message_t instance with your desired information
        message = pb2.message(from_ip='192.168.31.163',
                              from_port='50051',
                              to_ip='192.168.31.163',
                              to_port='50053',
                              message='Hello from client')
        message.hash = hashlib.sha256(pickle.dumps(message)).digest()
        # Call the Communicate method of the Service_t service
        response = stub.Send(message)
        print(response)


if __name__ == '__main__':
    run_client()
