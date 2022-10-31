/*
This creates a stream upon the balance sheet CDC topic,
so that it can be queried to produce to translate to a new schema and topic.
Note that the schema of this stream is inferred from the source topic, although
the `key` column as added to preserve the KEY of the source messages.
*/

CREATE STREAM accounting_bal_sheet_input (`key` VARCHAR KEY)
WITH (
    KAFKA_TOPIC='private_accounting_bal_sheet_cdc',
    VALUE_FORMAT='avro'
);