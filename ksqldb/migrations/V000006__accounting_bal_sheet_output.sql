/*
This creates a new stream by selecting from the input stream,
projecting fields to the canonical schema defined in the schema registry,
and producing new messages into the public topic for other services
to consume.
The schema created in the projection must be compatible with the
canonical schema for balance sheet events.
*/

CREATE STREAM accounting_bal_sheet_output
WITH (
    KAFKA_TOPIC = 'public_balance_sheet_entity_events',
    VALUE_FORMAT = 'avro'
) AS
    SELECT
        '1.0' AS `specversion`,
        UUID() as `id`,
        'balance_sheet_calculated' as `type`,
        'accounting-service' as `source`,
        `key` as `subject`,
        DATE_CALCULATED as `time`,
        STRUCT(
            `id` := ID,
            `person_id` := PERSON_ID,
            `date_calculated` := DATE_CALCULATED,
            `assets` := ASSETS,
            `liabilities` := LIABILITIES
        ) AS `data`
    FROM
        accounting_bal_sheet_input
    EMIT CHANGES;
