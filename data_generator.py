import time, random, json
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode(),
)

symbols = ["AAPL", "GOOG", "MSFT", "AMZN", "TSLA"]

while True:
    tick = {
        "symbol": random.choice(symbols),
        "price": round(random.uniform(100, 500), 2),
        "timestamp": int(time.time() * 1000),
    }
    producer.send("raw_prices", value=tick)
    print(f"Produced tick: {tick}")
    time.sleep(1)
