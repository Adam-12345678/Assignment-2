# shop/tests.py

from django.test import TestCase
from django.urls import reverse
from .models import Product, Subscription
from django.contrib.auth.models import User

# Model Tests
class ProductModelTests(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name='Test Product',
            description='A description of the product.',
            price=99.99,
            stock=10
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Test Product')

    def test_product_price(self):
        self.assertEqual(self.product.price, 99.99)

    def test_product_stock(self):
        self.assertEqual(self.product.stock, 10)


class SubscriptionModelTests(TestCase):

    def setUp(self):
        user = User.objects.create(username='testuser')
        self.subscription = Subscription.objects.create(
            user=user,
            email_confirmed=True,
            access_level={"level": "premium"}
        )

    def test_subscription_str(self):
        self.assertEqual(self.subscription.user.username, 'testuser')
        self.assertTrue(self.subscription.email_confirmed)


# View Tests
class ViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_product_list_view(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product_list.html')
    
    def test_catalog_view(self):
        response = self.client.get(reverse('catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/catalog.html')
    
    def test_register_view_post(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'securepassword',
            'password2': 'securepassword'
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())  # Check if the user was created

    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/register.html')