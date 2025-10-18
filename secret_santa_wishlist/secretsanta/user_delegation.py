# Write a function that delegates the user a random user. Make sure they did not have them the past 3 years.

import random
from datetime import datetime, timedelta
from secret_santa_wishlist.secretsanta.models import User, Assignment
def delegate_user(current_user):
    # Get the current year
    current_year = datetime.now().year
    
    # Get the list of users that the current user has been assigned in the past 3 years
    past_assignments = Assignment.objects.filter(
        giver=current_user,
        year__gte=current_year - 3
    ).values_list('receiver_id', flat=True)
    
    # Get all users excluding the current user and those they have been assigned in the past 3 years
    eligible_users = User.objects.exclude(
        id__in=past_assignments
    ).exclude(
        id=current_user.id
    )
    
    # If there are no eligible users, return None
    if not eligible_users.exists():
        return None
    
    # Randomly select an eligible user
    selected_user = random.choice(eligible_users)
    
    return selected_user    

# Example usage:
# current_user = User.objects.get(id=1)  # Replace with actual user retrieval
# assigned_user = delegate_user(current_user)
# print(f"Assigned user: {assigned_user}")
