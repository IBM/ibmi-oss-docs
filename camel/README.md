# Apache Camel

```{toctree}
:maxdepth: 1
```

[Apache Camel](https://camel.apache.org) is a powerful Java-based integration framework that can be used to
integrate countless technologies, including IBM i. For a brief introduction, see this article: 
[Integrate IBM i With Anything Using Apache Camel](https://techchannel.com/SMB/8/2021/ibm-i-apache-camel).

**Examples**
Examples of using Apache Camel on IBM i can be found in the IBM i OSS examples repository, in [the 'camel' directory](https://github.com/IBM/ibmi-oss-examples/tree/master/camel).

## Using the Camel JT400 Component
The [JT400 Component](https://camel.apache.org/components/next/jt400-component.html) can be used to integrate
with IBM i in several ways, including:
- Message queues
- Data queues
- Program call

## Other Components
Most other Apache Camel [components](https://camel.apache.org/components/next/index.html) are platform-agnostic
and can be used from IBM i or to directly interact with IBM i. Some of the components most commonly used explicitly
for IBM i integration include, but are not limited to:
- [JDBC](https://camel.apache.org/components/next/jdbc-component.html)/[SQL](https://camel.apache.org/components/next/sql-component.html)
- [Paho (mqtt/IoT)](https://camel.apache.org/components/next/paho-component.html)
- [Exec (execute a command)](https://camel.apache.org/components/next/exec-component.html)
- [File](https://camel.apache.org/components/next/file-component.html)
- [FTP](https://camel.apache.org/components/next/ftp-component.html)/[sFTP](https://camel.apache.org/components/next/sftp-component.html)
- [HTTP](https://camel.apache.org/components/next/http-component.html)
- [SSH](https://camel.apache.org/components/next/ssh-component.html)
