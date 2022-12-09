from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
from django.test import TestCase

from bible.core.forms import SignInForm


class SignInGetTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('sign-in'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'sign_in.html')

    def test_html(self):
        contents = (
            ('type="email" name="email"', 1),
            ('type="password" name="password"', 1),
            ('<button type="submit"', 1),)

        for text, count in contents:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SignInForm)

    def test_csrf(self):
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_reset_password_link(self):
        self.assertContains(self.resp, 'href="/reset-password"')

    def test_sign_up_link(self):
        self.assertContains(self.resp, 'href="/sign-up"')


class SignInPostValidTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            username='thiago-assis',
            password='1234567890',
            email='thiago@assis.com')

        data = {'email': user.email, 'password': user.password}

        self.resp = self.client.post(r('sign-in'), data)

    # def test_post(self):
    #     """Valid POST should redirect to /home/"""
    #     self.assertRedirects(self.resp, r('home'))