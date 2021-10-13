
# Kafka and IBM i

## Streaming data to Kafka from IBM i
There are several approaches to streaming data from Db2 transactions to Kafka, including but not limited to:
1. [Db2 triggers and Apache Camel](KAFKA_CAMEL_DTAQ.md): stream events in real-time
1. [Kafka Connect JDBC Source connector](KAFKA_CONNECT_JDBC.md): Simple, polling-based technique for importing Db2 data into Kafka
1. [InfoSphere Data Replication and the CDC Replication Engine for Kafka](https://www.ibm.com/docs/en/idr/11.4.0?topic=replication-cdc-engine-kafka) (external link): a CDC-based approach that may be a good options for current IBM CDC customers
1. [Native ILE Kafka client (unsupported)](https://github.com/AlexeiBaranov/librdkafka/blob/port-os400/packaging/os400/README.md) (external link): call Kafka functions directly from ILE programs.
