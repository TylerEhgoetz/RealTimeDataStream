import grpc
import streaming_pb2, streaming_pb2_grpc


def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = streaming_pb2_grpc.TickServiceStub(channel)
    for tick in stub.StreamTicks(streaming_pb2.Empty()):
        print(f"Tick: {tick.symbol} {tick.price} | MA: {tick.indicator}")


if __name__ == "__main__":
    run()
