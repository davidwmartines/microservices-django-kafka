FROM confluentinc/ksqldb-server:0.28.2 AS base


FROM base AS plugins

# set up plugins dir
USER root
RUN mkdir -p /usr/share/kafka/plugins
RUN chown appuser /usr/share/kafka/plugins
USER appuser

# plugin: jdbc connector
RUN bin/confluent-hub install --no-prompt \
    --component-dir /usr/share/kafka/plugins \
    --worker-configs /etc/ksqldb/connect.properties -- \
    confluentinc/kafka-connect-jdbc:10.6.0

# plugin: debezium postgresql source connector
RUN bin/confluent-hub install --no-prompt \
    --component-dir /usr/share/kafka/plugins \
    --worker-configs /etc/ksqldb/connect.properties -- \
    debezium/debezium-connector-postgresql:1.9.6

# plugin: common SMTs
RUN bin/confluent-hub install --no-prompt \
    --component-dir /usr/share/kafka/plugins \
    --worker-configs /etc/ksqldb/connect.properties -- \
    jcustenborder/kafka-connect-transform-common:0.1.0.54

# plugin: EnvVarConfigProvider
RUN wget -c https://github.com/strimzi/kafka-env-var-config-provider/releases/download/1.0.0/kafka-env-var-config-provider-1.0.0.tar.gz -O - \
    | tar -xz -C /usr/share/kafka/plugins/
