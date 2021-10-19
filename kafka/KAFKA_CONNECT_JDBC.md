# Using the JDBC Source/Sink Connectors and Kafka Connect

Download the JDBC Connector (Source and Sink) from Confluent Hub [confluentinc-kafka-connect-jdbc-10.2.0.zip]. Source connectors are used to read data from a database. Sink connectors are used to insert data into a database.

Steps for installing the plugin came from https://docs.confluent.io/home/connect/userguide.html#connect-installing-plugins

To install the JDBC Connector:
1. Create a plugins directory (`mkdir -p kafka/plugins`)
1. Set the `plugin.path` property in the `config/connect-standalone.properties` file in your Kafka Connect installation (for instance, `plugin.path=/home/MYUSR/kafka/plugins`)
1. Extract the plugin archive in the plugins directory (for instance, `unzip confluentinc-kafka-connect-jdbc-10.2.0.zip` in the `kafka/plugins` directory)

Steps for installing the JDBC drivers for use with the connector can be found at https://docs.confluent.io/current/connect/kafka-connect-jdbc/index.html#installing-jdbc-drivers

**Important note: The jar files for the JDBC driver needs to be in the same directory as the jar file for the connector (for instance, `kafka/plugins/confluentinc-kafka-connect-jdbc-10.2.0/lib`). You can download the IBM Toolbox JDBC driver from [the JTOpen web site](http://jt400.sourceforge.net/) or copy it from `/QIBM/ProdData/OS400/jt400/lib/java8/jt400.jar`. Alternatively, you can use the IBM Db2 JDBC driver from DB2 Connect (you need both db2jcc4.jar and db2jcc_license_cisuz.jar).**

A worker configuration for each JDBC connector needs to be created. These can be different for the Toolbox JDBC driver and the IBM DB2 JDBC driver.

Here is an example using the Toolbox JDBC driver, limiting the connector to reading data from KC_JTOPEN.EMPLOYEE:

file: `config/worker-jtopen.properties`

contents:
```
name=jdbc_source_jtopen_01
connector.class=io.confluent.connect.jdbc.JdbcSourceConnector
connection.url=jdbc:as400://mysystem.mycompany.com
connection.user=MYUSR
connection.password=<password>
topic.prefix=jtopen-01-
mode=bulk
poll.interval.ms=3600000
schema.pattern=KC_JTOPEN
table.whitelist=EMPLOYEE
```
And here is an example using the IBM DB2 JDBC driver, limiting the connector to reading data from KC_DB2.EMPLOYEE:

file: `config/worker-db2.properties`

contents:
```
name=jdbc_source_db2_01
connector.class=io.confluent.connect.jdbc.JdbcSourceConnector
connection.url=jdbc:ibmdb://mysystem.mycompany.com:446/*LOCAL
connection.user=MYUSR
connection.password=<password>
topic.prefix=db2-01-
mode=bulk
poll.interval.ms=3600000
schema.pattern=KC_DB2
table.whitelist=EMPLOYEE
```

Assuming zookeeper and the Kafka server are already running, start connect using the worker configurations:
```
bin/connect-standalone.sh config/connect-standalone.properties config/worker-jtopen.properties config/worker-db2.properties
```

Assuming you are running Kafka on localhost, you can list the connectors using the following:
```
curl -s "http://localhost:8083/connectors"
```

You can list the status of a connector using something like the following: 
```
curl -s "http://localhost:8083/connectors/jdbc_source_jtopen_01/status" | jq '.'
curl -s "http://localhost:8083/connectors/jdbc_source_db2_01/status" | jq '.'
```
