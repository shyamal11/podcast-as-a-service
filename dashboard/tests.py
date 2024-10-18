from django.test import TestCase
from django.urls import reverse
from django.http import HttpRequest
from .views import generate_podcast_view  # Adjust the import based on your project structure
import json
import sys

class GeneratePodcastViewTest(TestCase):
    def setUp(self):
        # Create a mock HTTP request
        self.request = HttpRequest()
        self.request.method = 'POST'  # You can set it to 'GET' if you want to test that as well

    def test_generate_podcast_with_argument(self):
        # Mock sys.argv for this test
        sys.argv = ['manage.py', '098']  # Replace '178' with your desired argument

        # Call the view function directly
        response = generate_podcast_view(self.request)

        # Check the status code of the response
        self.assertEqual(response.status_code, 200, f"Unexpected status code: {response.status_code}")

        # Parse the response data
        try:
            response_data = json.loads(response.content)
            print(f"Response Data: {response_data}")
        except json.JSONDecodeError:
            self.fail("Response is not valid JSON")

        # Add additional assertions based on the expected real output
        self.assertIn('success', response_data, "Podcast generation did not succeed.")

    def test_generate_podcast_without_argument(self):
        # Mock sys.argv for this test
        sys.argv = ['manage.py', 'test', 'dashboard']  # No argument provided

        # Call the view function directly
        response = generate_podcast_view(self.request)

        # Check the status code of the response
        self.assertEqual(response.status_code, 200, f"Unexpected status code: {response.status_code}")

        # Parse the response data
        try:
            response_data = json.loads(response.content)
            print(f"Response Data: {response_data}")
        except json.JSONDecodeError:
            self.fail("Response is not valid JSON")

        # Add additional assertions based on the expected real output
        self.assertIn('success', response_data, "Podcast generation did not succeed.")
