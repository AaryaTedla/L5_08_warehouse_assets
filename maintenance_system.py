
"""Warehouse asset maintenance management system."""

import json
import tempfile
from datetime import datetime, timedelta

# Global state
assets = {}
registration_log = []
settings = {"service_interval_days": 90}

def register_asset(asset_id, machine_type, logs=None):
    """Register an asset and record the registration."""
    if logs is None:
        logs = registration_log
    assets[asset_id] = {"type": machine_type, "last_service": datetime.now().strftime("%Y-%m-%d")}
    logs.append(asset_id)
    print("Registered", asset_id, "- total registrations this run:", len(logs))

def update_service_date(asset_id, date):
    """Update the last service date for an asset."""
    try:
        assets[asset_id]["last_service"] = date
    except KeyError:
        print("Could not update", asset_id)

def due_for_inspection():
    """Return assets that are overdue for inspection."""
    due = []
    for asset_id, details in assets.items():
        last = datetime.strptime(details["last_service"], "%Y-%m-%d")
        if datetime.now() - last > timedelta(days=settings["service_interval_days"]):
            due.append(asset_id)
    return due

def change_interval(days):
    """Change the inspection interval in days."""
    settings["service_interval_days"] = days

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
        json.dump(assets, temp_file)
        path = temp_file.name
    print("Scratch copy at", path)

def print_alerts():
    """Print alerts for all overdue inspections."""
    for asset_id in due_for_inspection():
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
    update_service_date("FL-01", "2025-01-15")
    update_service_date("XX-99", "2025-02-01")
    change_interval(-30)
    d = input("Last service date for CV-07 (YYYY-MM-DD, Enter to skip): ")
    if d:
        update_service_date("CV-07", d)
    if not assets:
        raise RuntimeError("no assets")
    print_alerts()
    export_service_report()
    write_scratch_copy()

main()
