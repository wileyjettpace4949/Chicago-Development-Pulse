import requests
from datetime import datetime, timezone


BASE_URL = "https://data.cityofchicago.org/resource/ydr8-5enu.json"


def get_permits():
    """Retrieve a sample of Chicago building permit records."""

    try:
        response = requests.get(
            BASE_URL,
            params={
                "$limit": 10,
                "$order": "issue_date DESC",
            },
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:
        print(
            "Request timed out. "
            "The Chicago data API may be temporarily unavailable."
        )
        return []

    except requests.exceptions.RequestException as exc:
        print(f"API request failed: {exc}")
        return []


def shape_raw_permit(permit):
    """Map a Chicago permit record to our raw-layer schema."""

    return {
        # Source identifiers
        "source_record_id": permit.get("id"),
        "permit_number": permit.get("permit_"),

        # Permit attributes
        "permit_type": permit.get("permit_type"),
        "review_type": permit.get("review_type"),
        "work_type": permit.get("work_type"),
        "work_description": permit.get("work_description"),

        # Dates
        "application_start_date": permit.get("application_start_date"),
        "issue_date": permit.get("issue_date"),
        "processing_time": permit.get("processing_time"),

        # Location
        "street_number": permit.get("street_number"),
        "street_direction": permit.get("street_direction"),
        "street_name": permit.get("street_name"),
        "community_area": permit.get("community_area"),
        "census_tract": permit.get("census_tract"),
        "ward": permit.get("ward"),
        "latitude": permit.get("latitude"),
        "longitude": permit.get("longitude"),

        # Financials
        "reported_cost": permit.get("reported_cost"),
        "total_fee": permit.get("total_fee"),

        # Contacts
        "contact_1_type": permit.get("contact_1_type"),
        "contact_1_name": permit.get("contact_1_name"),
        "contact_2_type": permit.get("contact_2_type"),
        "contact_2_name": permit.get("contact_2_name"),
    }


def add_ingestion_metadata(permits):
    """Shape source records and add ingestion metadata."""

    ingested_at = datetime.now(timezone.utc).isoformat()

    raw_permits = []

    for permit in permits:
        record = shape_raw_permit(permit)

        record["_ingested_at"] = ingested_at
        record["_source"] = "chicago_building_permits"

        raw_permits.append(record)

    return raw_permits


def validate_raw_permits(permits):
    """Validate required fields in raw permit records."""

    required_fields = [
        "source_record_id",
        "permit_number",
    ]

    for permit in permits:
        for field in required_fields:
            if not permit.get(field):
                raise ValueError(
                    f"Missing required field '{field}' "
                    f"for source record {permit.get('source_record_id')}"
                )

            
if __name__ == "__main__":
    permits = get_permits()

    if permits:
        raw_permits = add_ingestion_metadata(permits)

        validate_raw_permits(raw_permits)

        print(f"Prepared {len(raw_permits)} raw permit records")
        print(raw_permits[0])