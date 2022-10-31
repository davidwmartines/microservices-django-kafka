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
