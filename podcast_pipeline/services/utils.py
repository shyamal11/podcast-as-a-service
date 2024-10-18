from datetime import datetime
from datetime import datetime, timedelta
import pytz
from PIL import Image
import os
from pydub import AudioSegment
import re


def get_day_of_week(date):
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    # Get the day of the week as an integer (0=Monday, 6=Sunday)
    day_of_week_number = date_obj.weekday()
    
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_of_week_name = days_of_week[day_of_week_number]
    months_of_year = ["January", "February", "March", "April", "May", "June", 
                      "July", "August", "September", "October", "November", "December"]
    month_name = months_of_year[date_obj.month - 1]

    # Return the month, date, and day of the week in a tuple
    return [month_name, date_obj.day, day_of_week_name]

def get_next_day(date):
    # Convert the date string to a datetime object
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    # Calculate the next day
    next_day = date_obj + timedelta(days=1)
    
    # Return the next day as a string in the format 'YYYY-MM-DD'
    return next_day.strftime('%Y-%m-%d')

def get_upload_date(date):
    pst = pytz.timezone('America/New_York')
    publish_day_str = get_next_day(date)
    publish_day = datetime.strptime(publish_day_str, '%Y-%m-%d')
    # Set the time to 5 AM PST
    upload_datetime = publish_day.replace(hour=5, minute=0, second=0, microsecond=0)
    
    # Localize to PST
    upload_datetime_pst = pst.localize(upload_datetime)
    
    # Convert to Unix timestamp
    unix_time = int(upload_datetime_pst.timestamp())
    month_name, day, day_of_week_name = get_day_of_week(upload_datetime_pst.strftime('%Y-%m-%d'))
    
    return month_name, day, day_of_week_name, unix_time

def spanish_title_case(text):
    # Words to keep in lowercase unless they are the first word
    lowercase_words = ['de', 'a', 'en', 'y', 'o', 'u', 'del', 'la', 'los', 'las', 'el', 'un', 'una', 'unos', 'unas']
    words = text.split()
    new_title = []
    for i, word in enumerate(words):
        if word.lower() in lowercase_words and i != 0:
            new_title.append(word.lower())
        else:
            new_title.append(word.capitalize())
    return ' '.join(new_title)

def english_title_case(text):
    # Words to keep in lowercase unless they are the first word
    lowercase_words = ['a', 'an', 'the', 'and', 'or', 'but', 'nor', 'at', 'by', 'for', 'from', 'in', 'into', 'near', 'of', 'on', 'onto', 'to', 'with']
    words = text.split()
    new_title = []
    for i, word in enumerate(words):
        if word.lower() in lowercase_words and i != 0:
            new_title.append(word.lower())
        else:
            new_title.append(word.capitalize())
    return ' '.join(new_title)


def compress_image_to_target_size(input_path, target_size_mb, initial_quality=85, step=5):
    """
    Compresses an image to ensure its size is below a target size in MB, overwriting the original image.

    :param input_path: Path to the input image.
    :param target_size_mb: Target size in MB.
    :param initial_quality: Initial quality for compression.
    :param step: Step to reduce quality in each iteration.
    """
    target_size_bytes = target_size_mb * 1024 * 1024
    quality = initial_quality

    with Image.open(input_path) as img:
        while True:
            img.save(input_path, 'JPEG', quality=quality)
            output_size = os.path.getsize(input_path)
            
            if output_size <= target_size_bytes or quality <= step:
                break

            quality -= step
            if quality <= 0:
                raise ValueError("Cannot compress image to the desired size.")
            

def trim_string_with_ellipsis(text, max_length=497):

    if len(text) > max_length:
        return text[:max_length - 3] + '...'  
    else:
        return text
    

def add_bgm(podcast_path, bgm_path, final_path):
    # Load the podcast and BGM
    podcast = AudioSegment.from_file(podcast_path)
    bgm = AudioSegment.from_file(bgm_path)

    # Extract intro (first 3 seconds), middle, and outro (last 10 seconds) of BGM
    bgm_intro = bgm[:3000] 
    bgm_outro = bgm[-13000:-5000]
    bgm_middle = bgm[3000:-13000] 

    bgm_intro = bgm_intro - 15 
    bgm_outro = bgm_outro - 18
    bgm_middle = bgm_middle - 22

    # Calculate required length for the middle BGM to loop
    middle_duration = len(podcast) - len(bgm_intro) - 1000

    # Loop the middle part of the BGM to cover the podcast duration
    bgm_middle_loop = bgm_middle * (middle_duration // len(bgm_middle) + 1)
    bgm_middle_loop = bgm_middle_loop[:middle_duration]  # Trim to exact duration

    # Combine intro, looped middle, and outro of BGM
    bgm_full = bgm_intro + bgm_middle_loop + bgm_outro

    final_mix = bgm_full.overlay(podcast, position=len(bgm_intro))
    final_mix.export(final_path, format="mp3")


def remove_leading_numbers(lst):
    # This regular expression matches any leading numbers followed by a dot and any amount of whitespace
        pattern = re.compile(r'^\d+\.\s*')
        # This will apply the regex substitution to each string in the list
        return [pattern.sub('', s.strip()) for s in lst]



def english_title_case(text):
    # Words to keep in lowercase unless they are the first word
    lowercase_words = ['a', 'an', 'the', 'and', 'or', 'but', 'nor', 'at', 'by', 'for', 'from', 'in', 'into', 'near', 'of', 'on', 'onto', 'to', 'with']
    words = text.split()
    new_title = []
    for i, word in enumerate(words):
        if word.lower() in lowercase_words and i != 0:
            new_title.append(word.lower())
        else:
            new_title.append(word.capitalize())
    return ' '.join(new_title)






