# RealTimeDataStream
A basic Real-Time Data Streaming pipeline that simulates real-time stock ticks. Uses Kafka for streaming and gRPC for downstream communication.

A Data generator will simulate real-time stock ticks, produces to Kafka topic raw_prices
Kafka consumer reads raw_prices and computes an indicator then publishes to indicators topic.
Exposes a gRPC service to downstream clients to subscribe to indicators.

Start the pipeline:
docker-compose up -d

Stop the pipeline:
docker-compose down

Run the data generator:
python data_generator.py

Run the processor:
python processor.py

Run the consumer:
python consumer.py
