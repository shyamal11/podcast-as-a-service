
import os
from pathlib import Path
import azure.cognitiveservices.speech as speechsdk  # Make sure you have azure-cognitiveservices-speech installed
from pydub import AudioSegment  # Make sure you have pydub installed
from .utils import add_bgm  # Adjust the import according to the module where `add_bgm` is defined
from django.conf import settings


BGM_PATH = os.path.join(settings.BASE_DIR, 'assets', 'bgm.mp3')


def text_to_speech(script,  language='English'):
        
        try:

            speech_key = settings.AZURE_SPEECH_KEY  # Retrieve your speech key
            region = settings.AZURE_REGION  # Retrieve your region
            output_directory = settings.OUTPUT_DIRECTORY
            
            # Initialize the speech configuration and synthesizer within the method
            speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
            wav_file_path = str(Path(output_directory) / f"{language}.wav")
            audio_config = speechsdk.audio.AudioOutputConfig(filename=str(wav_file_path))
            speech_config.speech_synthesis_voice_name='en-US-AvaMultilingualNeural'
            speech_synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=speech_config,
                audio_config=audio_config
            )
            print(f"Starting Audio synthesis for the script in {language}...")


            result = speech_synthesizer.speak_text_async(script).get()

            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                mp3_file_path = str(Path(output_directory) / f"{language}.mp3")

                try:
                    audio = AudioSegment.from_wav(wav_file_path)
                    audio.export(mp3_file_path, format="mp3")

                    final_podcast_path = Path(output_directory) / f"{language}_final_podcast.mp3"
                
                    add_bgm(str(mp3_file_path), BGM_PATH, str(final_podcast_path))
                   
                    print(f"Podcast Audio successfully generated and saved at: {final_podcast_path}")

                except Exception as e:
                    print(f"An error occurred while handling files: {e}")
                    return None

                return final_podcast_path
            
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                print(f"Speech synthesis canceled: {cancellation_details.reason}")
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print(f"Error details: {cancellation_details.error_details}")
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        