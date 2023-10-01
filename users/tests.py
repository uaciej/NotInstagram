from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Tier

class TierModelTest(TestCase):
    def setUp(self):
        self.tier = Tier.objects.create(
            name='Test Tier',
            thumbnail_sizes='100',
            link_enabled=True,
            expiring_link_enabled=False
        )

    def test_tier_creation(self):
        self.assertEqual(Tier.objects.count(), 4) # 3 predefined ones and the extra 1
        self.assertEqual(self.tier.name, 'Test Tier')

class AccountModelTest(TestCase):
    def setUp(self):
        self.tier = Tier.objects.create(
            name='Test Tier',
            thumbnail_sizes='100x100',
            link_enabled=True,
            expiring_link_enabled=False
        )
        self.user = get_user_model().objects.create_user(
            email='testuser@test.com',
            password='testpass123',
            tier=self.tier
        )

    def test_user_creation(self):
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(self.user.email, 'testuser@test.com')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertEqual(self.user.tier, self.tier)

    def test_create_superuser(self):
        admin_user = get_user_model().objects.create_superuser(
            email='adminuser@test.com',
            password='testpass123'
        )
        self.assertEqual(get_user_model().objects.count(), 2)
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)