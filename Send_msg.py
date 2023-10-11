import grpc
import test_pb2 as pb2
import test_pb2_grpc as pb2_grpc


def run_client():
    # Connect to the gRPC server running on localhost:50051
    with grpc.insecure_channel('192.168.31.163:50051') as channel:
        # Create a stub (client) for the Service_t service
        stub = pb2_grpc.Service_tStub(channel)

        # Create a Message_t instance with your desired information
        ans = pb2.answers(answer=("I dont know", "I dont care"))
        publish_item = pb2.message(topic="Topic A", message={"What is the answer to this question?": ans})
        response = stub.Publish(publish_item)
        print(response)


if __name__ == '__main__':
    run_client()
