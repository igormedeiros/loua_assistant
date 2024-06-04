from gtts import gTTS
from pydub import AudioSegment
import pygame

def speak(text, speed=1.3):
    """Converts text to speech with a custom voice and speed control."""

    mp3_file = "temp_audio.mp3"
    # Load the custom voice pack (replace with the path of your file)
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