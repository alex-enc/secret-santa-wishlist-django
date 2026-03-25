""" Tests for Wishlist Item model """

from django.core.exceptions import ValidationError
from django.test import TestCase
from secretsanta.models.user_model import User
from secretsanta.models.group_model import Group
from secretsanta.models.wishlist_model import Wishlist
from secretsanta.models.wishlist_item_model import WishlistItem

class WishlistItemModelTestCase(TestCase):
    fixtures = ['secretsanta/tests/fixtures/default_user.json', 
                'secretsanta/tests/fixtures/default_group.json',
                'secretsanta/tests/fixtures/other_group.json']

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.group = Group.objects.get(code='DEFAULT123')
        self.group2 = Group.objects.get(code='OTHER123')
        self.wishlist = Wishlist.objects.create(user=self.user, group=self.group)

    # test create wishlist item
    def test_valid_wishlist_item(self):
        wishlist_item =  WishlistItem(
            wishlist=self.wishlist,
            item_name = 'Test Item',
            item_url = 'https://www.example.com/test-item',
            description = 'This is a test item description.',
            taken = False
        )
        self._assert_wishlist_item_is_valid(wishlist_item)

    # test item name is blank
    def test_wishlist_item_with_blank_name(self):
        wishlist_item = WishlistItem(
            wishlist = self.wishlist,
            item_name = '',
            item_url = 'https://www.example.com/test-item',
            description = 'This is a test item description.',
            taken = False
        )
        self._assert_wishlist_item_is_invalid(wishlist_item)

    #  test item name is too long
    def test_wishlist_item_name_too_long(self):
        wishlist_item = WishlistItem(
            wishlist = self.wishlist,
            item_name = 'A' * 256,
            item_url = 'https://www.example.com/test-item',
            description = 'This is a test item description.',
            taken = False
        )
        self._assert_wishlist_item_is_invalid(wishlist_item)

    # test item url is invalid
    def test_wishlist_item_with_invalid_url(self):
        wishlist_item = WishlistItem(
            wishlist = self.wishlist,
            item_name = 'Test Item',
            item_url = 'invalid-url',
            description = 'This is a test item description.',
            taken = False
        )
        self._assert_wishlist_item_is_invalid(wishlist_item)

    # test item url is blank
    def test_wishlist_item_with_blank_url(self):
        wishlist_item = WishlistItem(
            wishlist = self.wishlist,
            item_name = 'Test Item',
            item_url = None,
            description = 'This is a test item description.',
            taken = False
        )
        self._assert_wishlist_item_is_valid(wishlist_item)

    # test item description is blank
    def test_wishlist_item_with_blank_description(self):
        wishlist_item = WishlistItem(
            wishlist = self.wishlist,
            item_name = 'Test Item',
            item_url = 'https://www.example.com/test-item',
            description = None,
            taken = False
        )
        self._assert_wishlist_item_is_valid(wishlist_item)

    # test item is taken
    def test_wishlist_item_is_taken(self):
        wishlist_item = WishlistItem(
            wishlist = self.wishlist,
            item_name = 'Test Item',
            item_url = 'https://www.example.com/test-item',
            description = 'This is a test item description.',
            taken = True
        )
        self._assert_wishlist_item_is_valid(wishlist_item)

    # test item is not taken
    def test_wishlist_item_is_not_taken(self):
        wishlist_item = WishlistItem(
            wishlist = self.wishlist,
            item_name = 'Test Item',
            item_url = 'https://www.example.com/test-item',
            description = 'This is a test item description.',
            taken = False
        )
        self._assert_wishlist_item_is_valid(wishlist_item)

    # test that wishlist items are deleted when wishlist is deleted
    def test_items_deleted_with_wishlist(self):
        WishlistItem.objects.create(
            wishlist=self.wishlist,
            item_name='Test Item',
            item_url = 'https://www.example.com/test-item',
            description = 'This is a test item description.',
            taken = False
        )

        self.wishlist.delete()

        self.assertEqual(WishlistItem.objects.count(), 0)
        
    def _assert_wishlist_item_is_valid(self, wishlist_item):
            try:
                wishlist_item.full_clean()
            except ValidationError:
                self.fail('Test wishlist item should be valid')

    def _assert_wishlist_item_is_invalid(self, wishlist_item):
            with self.assertRaises(ValidationError):
                wishlist_item.full_clean()






    # wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name="items")
    # item_name = models.CharField(max_length=255)
    # item_url = models.URLField(blank=True, null=True)
    # description = models.TextField(blank=True, null=True)
    # taken = models.BooleanField(default=False)  # Whether the item has been taken by a giver
    # created_at = models.DateTimeField(auto_now_add=True)
   