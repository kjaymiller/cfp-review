from django.test import TestCase
from django.urls import reverse


class HomePageTests(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_page_contains_correct_html(self):
        response = self.client.get("/")
        self.assertContains(response, "The Green Room for the World Stage")
        self.assertContains(response, "Start Your Journey")
