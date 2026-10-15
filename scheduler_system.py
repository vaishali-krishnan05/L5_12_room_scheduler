
"""Conference room and equipment scheduling system."""

import json
from datetime import datetime

# Shared scheduler state.
reservations = {}
equipment_pool = {"projector": 2, "microphone": 4, "webcam": 1}
conflicts = []
next_reservation = 1


def schedule_room(room_id, time_slot, equipment_list=None):
    """Schedule a room, recording conflicts and allocating equipment."""
    global next_reservation

    if not isinstance(time_slot, str):
        raise TypeError("time_slot must be a string in HH-HH format")

    slot_hours(time_slot)

    if equipment_list is None:
        equipment_list = []
    else:
        equipment_list = list(equipment_list)

    for reservation in reservations.values():
        if (
            reservation["room"] == room_id
            and reservation["slot"] == time_slot
        ):
            conflicts.append(
                f"{room_id} double-booked at {time_slot}"
            )

    for equipment in equipment_list:
        if equipment not in equipment_pool:
            raise ValueError(f"Unknown equipment: {equipment}")
        if equipment_pool[equipment] <= 0:
            raise ValueError(f"No {equipment} available")

    for equipment in equipment_list:
        equipment_pool[equipment] -= 1

    reservations[next_reservation] = {
        "room": room_id,
        "slot": time_slot,
        "equipment": equipment_list,
    }
    reservation_id = next_reservation
    next_reservation += 1
    return reservation_id


def cancel_reservation(reservation_id):
    """Cancel a reservation and return its equipment to the pool."""
    if reservation_id not in reservations:
        return False

    for equipment in reservations[reservation_id]["equipment"]:
        equipment_pool[equipment] += 1

    del reservations[reservation_id]
    return True


def slot_hours(time_slot):
    """Return the duration of a valid time slot expressed as HH-HH."""
    if not isinstance(time_slot, str) or time_slot.count("-") != 1:
        raise ValueError("Time slot must use the format HH-HH")

    start_text, end_text = time_slot.split("-")

    if not start_text.isdigit() or not end_text.isdigit():
        raise ValueError("Start and end times must be numeric")

    start = int(start_text)
    end = int(end_text)

    if not (0 <= start <= 23 and 0 <= end <= 24):
        raise ValueError("Times must be within a 24-hour day")
    if end <= start:
        raise ValueError("End time must be later than start time")

    return end - start


def export_schedule(file="schedule.json"):
    """Export current reservations to a JSON file."""
    with open(file, "w", encoding="utf-8") as output_file:
        json.dump(reservations, output_file, indent=2)


def log_conflicts(file="conflicts.log"):
    """Append detected scheduling conflicts to a log file."""
    with open(file, "a", encoding="utf-8") as output_file:
        for conflict in conflicts:
            output_file.write(f"{datetime.now()} {conflict}\n")


def main():
    """Run a sample scheduling session."""
    schedule_room("Board-1", "09-11")
    schedule_room("Board-1", "09-11")
    second_reservation = schedule_room("Huddle-3", "14-16")

    print(
        "Slot length for second reservation:",
        slot_hours(reservations[second_reservation]["slot"]),
    )
    print("First reservation cancelled:", cancel_reservation(77))

    slot = input(
        "Slot for Board-2, like 10-12 (Enter for 10-12): "
    ) or "10-12"

    try:
        schedule_room("Board-2", slot, ["projector", "webcam"])
    except (TypeError, ValueError) as error:
        print(f"Could not schedule Board-2: {error}")

    export_schedule()
    log_conflicts()
    print("Equipment left:", equipment_pool)
    print("Reservations:", reservations)


if __name__ == "__main__":
    main()
