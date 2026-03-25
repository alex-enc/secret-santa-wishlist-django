""" Test for the Wishlist model"""

from django.core.exceptions import ValidationError
from django.test import TestCase
from secretsanta.models.user_model import User
from secretsanta.models.group_model import Group
from secretsanta.models.wishlist_model import Wishlist

class WishlistModelTestCase(TestCase):
    fixtures = ['secretsanta/tests/fixtures/default_user.json', 
                'secretsanta/tests/fixtures/default_group.json',
                'secretsanta/tests/fixtures/other_group.json']

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.group = Group.objects.get(code='DEFAULT123')
        self.group2 = Group.objects.get(code='OTHER123')

    # test create valid wishlist
    def test_valid_wishlist(self):
        wishlist = Wishlist(
            user= self.user,
            group = self.group
        )
        self._assert_wishlist_is_valid(wishlist)
    
    # test user cannot have more than one wishlist per group
    def test_user_cannot_have_more_than_one_wishlist_per_group(self):
            wishlist1 = Wishlist(
                user= self.user,
                group = self.group
            )
            wishlist1.save()

            wishlist2 = Wishlist(
                user= self.user,
                group = self.group
            )
            
            self._assert_wishlist_is_invalid(wishlist2)

    # test user can have multiple wishlists in different groups
    def test_user_can_have_multiple_wishlists_in_different_groups(self):
        wishlist1 = Wishlist(
            user= self.user,
            group = self.group
        )
        wishlist1.save()

        wishlist2 = Wishlist(
            user= self.user,
            group = self.group2
        )
        
        self._assert_wishlist_is_valid(wishlist2)

    def _assert_wishlist_is_valid(self, wishlist):
        try:
            wishlist.full_clean()
        except ValidationError:
            self.fail('Test wishlist should be valid')

    def _assert_wishlist_is_invalid(self, wishlist):
        with self.assertRaises(ValidationError):
            wishlist.full_clean()  


    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlists")
    # group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="wishlists")
    # created_at = models.DateTimeField(auto_now_add=True)
