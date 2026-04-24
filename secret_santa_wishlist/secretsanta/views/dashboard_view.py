from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from secretsanta.models import Group, GroupMember, Wishlist, WishlistItem
from secretsanta.forms.join_group_form import JoinGroupForm
from secretsanta.forms.create_group_form import CreateGroupForm
from secretsanta.forms.add_wishlist_item_form import WishlistItemForm


@login_required
def dashboard(request):
    user = request.user

    # ---------------------------------
    # GROUPS USER BELONGS TO
    # ---------------------------------
    member_groups = Group.objects.filter(
        memberships__user=user
    ).distinct()

    selected_group = None
    wishlist = None
    items = []

    # ---------------------------------
    # RESTORE SELECTED GROUP FROM SESSION
    # ---------------------------------
    selected_group_id = request.session.get("selected_group_id")

    if selected_group_id:
        selected_group = Group.objects.filter(
            id=selected_group_id,
            memberships__user=user
        ).first()

    # Auto-select first group
    if not selected_group and member_groups.exists():
        selected_group = member_groups.first()
        request.session["selected_group_id"] = selected_group.id

    # ---------------------------------
    # FORMS
    # ---------------------------------
    create_group_form = CreateGroupForm()
    join_group_form = JoinGroupForm()
    add_wishlist_item_form = WishlistItemForm()

    # ---------------------------------
    # HANDLE POST ACTIONS
    # ---------------------------------
    if request.method == "POST":

        # -----------------------------
        # CHANGE SELECTED GROUP
        # -----------------------------
        if "selected_group" in request.POST:
            group_id = request.POST.get("selected_group")

            if group_id:
                selected_group = get_object_or_404(
                    Group,
                    id=group_id,
                    memberships__user=user
                )
                request.session["selected_group_id"] = selected_group.id

            return redirect("dashboard")

        # -----------------------------
        # CREATE GROUP
        # -----------------------------
        elif "create_group" in request.POST:
            create_group_form = CreateGroupForm(request.POST)

            if create_group_form.is_valid():
                create_group_form.save(admin=user)
                messages.success(request, "Group created successfully!")
                return redirect("my_groups")

            messages.error(request, "There was an error creating the group.")

        # -----------------------------
        # JOIN GROUP
        # -----------------------------
        elif "join_group" in request.POST:
            join_group_form = JoinGroupForm(request.POST)

            if join_group_form.is_valid():
                code = join_group_form.cleaned_data["group_code"]

                try:
                    group = Group.objects.get(code=code)
                except Group.DoesNotExist:
                    messages.error(request, "Invalid group code.")
                else:
                    GroupMember.objects.get_or_create(
                        user=user,
                        group=group,
                        defaults={"is_admin": False}
                    )

                    request.session["selected_group_id"] = group.id
                    messages.success(request, f"You joined {group.name}!")
                    return redirect("dashboard")

        # -----------------------------
        # ADD WISHLIST ITEM
        # -----------------------------
        elif "add_wishlist_item" in request.POST:
            if not selected_group:
                messages.error(request, "Please select a group first.")
                return redirect("dashboard")

            add_wishlist_item_form = WishlistItemForm(request.POST)

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

        # -----------------------------
        # EDIT WISHLIST ITEM
        # -----------------------------
        elif "edit_wishlist_item" in request.POST:
            item = get_object_or_404(
                WishlistItem,
                id=request.POST["item_id"],
                wishlist__user=user
            )

            item.item_name = request.POST.get("item_name", "")
            item.item_url = request.POST.get("item_url", "")
            item.description = request.POST.get("description", "")
            item.save()

            messages.success(request, "Item updated!")
            return redirect("dashboard")

        # -----------------------------
        # DELETE WISHLIST ITEM
        # -----------------------------
        elif "delete_wishlist_item" in request.POST:
            item = get_object_or_404(
                WishlistItem,
                id=request.POST["item_id"],
                wishlist__user=user
            )

            item.delete()
            messages.success(request, "Item deleted!")
            return redirect("dashboard")
        # ---------------------------------
        # PUBLISH WISHLIST
        # ---------------------------------
        elif "publish_wishlist" in request.POST:
            wishlist, created = Wishlist.objects.get_or_create(
                user=user,
                group=selected_group
            )
            
            wishlist.published = True
            wishlist.save()
            print("Wishlist published:", wishlist.published)
            messages.success(request, "Wishlist published!")
            return redirect("dashboard")
        # ---------------------------------
        # UNPUBLISH WISHLIST
        # ---------------------------------
        elif "unpublish_wishlist" in request.POST:
            wishlist = Wishlist.objects.filter(
                user=user,
                group=selected_group
            ).first()

            if wishlist:
                wishlist.published = False
                wishlist.save()
                messages.success(request, "Wishlist unpublished!")
            return redirect("dashboard")
        
    # ---------------------------------
    # LOAD WISHLIST + ITEMS
    # ---------------------------------
    if selected_group:
        wishlist = Wishlist.objects.filter(
            user=user,
            group=selected_group
        ).first()

        if wishlist:
            items = wishlist.items.all()

    # ---------------------------------
    # OTHER USER'S WISHLIST
    # ---------------------------------
    selected_group_members = selected_group.memberships.exclude(user=user).select_related("user") if selected_group else []

    wishlists = Wishlist.objects.filter(
        group=selected_group,
        user__in=[m.user for m in selected_group_members]
    ).prefetch_related("items")

    wishlist_map = {w.user_id: w for w in wishlists}

    for member in selected_group_members:
        member.group_wishlist = wishlist_map.get(member.user_id)

    # ---------------------------------
    # RENDER PAGE
    # ---------------------------------
    return render(
        request,
        "dashboard.html",
        {
            "member_groups": member_groups,
            "selected_group": selected_group,
            "wishlist": wishlist,
            "items": items,
            "create_group_form": create_group_form,
            "join_group_form": join_group_form,
            "add_wishlist_item_form": add_wishlist_item_form,
            "selected_group_members": selected_group_members if selected_group else [],
        }
    )