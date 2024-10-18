from django.shortcuts import render
from django.http import JsonResponse
from .services.content_production import NewsPodcastOrchestrator, prepare_and_save_response_data
from .services.utils import  remove_leading_numbers # Ensure this import points to your orchestrator
from .services.audio_production import text_to_speech
from .services.cover_production import generate_podcast_cover
from .services.utils import  get_upload_date, english_title_case
import os
import datetime
import logging
import pytz
import sys
from django.conf import settings
import json
PRODUCTION_MODE=True


pdt = pytz.timezone('America/New_York')
pdt_now = datetime.datetime.now(pdt)
today = pdt_now.date()
today_date = today.strftime('%Y-%m-%d')


def generate_podcast(news_articles):
   
        try:

           
            
            _,_,_, publish_unix = get_upload_date(today_date)

            if len(sys.argv) > 1:
                episode_prefix = sys.argv[1]
                episode_number = f"EP-{episode_prefix} "
    
            else:
                raise ValueError("No additional argument provided.")

    
            orchestrator = NewsPodcastOrchestrator(today, news_articles)  # Add your actual news URLs here

            top_news_prompt, top_news = orchestrator.get_top_news()
            news_concat = orchestrator.get_news_content_concat(
                remove_leading_numbers(top_news))

          
            generate_script_prompt, script = orchestrator.generate_podcast_script(news_concat)

            polished_script = orchestrator.polish_podcast_script(script)
            podcast_description = orchestrator.generate_podcast_description(polished_script)
            podcast_title = episode_number + ": " +\
                    english_title_case(orchestrator.generate_podcast_title(polished_script))
                

            image_prompt, podcast_cover = generate_podcast_cover( orchestrator, podcast_title)

            if PRODUCTION_MODE:
                for language, cur_script in [('English', polished_script)]:
                        print(f"Generating podcast in {language}...")
                        audio_file_path = text_to_speech(
                            cur_script, language)
                        if audio_file_path:
                            logging.info(
                                f"Podcast in {language} completed successfully. Audio file at: {audio_file_path}")
                        else:
                            logging.error(f"Failed to generate {language} audio file.")

                
            response_data = prepare_and_save_response_data(top_news_prompt, top_news, generate_script_prompt, 
                          script, polished_script, podcast_title, 
                          podcast_description, podcast_cover, image_prompt)
            

            response_data['episode_prefix'] = episode_prefix
            response_data['publish_unix'] = publish_unix
                

                

            print(response_data)

            return response_data
         

        except Exception as e:
            logging.error(f"Error generating podcast: {str(e)}")
            return JsonResponse({'error': 'An error occurred while generating the podcast.'}, status=500)




