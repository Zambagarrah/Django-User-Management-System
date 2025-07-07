from django.test import TestCase, Client
from django.urls import reverse
from .models import CustomUser

# Create your tests here.
class CustomUserModelTest(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='pass1234')
        self.assertEqual(user.username, 'testuser')
        self.assertFalse(user.is_verified)
        self.assertTrue(user.check_password('pass1234'))
        
class RegistrationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_registration_page_loads(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_valid_registration(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after registration
        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())
        
class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='profileuser', email='p@example.com', password='pass1234')
        self.client.login(username='profileuser', password='pass1234')

    def test_profile_view(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'profileuser')

    def test_verification_toggle(self):
        response = self.client.get(reverse('verify_user'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified)

