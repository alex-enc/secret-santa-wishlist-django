from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from secretsanta.models import GroupMember, Group, Assignment, Wishlist
from secretsanta.forms.sign_up_form import SignUpForm
from secretsanta.forms.log_in_form import LogInForm 
from secretsanta.forms.create_group_form import CreateGroupForm 
from secretsanta.forms.join_group_form import JoinGroupForm 
from secretsanta.forms.add_wishlist_item_form import WishlistItemForm 
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from secretsanta.user_delegation import generate_secret_santa_assignments

# Create your views here.
def home(request):
    return render(request, 'home.html') 

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(form.is_bound)
        if form.is_valid():
            print("Form is valid")
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})



def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard') 
            else:
                messages.error(request, 'Invalid username or password.')  # Add error message
        else:
            messages.error(request, 'Please correct the error below.')  # For form errors

    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

def dashboard(request):
    user = request.user
    member_groups = Group.objects.filter(memberships__user=user).distinct()
    join_group_form = JoinGroupForm(request.POST)
    if join_group_form.is_valid():
        group_code = join_group_form.cleaned_data["group_code"] 
        # Check if a group with this code exists
        try:
            group = Group.objects.get(code=group_code)
        except Group.DoesNotExist:
            messages.error(request, 'Invalid group code.')
        else:
            # Add user as member if not already a member
            GroupMember.objects.get_or_create(
                user=request.user,
                group=group,
                defaults={"is_admin": False},
            )
            messages.success(request, f"You have successfully joined {group.name}.")
            return redirect("dashboard")
    else:
        join_group_form = JoinGroupForm()

    add_wishlist_item_form = WishlistItemForm(request.POST)
    """IF user does not have a wishlist for this group yet, create a wishlist and add wishlist items to it
     Get or create wishlist
  """
    # wishlist, created = Wishlist.objects.get_or_create(        
    #     user=request.user,
    #     group=group
    # ) 
    if add_wishlist_item_form.is_valid():
            print("Form is valid")
            item = add_wishlist_item_form.save(commit=False)
            item.wishlist = wishlist
            item.save()
            messages.success(request, "Item added to your wishlist!")
    else:
        add_wishlist_item_form = WishlistItemForm()

    return render(request, "dashboard.html", {"join_group_form": join_group_form, "member_groups": member_groups, "add_wishlist_item_form": add_wishlist_item_form})

def new_group_info(request):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            form.save(admin=request.user)  # Set the logged-in user as the admin
            messages.success(request, 'Group created successfully!')
            return redirect('dashboard')  # Redirect to the dashboard or any other page
        else:
            messages.error(request, 'There was an error creating the group.')
    else:
        form = CreateGroupForm()

    return render(request, 'new_group_info.html', {'form': form})

@login_required
def create_group(request):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        print(form.is_bound)
        
        if form.is_valid():
            print("Form is valid")
            form.save(admin=request.user)
            messages.success(request, 'Group created successfully!')
            return redirect('my_groups')  # Redirect to the dashboard or any other page
        else:
            messages.error(request, 'There was an error creating the group.')
    else:
        form = CreateGroupForm()

    return render(request, 'create_group.html', {'form': form})

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

@login_required
def profile(request):
    user = request.user
    
    return render(request, "profile.html", {'user': user})

# views.py

@login_required
def my_wishlist(request, group_id):
    group = get_object_or_404(Group, id=group_id)   
    # Get or create wishlist
    wishlist, created = Wishlist.objects.get_or_create(
        user=request.user,
        group=group
    )

    items = wishlist.items.all()
    form = WishlistItemForm()

    return render(request, "wishlist/my_wishlist.html", {
        "group": group,
        "wishlist": wishlist,
        "items": items,
        "form": form,
    })
    
def log_out(request):
    logout(request)
    return redirect('home')