CREATE SCHEMA IF NOT EXISTS staging;

CREATE OR REPLACE VIEW staging.building_permits AS

SELECT
    source_record_id,
    permit_number,

    permit_type,
    review_type,
    work_type,
    work_description,

    application_start_date::TIMESTAMP AS application_start_at,
    issue_date::TIMESTAMP AS issue_at,
    processing_time::INTEGER AS processing_days,

    street_number,
    street_direction,
    street_name,

    community_area::INTEGER AS community_area,
    census_tract,
    ward::INTEGER AS ward,

    latitude::DOUBLE PRECISION AS latitude,
    longitude::DOUBLE PRECISION AS longitude,

    reported_cost::NUMERIC(18, 2) AS reported_cost,
    total_fee::NUMERIC(18, 2) AS total_fee,

    contact_1_type,
    contact_1_name,
    contact_2_type,
    contact_2_name,

    _ingested_at,
    _source

FROM raw.building_permits;