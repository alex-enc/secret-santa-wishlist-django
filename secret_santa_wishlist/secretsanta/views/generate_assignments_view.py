from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from secretsanta.models import Group, Assignment
from secretsanta.user_delegation import generate_secret_santa_assignments
from datetime import datetime

@login_required
def generate_assignments(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    user = request.user

    if group.admin != user:
        messages.error(request, "Only the group admin can generate assignments.")
        return redirect("my_groups")

    current_year = datetime.now().year
    if Assignment.objects.filter(group=group, year=current_year).exists():
        messages.warning(request, "Assignments have already been generated for this year.")
        return redirect("my_groups")

    success = generate_secret_santa_assignments(group)

    if success:
        messages.success(request, "Secret Santa assignments generated successfully!")
    else:
        messages.error(request, "Failed to generate assignments. Try again later.")

    return redirect("my_groups")