CREATE STREAM accounting_bal_sheet_input (`key` VARCHAR KEY)
WITH (
    KAFKA_TOPIC='private_accounting_bal_sheet_cdc',
    VALUE_FORMAT='avro'
);