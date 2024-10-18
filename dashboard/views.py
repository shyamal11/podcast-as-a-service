from django.shortcuts import render
from django.http import JsonResponse
from news_sources.views import scrape_all_news  # Assuming this is the correct import
from podcast_pipeline.views import generate_podcast  # Assuming these exist
from upload_podcast.views import upload_podcast_episode
import os
import datetime
import logging

# Set up logging
logger = logging.getLogger(__name__)

def dashboard_view(request):
    response = render(request, 'podcast_dashboard.html')  # Render the HTML template
    return response

def generate_podcast_view(request):
   
    if request.method == 'POST':
        try:
            current_date = datetime.datetime.now().date() 
            print(f"Scraping news articles for date: {current_date}")
            news_articles = scrape_all_news(current_date)
            
            if not news_articles:
                logger.warning("No news articles scraped.")
                return JsonResponse({'error': 'No news scraped.'}, status=500)

            # Generate podcast content
            print("Generating podcast content.")
            podcast_content = generate_podcast(news_articles)

            if not podcast_content:
                logger.warning("Failed to generate podcast data.")
                return JsonResponse({'error': 'Failed to generate podcast data.'}, status=500)

            # Call the upload service
            print("Uploading podcast episode.")
            upload_status = upload_podcast_episode(podcast_content)

            if upload_status:
                logger.info("Podcast generated and uploaded successfully.")
                return JsonResponse({'success': 'Podcast generated and uploaded successfully.'})
            else:
                logger.warning("Podcast upload failed.")
                return JsonResponse({'error': 'Podcast upload failed.'}, status=500)

        except Exception as e:
            logger.error(f"Error generating podcast: {str(e)}")
            return JsonResponse({'error': 'An error occurred while generating the podcast.'}, status=500)
    else:
        logger.warning("Invalid request method.")
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
