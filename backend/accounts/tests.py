from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.protected_urls = [
            reverse('dashboard'),
            reverse('patient_list'),
            reverse('rendezvous_list'),
            reverse('consultation_list'),
            reverse('billing:facture_list'),
        ]

    def test_redirect_if_not_logged_in(self):
        """Test that protected pages redirect to login when not authenticated"""
        for url in self.protected_urls:
            response = self.client.get(url)
            self.assertRedirects(response, f'/accounts/login/?next={url}')

    def test_access_if_logged_in(self):
        """Test that pages are accessible when logged in"""
        self.client.force_login(self.user)
        for url in self.protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Failed to access {url}")

    def test_login_view(self):
        """Test that login page loads"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
