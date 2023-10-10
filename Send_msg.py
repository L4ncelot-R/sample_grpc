import grpc
import test_pb2 as pb2
import test_pb2_grpc as pb2_grpc

def run_client():
    # Connect to the gRPC server running on localhost:50051
    with grpc.insecure_channel('127.0.0.1:50051') as channel:

        # Create a stub (client) for the Service_t service
        stub = pb2_grpc.Service_tStub(channel)

        # Create a Message_t instance with your desired information
        message = pb2.Message_t(ip='127.0.0.1', port='50052', message='Hello from client')

        # Call the Communicate method of the Service_t service
        stub.Communicate(message)


if __name__ == '__main__':
    run_client()
