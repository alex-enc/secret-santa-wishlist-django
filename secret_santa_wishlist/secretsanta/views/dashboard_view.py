from secretsanta.models import GroupMember, Group, Wishlist
from django.shortcuts import get_object_or_404, redirect, render
from secretsanta.forms.join_group_form import JoinGroupForm 
from secretsanta.forms.add_wishlist_item_form import WishlistItemForm 
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    user = request.user

    # GROUPS USER BELONGS TO
    member_groups = Group.objects.filter(memberships__user=user).distinct()

    selected_group = None
    wishlist = None
    items = []

    # RESTORE SELECTED GROUP (SESSION)
    selected_group_id = request.session.get("selected_group_id")

    if selected_group_id:
        selected_group = Group.objects.filter(
            id=selected_group_id,
            memberships__user=user
        ).first()

    # Auto-select if only one group
    if not selected_group and member_groups.count() == 1:
        selected_group = member_groups.first()
        request.session["selected_group_id"] = selected_group.id

    # HANDLE GROUP SELECTION (DROPDOWN)
    if request.method == "POST" and "selected_group" in request.POST:
        selected_group_id = request.POST.get("selected_group")

        if selected_group_id:
            selected_group = get_object_or_404(
                Group,
                id=selected_group_id,
                memberships__user=user
            )
            request.session["selected_group_id"] = selected_group.id

        return redirect("dashboard")  #  prevents double-POST bugs

    # LOAD MEMBERS IN SELECTED GROUP


    # LOAD WISHLIST + ITEMS
    if selected_group:
        wishlist = Wishlist.objects.filter(
            user=user,
            group=selected_group
        ).first()

        if wishlist:
            items = wishlist.items.all()



    # JOIN GROUP FORM
    join_group_form = JoinGroupForm(request.POST or None)

    if request.method == "POST" and "join_group" in request.POST:
        if join_group_form.is_valid():
            group_code = join_group_form.cleaned_data["group_code"]

            try:
                group = Group.objects.get(code=group_code)
            except Group.DoesNotExist:
                messages.error(request, "Invalid group code.")
            else:
                GroupMember.objects.get_or_create(
                    user=user,
                    group=group,
                    defaults={"is_admin": False},
                )
                messages.success(request, f"You joined {group.name}!")
                request.session["selected_group_id"] = group.id
                return redirect("dashboard")

    # ADD WISHLIST ITEM FORM
    add_wishlist_item_form = WishlistItemForm(request.POST or None)

    if request.method == "POST" and "add_wishlist_item" in request.POST:
        if not selected_group:
            messages.error(request, "Please select a group first.")
            return redirect("dashboard")

        if add_wishlist_item_form.is_valid():
            wishlist, _ = Wishlist.objects.get_or_create(
                user=user,
                group=selected_group
            )

            item = add_wishlist_item_form.save(commit=False)
            item.wishlist = wishlist
            item.save()

            messages.success(request, "Wishlist item added!")
            return redirect("dashboard")

    return render(
        request,
        "dashboard.html",
        {
            "member_groups": member_groups,
            "selected_group": selected_group,
            "wishlist": wishlist,
            "items": items,
            "join_group_form": join_group_form,
            "add_wishlist_item_form": add_wishlist_item_form,
        }
    )