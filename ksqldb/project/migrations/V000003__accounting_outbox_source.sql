/*
Accounting service outbox connector.
*/


CREATE SOURCE CONNECTOR accounting_outbox_source WITH (
    'connector.class' = 'io.debezium.connector.postgresql.PostgresConnector', 
    'plugin.name' = 'pgoutput',
    'database.hostname' = 'postgres', 
    'database.port' = '5432', 
    'database.user' = 'postgres', 
    'database.password' = '', 
    'database.dbname' = 'accounting', 
    'database.server.name' = 'accounting-service',
    'slot.name' = 'accounting_service_debezium',
    'table.include.list' = 'public.events_outboxitem',
    'transforms' = 'outbox',
    'transforms.outbox.type' = 'io.debezium.transforms.outbox.EventRouter',
    'transforms.outbox.table.field.event.key' = 'message_key',
    'transforms.outbox.route.by.field' = 'topic',
    'transforms.outbox.route.topic.replacement' = '${routedByValue}',
    'transforms.outbox.table.fields.additional.placement' = 'id:header:ce_id,timestamp:header:ce_time,event_type:header:ce_type,source:header:ce_source,content_type:header:content-type',
    'value.converter' = 'io.debezium.converters.ByteBufferConverter'
);