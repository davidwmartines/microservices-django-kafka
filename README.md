# Django / Kafka  - Microservices

Demo of microservice architecture using Django and Kafka.




## Run

This project uses [just](https://github.com/casey/just) commands.


To get the demo working, run the following commands:

### Start up the stack:

```sh
just up
```

### Initialize the services:
```sh
just init-services
```

### Initialize ksqldb:
```sh
just init-ksqldb
```

#### Notes for Linux

The sh scripts may require exec permissions:
```sh
chmod +x wait-for-it.sh 
```

You may need to run the just commands with `sudo`  in order to run docker commands, e.g.:
```sh
sudo just up
```