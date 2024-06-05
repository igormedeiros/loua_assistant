import os
import pygame
from gtts import gTTS
from pydub import AudioSegment

def speak(text, speed=1.3):
    """Converts text to speech with a custom voice and speed control."""

    mp3_file = "temp_audio.mp3"
    try:
        # Generate the audio file using gTTS
        tts = gTTS(text=text, lang='pt', tld='com.br')
        tts.save(mp3_file)

        # Load the generated audio and adjust the speed
        sound = AudioSegment.from_mp3(mp3_file)
        faster_sound = sound.speedup(playback_speed=speed)
        faster_sound.export(mp3_file, format="mp3")

        # Play the audio with pygame
        pygame.mixer.init()
        pygame.mixer.music.load(mp3_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # Stop the music and quit the mixer
        pygame.mixer.music.stop()
        pygame.mixer.quit()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Remove the temporary audio file after playback is finished
        try:
            if os.path.exists(mp3_file):
                os.remove(mp3_file)
        except PermissionError:
            print(f"PermissionError: Could not remove {mp3_file}. The file is still in use.")
