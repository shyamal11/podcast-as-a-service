import os
import tempfile
from django.test import TestCase
from .views import upload_podcast_episode  # Adjust the import based on your app structure
from dotenv import load_dotenv


load_dotenv()

class PodcastUploadTests(TestCase):
    
    def test_upload_podcast_episode_with_dummy_data(self):
        # Create temporary files for the podcast episode and cover art
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as podcast_file, \
             tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as cover_file:

            podcast_file_name = podcast_file.name
            podcast_cover_art = cover_file.name

            # Write sample data to the podcast file
            podcast_file.write(b'This is a test podcast episode with dummy data.')
            podcast_file.close()  # Close the file so we can open it again later

            # Write sample data to the cover art file
            cover_file.write(b'This is a test cover art.')  # Placeholder data
            cover_file.close()  # Close the file so we can open it again later

        # Define parameters
        client_id = 'client_id'        # Replace with your actual client ID
        client_secret = 'client_secret' # Replace with your actual client secret
        title = 'Test Podcast Title'
        content = 'This is a test podcast episode with dummy data.'
        status = 'published'
        type_ = 'episode'
        episode_number = 1
        publish_timestamp = None

        # Call the function
        upload_podcast_episode(client_id, client_secret, podcast_file_name, podcast_cover_art,
                               title, content, status, type_,
                               episode_number, publish_timestamp)

        # Clean up temporary files
        os.remove(podcast_file_name)
        os.remove(podcast_cover_art)

        print("Test completed. Check Podbean for the uploaded episode.")
