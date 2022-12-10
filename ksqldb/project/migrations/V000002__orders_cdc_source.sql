/*
This creates a source connector for producing change-data-capture events
from the Orders table in the orders service.
Note that the schema of the events is exactly based on the source-table
schema.  For that reason, these events are produced to a private topic
owned by the service.  For public use of these events, stream processing
will translate the events to the canonical schema and produce new messages
to a public topic.
*/

CREATE SOURCE CONNECTOR order_source WITH (
    'connector.class' = 'io.debezium.connector.postgresql.PostgresConnector', 
    'plugin.name' = 'pgoutput',
    'database.hostname' = 'postgres', 
    'database.port' = '5432', 
    'database.user' = 'postgres', 
    'database.password' = '', 
    'database.dbname' = 'orders', 
    'database.server.name' = 'orders-service',
    'slot.name' = 'orders_service_bal_sheet_cdc_debezium',
    'table.include.list' = 'public.orders_order',
    'value.converter'='io.confluent.connect.avro.AvroConverter',
    'value.converter.schema.registry.url' = '${env:KSQL_KSQL_SCHEMA_REGISTRY_URL}',
    'transforms' = 'reroute,extractKey,unwrap',
    'transforms.reroute.type' = 'io.debezium.transforms.ByLogicalTableRouter',
    'transforms.reroute.topic.regex' = '(.*)',
    'transforms.reroute.topic.replacement' = 'private_orders_order_cdc',
    'transforms.extractKey.type' = 'org.apache.kafka.connect.transforms.ExtractField$Key',
    'transforms.extractKey.field' = 'id',
    'transforms.unwrap.type' = 'io.debezium.transforms.ExtractNewRecordState'
);