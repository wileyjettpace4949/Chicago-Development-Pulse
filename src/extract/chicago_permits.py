import requests


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


if __name__ == "__main__":
    permits = get_permits()

    if permits:
        print(f"Retrieved {len(permits)} permits")

        print("\nFields returned by the API:")
        for field in permits[0].keys():
            print(field)

        print("\nField completeness:")

        all_fields = set()

        for permit in permits:
            all_fields.update(permit.keys())

        for field in sorted(all_fields):
            populated = sum(
                1 for permit in permits
                if permit.get(field) not in (None, "")
            )

            print(f"{field}: {populated}/{len(permits)}")