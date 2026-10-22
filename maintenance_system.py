
"""Warehouse asset maintenance management system."""

import json
import tempfile
from datetime import date, datetime, timedelta


# Global state
assets = {}
registration_log = []
settings = {"service_interval_days": 90}


def register_asset(asset_id, machine_type, logs=None):
    """Register an asset after validating its details."""
    if logs is None:
        logs = registration_log

    if not isinstance(asset_id, str) or not asset_id.strip():
        print("Registration failed: Asset ID cannot be empty.")
        return False

    if not isinstance(machine_type, str) or not machine_type.strip():
        print("Registration failed: Machine type cannot be empty.")
        return False

    asset_id = asset_id.strip()
    machine_type = machine_type.strip()

    if asset_id in assets:
        print(f"Registration failed: {asset_id} already exists.")
        return False

    assets[asset_id] = {
        "type": machine_type,
        "last_service": date.today().isoformat()
    }

    logs.append(asset_id)

    print(
        "Registered",
        asset_id,
        "- total registrations this run:",
        len(logs)
    )
    return True


def update_service_date(asset_id, service_date):
    """Update an asset's service date after validation."""
    if asset_id not in assets:
        print(f"Could not update {asset_id}: Asset not found.")
        return False

    if not isinstance(service_date, str):
        print("Invalid service date: Use YYYY-MM-DD.")
        return False

    try:
        parsed_date = datetime.strptime(
            service_date.strip(), "%Y-%m-%d"
        ).date()
    except ValueError:
        print("Invalid service date: Use YYYY-MM-DD.")
        return False

    if parsed_date > date.today():
        print("Invalid service date: Future dates are not allowed.")
        return False

    assets[asset_id]["last_service"] = parsed_date.isoformat()
    print(f"Service date updated for {asset_id}.")
    return True


def due_for_inspection():
    """Return assets whose inspections are overdue."""
    due = []
    today = date.today()

    interval = timedelta(
        days=settings["service_interval_days"]
    )

    for asset_id, details in assets.items():
        last_service = date.fromisoformat(
            details["last_service"]
        )

        if today - last_service > interval:
            due.append(asset_id)

    return due


def change_interval(days):
    """Change the inspection interval after validation."""
    if isinstance(days, bool) or not isinstance(days, int):
        print("Invalid interval: Enter a positive integer.")
        return False

    if days <= 0:
        print("Invalid interval: Days must be greater than zero.")
        return False

    settings["service_interval_days"] = days
    print(f"Inspection interval updated to {days} days.")
    return True


def export_service_report(file="maintenance.json"):
    """Export all asset records to a JSON file."""
    with open(file, "w", encoding="utf-8") as report:
        json.dump(assets, report, indent=2)

    print("Report written to " + file)


def write_scratch_copy():
    """Write a secure temporary JSON copy of asset records."""
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        encoding="utf-8",
        delete=False
    ) as temp_file:
        json.dump(assets, temp_file, indent=2)
        path = temp_file.name

    print("Scratch copy at", path)


def print_alerts():
    """Print alerts for all overdue inspections."""
    overdue_assets = due_for_inspection()

    if not overdue_assets:
        print("No overdue inspections found.")
        return

    for asset_id in overdue_assets:
        print(
            "ALERT: inspection overdue for",
            asset_id,
            assets[asset_id]["type"]
        )


def main():
    """Run the warehouse maintenance system."""
    register_asset("FL-01", "Forklift")
    register_asset("CV-07", "Conveyor")
    register_asset("", "Pallet Jack")
    register_asset("FL-01", "Crane")
    register_asset("PJ-03", "Pallet Jack")

    update_service_date("FL-01", "2025-01-15")
    update_service_date("XX-99", "2025-02-01")

    change_interval(-30)
    change_interval(90)

    user_date = input(
        "Last service date for CV-07 "
        "(YYYY-MM-DD, Enter to skip): "
    ).strip()

    if user_date:
        update_service_date("CV-07", user_date)

    if not assets:
        raise RuntimeError("No assets are registered.")

    print_alerts()
    export_service_report()
    write_scratch_copy()


if __name__ == "__main__":
    main()
