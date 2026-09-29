from src.extract.chicago_permits import (
    add_ingestion_metadata,
    get_permits,
    validate_raw_permits,
)
from src.load.postgres import upsert_permits


def run_permit_pipeline():
    """Run the Chicago building permits ingestion pipeline."""

    permits = get_permits()

    if not permits:
        print("No permits retrieved.")
        return

    raw_permits = add_ingestion_metadata(permits)

    validate_raw_permits(raw_permits)

    rows_loaded = upsert_permits(raw_permits)

    print(f"Loaded {rows_loaded} permit records.")


if __name__ == "__main__":
    run_permit_pipeline()