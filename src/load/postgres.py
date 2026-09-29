from src.db.connection import get_connection


UPSERT_PERMIT_SQL = """
INSERT INTO raw.building_permits (
    source_record_id,
    permit_number,
    permit_type,
    review_type,
    work_type,
    work_description,
    application_start_date,
    issue_date,
    processing_time,
    street_number,
    street_direction,
    street_name,
    community_area,
    census_tract,
    ward,
    latitude,
    longitude,
    reported_cost,
    total_fee,
    contact_1_type,
    contact_1_name,
    contact_2_type,
    contact_2_name,
    _ingested_at,
    _source
)
VALUES (
    %(source_record_id)s,
    %(permit_number)s,
    %(permit_type)s,
    %(review_type)s,
    %(work_type)s,
    %(work_description)s,
    %(application_start_date)s,
    %(issue_date)s,
    %(processing_time)s,
    %(street_number)s,
    %(street_direction)s,
    %(street_name)s,
    %(community_area)s,
    %(census_tract)s,
    %(ward)s,
    %(latitude)s,
    %(longitude)s,
    %(reported_cost)s,
    %(total_fee)s,
    %(contact_1_type)s,
    %(contact_1_name)s,
    %(contact_2_type)s,
    %(contact_2_name)s,
    %(_ingested_at)s,
    %(_source)s
)
ON CONFLICT (source_record_id)
DO UPDATE SET
    permit_number = EXCLUDED.permit_number,
    permit_type = EXCLUDED.permit_type,
    review_type = EXCLUDED.review_type,
    work_type = EXCLUDED.work_type,
    work_description = EXCLUDED.work_description,
    application_start_date = EXCLUDED.application_start_date,
    issue_date = EXCLUDED.issue_date,
    processing_time = EXCLUDED.processing_time,
    street_number = EXCLUDED.street_number,
    street_direction = EXCLUDED.street_direction,
    street_name = EXCLUDED.street_name,
    community_area = EXCLUDED.community_area,
    census_tract = EXCLUDED.census_tract,
    ward = EXCLUDED.ward,
    latitude = EXCLUDED.latitude,
    longitude = EXCLUDED.longitude,
    reported_cost = EXCLUDED.reported_cost,
    total_fee = EXCLUDED.total_fee,
    contact_1_type = EXCLUDED.contact_1_type,
    contact_1_name = EXCLUDED.contact_1_name,
    contact_2_type = EXCLUDED.contact_2_type,
    contact_2_name = EXCLUDED.contact_2_name,
    _ingested_at = EXCLUDED._ingested_at,
    _source = EXCLUDED._source;
"""

def upsert_permits(permits):
    """Insert or update raw permit records in PostgreSQL."""

    if not permits:
        return 0

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.executemany(
                UPSERT_PERMIT_SQL,
                permits,
            )

    return len(permits)