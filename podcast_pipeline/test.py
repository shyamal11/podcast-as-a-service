import os
import json
import unittest
from unittest.mock import MagicMock
from pathlib import Path
from django.conf import settings
from .services.content_production import prepare_and_save_response_data  # Adjust this import
from .services.audio_production import text_to_speech  # Adjust this import
from .services.cover_production import generate_podcast_cover  # Adjust this import

# Test for prepare_and_save_response_data function
class PrepareAndSaveResponseDataTest(unittest.TestCase):
    
    def test_prepare_and_save_response_data(self):
        # Mock or real values for the inputs
        top_news_prompt = "Here are the top news stories:"
        top_news = ["Headline 1", "Headline 2", "Headline 3"]
        generate_script_prompt = "Generate podcast script for these news items:"
        script = "This is the raw podcast script."
        polished_script = "This is the polished version of the podcast script."
        podcast_title = "EP-46 : Openai's New Ciso & U.s. Ai Export Concerns 🔒💻, Tesla's Fsd Challenges 🚗, Amd & Intel's Unexpected Alliance 🤝"
        podcast_description = (
            "<p>welcome to echo-pod's tech briefing for wednesday, october 16th! "
            "join us as we explore today's significant developments in the tech world:</p>\n"
            "<ul>\n"
            "<li><strong>openai’s new ciso:</strong> former palantir chief information security officer dane stuckey steps in to enhance security and compliance at openai...</li>\n"
            "</ul>\n"
            "<p>tune in tomorrow for more updates from the ever-evolving landscape of technology!</p>"
        )
        podcast_cover = "path/to/podcast_cover_image.jpg"
        image_prompt = "AI generated cover image for the podcast."

        # Call the function
        response_data = prepare_and_save_response_data(
            top_news_prompt, top_news, generate_script_prompt,
            script, polished_script, podcast_title,
            podcast_description, podcast_cover, image_prompt
        )

       

        print("Response Data:", response_data)


# Test for text_to_speech function
class TextToSpeechRealTest(unittest.TestCase):

    def setUp(self):
        # Set up any necessary configurations before each test
        settings.AZURE_SPEECH_KEY = 'your_test_speech_key'  # Replace with your Azure Speech key
        settings.AZURE_REGION = 'your_test_region'  # Replace with your Azure region
        settings.OUTPUT_DIRECTORY = 'test_output_directory'  # Ensure this directory exists

        # Create the output directory if it doesn't exist
        if not os.path.exists(settings.OUTPUT_DIRECTORY):
            os.makedirs(settings.OUTPUT_DIRECTORY)

    def test_text_to_speech_real(self):
        # Dummy data for testing
        script = "This is a test script for the podcast."
        language = 'English'

        # Call the function
        final_podcast_path = text_to_speech(script, language)

        # Check if the final podcast path is created
        self.assertIsNotNone(final_podcast_path, "The final podcast path should not be None.")
        self.assertTrue(os.path.exists(final_podcast_path), "The final podcast file should exist.")

        # Print the output path for visibility
        print(f"Final podcast path: {final_podcast_path}")

    def tearDown(self):
        # Clean up any files or directories created during the test if needed
        if os.path.exists(settings.OUTPUT_DIRECTORY):
            for file in os.listdir(settings.OUTPUT_DIRECTORY):
                file_path = os.path.join(settings.OUTPUT_DIRECTORY, file)
                os.remove(file_path)
            os.rmdir(settings.OUTPUT_DIRECTORY)  # Remove the directory itself


# Test for podcast cover generation
class PodcastCoverGenerationTest(unittest.TestCase):

    def setUp(self):
        # Set up any necessary configurations before each test
        settings.OUTPUT_DIRECTORY = 'test_output_directory'  # Ensure this directory exists

        # Create the output directory if it doesn't exist
        if not os.path.exists(settings.OUTPUT_DIRECTORY):
            os.makedirs(settings.OUTPUT_DIRECTORY)

        # Mock the orchestrator
        self.orchestrator = MagicMock()
        self.orchestrator.ask_gpt.return_value = "A cohesive podcast cover image featuring..."  # Sample response from GPT
        self.orchestrator.openai_client.images.generate.return_value = MagicMock(data=[MagicMock(url='http://example.com/image.jpeg')])

    def test_generate_podcast_cover(self):
        # Dummy data for testing
        titles = "Title 1, Title 2, Title 3"

        # Call the function
        image_prompt, file_path = generate_podcast_cover(self.orchestrator, titles)

        # Check if the image prompt is returned
        self.assertIsNotNone(image_prompt, "The image prompt should not be None.")
        self.assertIn("A cohesive podcast cover image", image_prompt, "The image prompt should contain a description.")

        # Check if the file path is created
        self.assertTrue(os.path.exists(file_path), "The generated image file should exist.")
        print(f"Generated image saved at: {file_path}")

    def tearDown(self):
        # Clean up any files or directories created during the test if needed
        if os.path.exists(settings.OUTPUT_DIRECTORY):
            for file in os.listdir(settings.OUTPUT_DIRECTORY):
                file_path = os.path.join(settings.OUTPUT_DIRECTORY, file)
                os.remove(file_path)
            os.rmdir(settings.OUTPUT_DIRECTORY)  # Remove the directory itself


if __name__ == '__main__':
    # Run all tests
    unittest.main()
