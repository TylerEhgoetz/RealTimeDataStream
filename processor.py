from concurrent import futures
import threading, time, json

from collections import deque
from kafka import KafkaConsumer, KafkaProducer
import grpc
import streaming_pb2, streaming_pb2_grpc

buffers = {}  # holds last N prices per symbol


class TickServicer(streaming_pb2_grpc.TickServiceServicer):
    def StreamTicks(self, request, context):
        while True:
            if not output_queue:
                time.sleep(1)
                continue
            yield output_queue.popleft()


def start_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    streaming_pb2_grpc.add_TickServiceServicer_to_server(TickServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


from collections import deque

output_queue = deque(maxlen=1000)


def process_stream():
    consumer = KafkaConsumer(
        "raw_prices",
        bootstrap_servers="localhost:9092",
        value_deserializer=lambda x: json.loads(x.decode()),
    )
    producer = KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda x: json.dumps(x).encode(),
    )

    for msg in consumer:
        tick = msg.value
        symbol = tick["symbol"]
        timestamp = tick["timestamp"]
        price = tick["price"]
        buf = buffers.setdefault(symbol, deque(maxlen=10))
        buf.append(price)
        ma = sum(buf) / len(buf)
        enriched = {**tick, "indicator": ma}
        producer.send("indicators", value=enriched)
        grpc_tick = streaming_pb2.Tick(
            symbol=symbol, price=price, timestamp=timestamp, indicator=ma
        )
        output_queue.append(grpc_tick)


if __name__ == "__main__":
    threading.Thread(target=start_grpc_server, daemon=True).start()
    process_stream()
