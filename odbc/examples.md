# Node.js Example

```{toctree}
:maxdepth: 1
```

This quick example will demonstrate development on a non-IBM i machine against
Db2 on i, and then how you would transfer that same code to run on IBM i when
you are ready to run in production.

For this example, we will be using Node.js and the `odbc` package available on
NPM. Node.js is simply used as an example technology, and this same thing could
be done with PHP, Python, R, or any other package that has the ability to
connect to the ODBC driver manager.

## Setting Up Your Development Environment

### DSNs

The following instructions assume you have set up your ODBC environment [as
outlined in the sections above](#installation). On your development machine,
define a private DSN similar to the following, adding in your system and user credentials:

```ini
[MYDSN]
Description            = The IBM i System
Driver                 = IBM i Access ODBC Driver
System                 = PUT.YOUR.SYSTEM.HERE
UserID                 = USERNAME
Password               = PASSWORD
```

### Node.js

To run through this example, you will need to have Node.js installed. You can
find the downloads at the [official Node.js website](https://nodejs.org/en/download/)
or through your system's package manager.

When you have Node.js installed, navigate to a new folder to contain your
project and run:

```bash
npm init -y
```

This will create a file for you called `package.json`, which tracks software you
download from npm (among other things).

Next, install the `odbc` package, which allows Node.js to talk to your driver manager.

```bash
npm install odbc
```

You now have everything you need to connect to Db2 for i from your development machine!

## Development

Using the `odbc` package, you can use a connection string that only references
the DSN you defined above. Once you have the connection created, all of your
queries will be run against the IBM i system defined in the DSN.

**`app.js`**

```javascript
const odbc = require('odbc');

odbc.connect('DSN=MYDSN', (error, connection) => {
  if (error) { throw error; }
  // now have an open connection to IBM i from any Linux or Windows machine
  connection.query('SELECT * FROM QIWS.QCUSTCDT', (error, result) => {
    if (error) { throw error; }
    console.log(result);
  })
});
```

## Transfer to IBM i

When you are ready to transfer your program to IBM i, you just need to make sure
you have everything set up on that system.

### DSNs on IBM i

Like on your development machine, you will have to install your driver manager
and driver. Steps to do that can be found in [installation on IBM i](#installation-on-ibm-i)
section. That section will also cover instructions for downloading the Db2 for i
driver and how to configure your DSNs, though this example will use the default
`*LOCAL` DSN.

### Node.js on IBM i

Because we want to transfer our Node.js application to our IBM i system, we will
have to have Node.js installed:

```bash
yum install nodejs10
```

You will then have Node.js v10 on your system. You simply need to move your code
over to your IBM i system. Because we want to connect to the local database, we
change our DSN to be `*LOCAL` instead of `MYDSN`:

**`app.js`**

```javascript
const odbc = require('odbc');

odbc.connect('DSN=*LOCAL', (error, connection) => {
  if (error) { throw error; }
  // now have an open connection to IBM i from any Linux or Windows machine
  connection.query('SELECT * FROM QIWS.QCUSTCDT', (error, result) => {
    if (error) { throw error; }
    console.log(result);
  })
});
```
