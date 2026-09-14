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
        print("Request timed out. The Chicago data API may be temporarily unavailable.")
        return []

    except requests.exceptions.RequestException as exc:
        print(f"API request failed: {exc}")
        return []

def add_ingestion_metadata(permits):
    """Add metadata about when and where each record was ingested."""

    ingested_at = datetime.now(timezone.utc).isoformat()

    enriched_permits = []

    for permit in permits:
        record = permit.copy()

        record["_ingested_at"] = ingested_at
        record["_source"] = "chicago_building_permits"

        enriched_permits.append(record)

    return enriched_permits

def check_identifier_uniqueness(permits):
    """Check whether candidate identifier fields are unique."""

    ids = [permit.get("id") for permit in permits]
    permit_numbers = [permit.get("permit_") for permit in permits]

    print("\nIdentifier checks:")

    print(f"Rows: {len(permits)}")
    print(f"Unique IDs: {len(set(ids))}")
    print(f"Unique permit numbers: {len(set(permit_numbers))}")

    duplicate_ids = len(ids) - len(set(ids))
    duplicate_permit_numbers = len(permit_numbers) - len(set(permit_numbers))

    print(f"Duplicate IDs: {duplicate_ids}")
    print(f"Duplicate permit numbers: {duplicate_permit_numbers}")


if __name__ == "__main__":
    permits = get_permits()

    if permits:
        raw_permits = add_ingestion_metadata(permits)

        print(f"Retrieved {len(raw_permits)} permits")

        check_identifier_uniqueness(raw_permits)