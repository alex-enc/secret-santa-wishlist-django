import random
from datetime import datetime
from .models import Assignment

def generate_secret_santa_assignments(group):
    """
    Randomly assign each member in a group another member to gift to.
    Avoids giving someone they had in the last 3 years (if possible).
    Saves assignments to the database.
    """

    members = [m.user for m in group.memberships.all()]

    current_year = datetime.now().year

    if len(members) < 2:
        return False  # Not enough members to assign

    # Build exclusion history for each member
    exclusion_map = {}
    for giver in members:
        recent_receivers = Assignment.objects.filter(
            giver=giver,
            group=group,
            year__gte=current_year - 3
        ).values_list("receiver_id", flat=True)
        exclusion_map[giver.id] = set(recent_receivers) | {giver.id}  # Can't gift themselves either

    # Attempt to find valid assignments
    attempts = 0
    while attempts < 500:
        receivers = members[:]
        random.shuffle(receivers)

        valid = True
        for giver, receiver in zip(members, receivers):
            if receiver.id in exclusion_map[giver.id]:
                valid = False
                break

        if valid:
            # Success — save assignments
            for giver, receiver in zip(members, receivers):
                Assignment.objects.create(
                    giver=giver,
                    receiver=receiver,
                    group=group,
                    year=current_year
                )
            return True  # Done!

        attempts += 1

    # If no perfect match found, relax constraint and try again
    # (for very small groups)
    receivers = members[:]
    random.shuffle(receivers)
    for giver, receiver in zip(members, receivers):
        if giver != receiver:
            Assignment.objects.create(
                giver=giver,
                receiver=receiver,
                group=group,
                year=current_year
            )

    return True
