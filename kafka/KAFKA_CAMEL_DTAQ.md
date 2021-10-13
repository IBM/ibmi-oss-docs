
# Using Db2 Triggers and Apache Camel to stream Db2 events to Kafka

## How it works

## How to implement
IBM and Perforce ran a workshop for the FOCUS2020 event, the source code and steps for which can be found [here](https://github.com/ThePrez/FOCUS2020-Workshop/).
You can follow those workshop steps on your own development system and examine the code for a more thorough understanding. The general steps are outlined here

### Step 1: Create a data queue
For instance
```fortran
CRTDTAQ DTAQ(MYLIB/MYDQ) MAXLEN(64000) SENDERID(*YES) SIZE(*MAX2GB) TEXT('row level changes for MYLIB/MYTABLE')
```
### Step 2: Create a Db2 trigger
An example can be found in the above workshop, or [here](https://github.com/IBM/ibmi-oss-examples/blob/master/camel/dtaq_to_kafka/banking_kafka_example.sql). 
The key points are that the transaction is converted to JSON and sent to the data queue via `qsys2.send_data_queue_utf8()`

### Step 3: Create a Camel route
Information about writing and deploying a Camel route can be found in the above workshop, or [here](https://github.com/IBM/ibmi-oss-examples/tree/master/camel).
A simple route to stream information from the data queue to Kafka looks like this:
```java
from(dtaqUri)
.convertBodyTo(String.class, "UTF-8") // We do this to convert the bytes from the data queue (UTF-8 JSON data) into a String object in the message
.to(kafkaUri); 
```
