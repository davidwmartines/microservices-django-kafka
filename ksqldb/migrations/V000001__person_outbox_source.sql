CREATE SOURCE CONNECTOR person_outbox_source WITH (
    'connector.class' = 'io.debezium.connector.postgresql.PostgresConnector', 
    'plugin.name' = 'pgoutput',
    'database.hostname' = 'postgres', 
    'database.port' = '5432', 
    'database.user' = 'postgres', 
    'database.password' = '', 
    'database.dbname' = 'person', 
    'database.server.name' = 'person-service',
    'table.include.list' = 'public.events_outboxitem',
    'table.field.event.timestamp' = 'timestamp',
    'transforms' = 'outbox',
    'transforms.outbox.type' = 'io.debezium.transforms.outbox.EventRouter',
    'transforms.outbox.table.fields.additional.placement' = 'id:header:ce_id,timestamp:header:ce_time,event_type:header:ce_type,source:header:ce_source,content_type:header:content-type',
    'value.converter' = 'io.debezium.converters.ByteBufferConverter'
);