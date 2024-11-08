from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from icecream import ic


User = get_user_model()


class PasswordChangeTest(TestCase):
    def setUp(self):
        # Create user with email login
        self.user = User.objects.create_user(
            first_name='Test',
            last_name='User',
            email='testuser@example.com',
            password='testpass123'
        )
        
        # Attempt login to confirm user setup
        ic(self.user)
        login_success = self.client.login(email=self.user.email, password='testpass123')
        self.assertTrue(login_success, "Initial login failed in setUp")

    def test_password_change(self):
        # Access password change form
        response = self.client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 200)

        # Submit the new password
        response = self.client.post(reverse('password_change'), {
            'old_password': 'testpass123',
            'new_password1': 'newpass123',
            'new_password2': 'newpass123',
        })
        self.assertRedirects(response, reverse('password_change_done'))

        # Test that the new password works
        self.client.logout()
        login_success = self.client.login(email=self.user.email, password='newpass123')
        self.assertTrue(login_success, "Login with new password failed")


class ForcePasswordChangeTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com', 
            password='testpass123',
            force_change_password=True  # Force the user to change password
        )
        self.client.login(email=self.user.email, password='testpass123')

    def test_force_password_change(self):
        # Ensure the user is redirected to the password change page
        response = self.client.get(reverse('home'))
        ic(response)
        self.assertRedirects(response, reverse('password_change'))

        # Submit the new password
        response = self.client.post(reverse('password_change'), {
            'old_password': 'testpass123',
            'new_password1': 'newpass123',
            'new_password2': 'newpass123',
        })
        self.assertRedirects(response, reverse('password_change_done'))

        # Test that the new password works
        self.client.logout()
        login_success = self.client.login(email=self.user.email, password='newpass123')
        self.assertTrue(login_success)

        # Test that the force_change_password flag is reset
        self.user.refresh_from_db()
        self.assertFalse(self.user.force_change_password)

class PasswordResetTest(TestCase):
    
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(email='test@example.com', password='testpassword123')

    def test_password_reset_email(self):
        # Trigger password reset by submitting the email
        response = self.client.post(reverse('password_reset'), {'email': self.user.email})
        
        # Check if the form redirects correctly after submission
        self.assertEqual(response.status_code, 302)

        # Check if we were redirected to the password reset done page
        self.assertRedirects(response, reverse('password_reset_done'))

        # Check that one email was sent
        self.assertEqual(len(mail.outbox), 1)

        # Verify the email subject and recipient
        self.assertIn('Password reset', mail.outbox[0].subject)
        self.assertIn(self.user.email, mail.outbox[0].to)

    def test_password_reset_complete_flow(self):
        # Initiate password reset
        response = self.client.post(reverse('password_reset'), {'email': self.user.email})
        self.assertEqual(response.status_code, 302)

        # Check if redirected to password reset done page
        self.assertRedirects(response, reverse('password_reset_done'))

        # Get the token and uid from the email
        email = mail.outbox[0]
        url = [line for line in email.body.splitlines() if 'password/reset/' in line][0]

        # Extract uid and token from the URL
        uid, token = url.split('/')[-3], url.split('/')[-2]

        # Submit a valid new password
        response = self.client.get(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))
        self.assertEqual(response.status_code, 302)
        reset_url = response.url
        response = self.client.post(reset_url, {'new_password1': 'newsecurepassword123', 'new_password2': 'newsecurepassword123'})
        
        # # Check if the password reset was successful (redirect to 'password_reset_complete')
        self.assertRedirects(response, reverse('password_reset_complete'))

        # # Log in with the new password
        login = self.client.login(email=self.user.email, password='newsecurepassword123')
        self.assertTrue(login)


    def test_invalid_email(self):
            # Test when an invalid email is provided
            response = self.client.post(reverse('password_reset'), {'email': 'invalid@example.com'})
            self.assertEqual(response.status_code, 302)  # It should still redirect even for invalid email for security reasons
            
            # No email should be sent
            self.assertEqual(len(mail.outbox), 0)