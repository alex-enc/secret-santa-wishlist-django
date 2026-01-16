# from django.contrib.auth.decorators import login_required
# from django.shortcuts import get_object_or_404, render
# from secretsanta.models import Group, Wishlist
# from secretsanta.forms.wishlist_item_form import WishlistItemForm

# @login_required
# def my_wishlist(request, group_id):
#     group = get_object_or_404(Group, id=group_id)   
#     # Get or create wishlist
#     wishlist, created = Wishlist.objects.get_or_create(
#         user=request.user,
#         group=group
#     )

#     items = wishlist.items.all()
#     form = WishlistItemForm()

#     return render(request, "wishlist/my_wishlist.html", {
#         "group": group,
#         "wishlist": wishlist,
#         "items": items,
#         "form": form,
#     })
    
