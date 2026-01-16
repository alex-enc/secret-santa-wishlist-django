from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from secretsanta.models import Group, Assignment
from datetime import datetime

@login_required
def my_groups(request):
    user = request.user
    created_groups = user.admin_groups.all()  # groups this user created
    # groups = user.groups.all() # groups the user belongs to
    member_groups = Group.objects.filter(memberships__user=user).distinct()
    # Find the user’s assignments for the current year
    current_year = datetime.now().year
   
    # current_year = 2025  # hardcode this for now; replace with datetime.now().year once tested

    # All assignments where this user is the giver
    user_assignments = Assignment.objects.filter(giver=user, year=current_year)

    # Attach receiver to each group
    for group in member_groups:
        assignment = user_assignments.filter(group=group).first()
        if assignment:
            group.assigned_receiver = assignment.receiver
            print(f"✅ Found assignment for {group.name}: {assignment.giver.username} → {assignment.receiver.username}")
        else:
            group.assigned_receiver = None
            print(f"⚠️ No assignment for {group.name}")

    return render(request, "my_groups.html", {"created_groups": created_groups, "member_groups": member_groups, "user": user})
