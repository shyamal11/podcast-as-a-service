import os
import logging
import time
import difflib
from typing import List, Tuple
import openai
import re
from newsplease import NewsPlease
from news_sources.views import scrape_and_group_by_source   # Adjust the import based on your project structure
from news_sources.views import format_grouped_titles_by_source
from .utils import get_upload_date, trim_string_with_ellipsis
from django.conf import settings
import json
import pytz
import datetime


MAX_RETRIES = 1
RETRY_DELAY = 2  # seconds in case of retries
TEXT_MODEL = "gpt-4o-mini"

pdt = pytz.timezone('America/New_York')
pdt_now = datetime.datetime.now(pdt)
today = pdt_now.date()


class NewsPodcastOrchestrator:
    

    def __init__(self, date, news_articles):
      
        self.openai_client = openai.OpenAI(
            api_key = os.environ.get("OPENAI_API_KEY"),
            organization = os.getenv('OPENAI_ORGANIZATION_ID')
        )
        self.date = date
        self.news_articles = news_articles
        self.speech_key = os.environ.get("SPEECH_KEY")
        self.region = os.environ.get("SPEECH_REGION")

    def ask_gpt(self, input_ask, role="system"):
       
        attempts = 0
        while attempts < MAX_RETRIES:
            try:
                completion = self.openai_client.chat.completions.create(
                    model=TEXT_MODEL,
                    messages=[{"role": "system", "content": role},
                              {"role": "user", "content": input_ask}]
                )
                response = completion.choices[0].message.content
                if isinstance(response, str):
                    return response.lower().strip().strip('.')
            except Exception as e:
                logging.error(f"Error in ask_gpt: {e}. Retrying...")
                time.sleep(RETRY_DELAY)
                attempts += 1
        return None

    def translate_text(self, text, target_language):
       
        prompt = f"Translate the English part of the text to {target_language}. Do not translate word by word; Do Translation naturally:\n\n{text}\n Translation:"
        translation = self.ask_gpt(prompt)
        return translation

    def get_top_news(self):

        print(f"Getting top News from get_top_news function")
       
        grouped_sources = scrape_and_group_by_source(self.date)
        formatted_text = format_grouped_titles_by_source(grouped_sources)

       
        input_ask = '''Suppose you are the chief editor at CNBC-TechCheck-Briefing. You need to select 5 most important news events to put into today's briefing(You might be able to see some hint by how many times a news event is reported, but also consider what your audience of CNBC-TechCheck-Briefing is interested in). Return the title of the event in order of importance for these unqiue events.
            Here are the news of today:\n''' + formatted_text
        role = "Output the response as string titles in the seperated by newline. Each title should be exactly how it is in the news source."
        

        #output = top_news(input_ask)
        output = self.ask_gpt(input_ask, role)
        return input_ask, output.split('\n') if output else []

    def generate_podcast_script(self, news_concat, language=None):

        print(f"generating Podcast Script")
        
        output_response_prompt = ""
        if language:
            output_response_prompt = f"Output the response in {language}."
        first_shot = """
        Prompt: Give a quick tech news update script in the style of CNBC techcheck briefing as an example.
        Response: I'm Echo-Pod, and this is your CNBC techcheck Briefing for Monday April 29th. Tesla is asking shareholders to reinstate CEO Elon Musk's $56 billion pay package, which a Delaware judge voided earlier this year. The judge ruled that the record-setting compensation deal was, quote, deeply flawed. Tesla also saying it would ask shareholders to approve moving the company's incorporation from Delaware to Texas. The company has hired a proxy solicitor and plans to spend millions of dollars to help secure votes for the two proposals. Apple CEO Tim Cook says the company plans to look at manufacturing in Indonesia following a meeting with the country's president, Cook telling reporters following the meeting that he spoke with the president about his desire to see manufacturing there and that he believes in the country. The comments come as Apple is pushed to diversify its supply chain with more manufacturing outside of China in countries such as Vietnam and India. Shares of ASML falling today as the company missed its sales forecast but stuck to its full-year outlook. Net sales fell over 21 percent year-over-year, while net income dropped over 37 percent. ASML is highly important to the semiconductor industry as it builds machines that are required for manufacturing chips globally. Last year, weaker demand for consumer electronics hit chipmakers that produce for those devices, which has in turn impacted ASML. That's all for today. We'll see you back here tomorrow.
        """

        month, day, day_of_week, _ = get_upload_date(self.date.strftime('%Y-%m-%d')) 
        intro_date = day_of_week + " " + month + " " + str(day)

        prompt = f"Prompt: Give a quick tech news update script in the style of CNBC techcheck briefing using the following news titles and content. Closely follow how CNBC techcheck chooses context to put into the script, the langauge style and sentence structure. Use the same beginning and ending(including mentioning host echo-pod and {intro_date}), and replace CNBC techcheck briefing to 'AI briefing' \n {news_concat}\n" + \
            output_response_prompt + "\n"
        response_begin = "Response:"
        input_ask = first_shot + prompt + response_begin

        return input_ask, self.ask_gpt(input_ask)
    


    def get_news_content_concat(self, top_news):
        news_concat = []
        for i, news in enumerate(top_news):
            if news not in self.news_articles:
                # Search for news in the dictionary keys
                possible_news = difflib.get_close_matches(
                    news, self.news_articles.keys())

                # If a close match is found, use the full string as the key
                if possible_news:
                    news = possible_news[0]
                else:
                    logging.warning(
                        f"News '{news}' not found in the available news sources. Skipping")
                    continue
                logging.warning(
                    f"News '{news}' not found in the available news sources. Skipping")
                continue

            curr_news = NewsPlease.from_url(self.news_articles[news])
            news_concat.append("title" + str(i) + ":\n" + curr_news.title +
                               "\n" + "description" + str(i) + ":\n" + curr_news.maintext)

        news_concat = '"' + "\n\n".join(news_concat) + '"'
        return news_concat

    def polish_podcast_script(self, script):

        print(f"Processing the script")
        
        month, day, day_of_week, _ = get_upload_date(self.date.strftime('%Y-%m-%d')) 
        intro_date = day_of_week + " " + month + " " + str(day)

       
        input_ask = script + f"""
        This is not up to standards with the style of 'CNBC techcheck', here is a example. Carefully inspect the language style, sentence structure, use of words and order of words in sentences of the following examples of 'CNBC techcheck'. Start the podcast with "i'm Echo-Pod, welcoming you to today's tech briefing for {intro_date}.:
example 1:
"I'm Julia Boorstin, and this is your tech Briefing for Monday April 29th. Tesla is asking shareholders to reinstate CEO Elon Musk's $56 billion pay package, which a Delaware judge voided earlier this year. The judge ruled that the record-setting compensation deal was, quote, deeply flawed. Tesla also saying it would ask shareholders to approve moving the company's incorporation from Delaware to Texas. The company has hired a proxy solicitor and plans to spend millions of dollars to help secure votes for the two proposals. Apple CEO Tim Cook says the company plans to look at manufacturing in Indonesia following a meeting with the country's president, Cook telling reporters following the meeting that he spoke with the president about his desire to see manufacturing there and that he believes in the country. The comments come as Apple is pushed to diversify its supply chain with more manufacturing outside of China in countries such as Vietnam and India. Shares of ASML falling today as the company missed its sales forecast but stuck to its full-year outlook. Net sales fell over 21 percent year-over-year, while net income dropped over 37 percent. ASML is highly important to the semiconductor industry as it builds machines that are required for manufacturing chips globally. Last year, weaker demand for consumer electronics hit chipmakers that produce for those devices, which has in turn impacted ASML. That's all for today. We'll see you back here tomorrow."
example 2:
"I'm Steve Kovach, and this is your tech Briefing for Tuesday March 23rd. AMD revealing today its latest AI chips. The new chips will be for so-called AI PCs, or PCs with special processors, for tasks like real-time language translation, or using tools like Microsoft's Copilot Assistant more efficiently. Last month, Intel put its latest AI PC chip in Microsoft's new Surface computer lineup, and Qualcomm is expected to put its chips in PCs starting next month. Sticking with AI, Microsoft announcing today a $1.5 billion investment in G42, a startup based in the United Arab Emirates. As part of the deal, G42 will use Microsoft's Azure Cloud to run its AI applications, and Microsoft President Brad Smith will join the company's board. Microsoft has made several foreign AI and cloud investments so far this year. Some examples include the company said it would open a headquarters in London, invest in the French startup Mistral, and invest $2.9 billion in AI infrastructure in Japan. Now over to China. Baidu, the Chinese search company, announced its AI chatbot ErnieBot has surpassed 200 million users. ErnieBot launched last year, and other companies like Samsung and Honor have integrated Ernie into their devices. Apple is reportedly going to partner with Baidu as well to help power new AI features in devices sold in China. That's all from today. We'll see you back here tomorrow."
Make my original podcast script more like the examples above to an extend that it is similar in style, language, sentence structure, and use of words and so closely resembled so that no one can tell the difference between the style.
refined podcast script:
"""
        role = "Output the polished script."
        polished_script = self.ask_gpt(input_ask, role)
        return polished_script

    def generate_podcast_description(self, script, language=None):
        print(f"Generating  Podcast Description ")

        output_response_prompt = ""
        if language:
            output_response_prompt = f"Output the Description in {language}."

        input_ask = f"""
            Generate a description for this podcast. Summarize topics discussed. This will be the script we use for the podcast description on Apple Podcast. So please be concise, use bullet point when possible. Please only output html without the root element, nothing else.
            
            Example:
            <p>welcome to echo-pod's tech briefing for monday, may 20th! dive into today's top tech stories:</p>
            <ul>
            <li><strong>microsoft build conference highlights:</strong> introduction of copilot+ pcs with dedicated npus for enhanced ai experiences, revamped surface devices with impressive battery life and new display technology.</li>
            <li><strong>surface refresh:</strong> new surface laptop with up to 22 hours of battery life and wi-fi 7, plus a surface pro featuring an oled hdr display and optional 5g connectivity.</li>
            <li><strong>scarlett johansson & chatgpt controversy:</strong> actress scarlett johansson reveals unsettling similarities between her voice and openai’s new ai voice feature "sky," sparking a legal inquiry.</li>
            <li><strong>qualcomm’s snapdragon x elite processors:</strong> launch of new pcs equipped with these ai-driven processors focused on energy efficiency and enhanced ai performance.</li>
            <li><strong>seekout layoffs:</strong> the recruiting startup lays off 30% of its workforce amid financial challenges, marking its second round of layoffs in less than a year.</li>
            <li><strong>google engage sdk:</strong> announced at google i/o 2024, this feature aims to increase user engagement by allowing developers to highlight content and deals within installed apps.</li>
            </ul>

            <p>stay tuned for tomorrow's tech updates!</p>
            
            Here's the podcast script:
            "
            {script}
            "
            {output_response_prompt}
            Description:
            """

        return self.ask_gpt(input_ask)
    


    def generate_podcast_title(self, transcript, language=None):
            print(f"Generating  Podcast Title ")
            output_response_prompt = ""
            if language:
                output_response_prompt = f"Output the Title in {language}."
            input_ask = "Generate a title for this podcast. Must include three key topics (if there are many, choose the three most important ones). Incorporate emojis where appropriate. Pay attention to capitalization of titles. Follow the style of titles such as: Tesla Showcases FSD Demo 🚗, Adam Neuman's WeWork Bid 💰, CSV Conundrums 🖥️,Anthropic’s $4B Amazon Boost 💰, Brex's Valuation Leap to $12B 💳, Strategies for Success ✨,The OpenAI Voice Revolution 🗣️, AI Safety Measures 🦺, LLMs Go Mobile 📱. Here's the transcript excerpt: " + transcript + "\n" + output_response_prompt + "\nTitle:"
            return self.ask_gpt(input_ask)
    

def prepare_and_save_response_data (top_news_prompt, top_news, generate_script_prompt, 
                          script, polished_script, podcast_title, 
                          podcast_description, podcast_cover, image_prompt):
        
        print(f"Saving  Podcast Data")
        
        output_directory = settings.OUTPUT_DIRECTORY  # Ensure this is set correctly in your settings
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        output_file_path =  os.path.join(output_directory, 'podcast_data.json')
        file_path = os.path.join(output_directory, 'English_final_podcast.mp3') 
        trimmed_description = trim_string_with_ellipsis(podcast_description)
        
        output_data = {
            "top_news_prompt": top_news_prompt,
            "Top News": top_news,
            "Generate_script_prompt": generate_script_prompt,
            "Script": script,
            "Polished Script": polished_script,
            "Podcast Title": podcast_title,
            "Podcast Description": podcast_description,
            "Image Prompt": image_prompt,
              "Podcast Cover":podcast_cover,
              "File Path":file_path,
              "Trimmed Description" : trimmed_description,
        }
         
        

        with open(output_file_path, 'w') as file:
                json.dump(output_data, file, indent=4)


        return  output_data



    



