CREATE SOURCE CONNECTOR person_outbox_source WITH (
    'connector.class' = 'io.debezium.connector.postgresql.PostgresConnector', 
    'plugin.name' = 'pgoutput',
    'database.hostname' = 'postgres', 
    'database.port' = '5432', 
    'database.user' = 'postgres', 
    'database.password' = '', 
    'database.dbname' = 'person', 
    'database.server.name' = 'person-service',
    'table.include.list' = 'public.events_event',
    'table.field.event.time-stamp' = 'timestamp',
    'transforms' = 'outbox',
    'transforms.outbox.type' = 'io.debezium.transforms.outbox.EventRouter',
    'value.converter' = 'io.debezium.converters.ByteBufferConverter'
);