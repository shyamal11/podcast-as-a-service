 
import os
import requests
import io
from PIL import Image  # Make sure you have the Pillow library installed
from datetime import date  # For handling today's date
from .utils import compress_image_to_target_size  # Adjust import according to where this function is defined
from django.conf import settings
import pytz
import datetime



pdt = pytz.timezone('America/New_York')
pdt_now = datetime.datetime.now(pdt)
today = pdt_now.date()
today_date = today.strftime('%Y-%m-%d')


def generate_podcast_cover( orchestrator, titles):
        
  
        output_directory = settings.OUTPUT_DIRECTORY
 
 
        file_path_hugging_face = os.path.join(output_directory, f"{today}generated_image.jpeg")

        print(f"Podcast Cover Art Generation Started...")
        
        gpt_prompt = f'''
        {titles}
        Use these news titles, generate a description of image formed if I'm using these three titles to create a cover image for a podcast episode. Create 1 coherent image instead of images separating talking about each title. I don't want any text in the image. 
        Only output the description.
        Example: 
        A cohesive podcast cover image featuring a nighttime scene of the Earth from space, with a focus on Indonesia illuminated by city lights. A sleek satellite in orbit, symbolizing Elon Musk's Starlink, beams a vibrant signal down to the Indonesian archipelago. In the foreground, a modern computer monitor with a holographic AI interface glows with dynamic data streams, representing Microsoft's AI integration. To the right, a stylish pair of wireless headphones from Sonos hovers, emitting colorful sound waves that blend into the background. The elements merge seamlessly, creating a unified, futuristic composition that highlights the innovation and connectivity of these tech advancements. 
        '''
        image_prompt = orchestrator.ask_gpt(
            input_ask=gpt_prompt,
        )

        try:

            API_URL = "https://api-inference.huggingface.co/models/XLabs-AI/flux-RealismLora"
            headers = {"Authorization": f"Bearer {os.getenv('HUGGING_FACE_API')}"}

          
            def query(payload):
                response = requests.post(API_URL, headers=headers, json=payload)
                response.raise_for_status()
                return response.content
            image_bytes = query({
                "inputs": image_prompt,
            })


            huggingface_model_image = Image.open(io.BytesIO(image_bytes))
            huggingface_model_image.save(file_path_hugging_face)
            print(f"image generated from hugging face model")
            compress_image_to_target_size(file_path_hugging_face, 1)

        
        except Exception as e:
            print(f"error generating image from hugging face model : {e}")


            try:

                response = orchestrator.openai_client.images.generate(
                    model="dall-e-3",
                    prompt=image_prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                
                image_url = response.data[0].url

                image_response = requests.get(image_url)
                image_response.raise_for_status() 
                
     
                with open(f'{output_directory}{today}generated_image.jpeg', 'wb') as file:
                        file.write(image_response.content)
                print(f"image generated from OpenAI model")

             
                compress_image_to_target_size(f'{output_directory}{today}generated_image.jpeg', 1)

                
             

            except Exception as e:
                print(f"Error generating image with OpenAI API: {e}")
                return None, None
            
        return image_prompt,file_path_hugging_face