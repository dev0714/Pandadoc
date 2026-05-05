import os
import time
import uuid
import sounddevice as sd
import soundfile as sf
import pygame
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

AUDIO_FILE = "question.wav"

def record_audio(seconds=6):
    print("Speak now...")

    audio = sd.rec(
        int(seconds * 44100),
        samplerate=44100,
        channels=1,
        dtype="float32"
    )

    sd.wait()
    sf.write(AUDIO_FILE, audio, 44100)

    print("Recording done.")

def transcribe_audio():
    with open(AUDIO_FILE, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=f
        )

    return transcript.text

def ask_gpt(question):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
You are a helpful voice assistant.
Answer clearly and briefly.

User asked:
{question}
"""
    )

    return response.output_text

def speak_answer(answer):
    reply_file = f"reply_{uuid.uuid4().hex}.mp3"

    try:
        pygame.mixer.quit()
    except:
        pass

    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=answer
    )

    with open(reply_file, "wb") as f:
        f.write(speech.read())

    pygame.mixer.init()
    pygame.mixer.music.load(reply_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.music.stop()
    pygame.mixer.quit()

    try:
        os.remove(reply_file)
    except:
        pass

def main():

    print("GPT Voice Assistant Started")
    print("Press ENTER to talk, or type q then ENTER to quit.")

    while True:
        command = input("\nPress ENTER to ask a question: ")

        if command.lower() == "q":
            print("Goodbye.")
            break

        record_audio(seconds=6)

        question = transcribe_audio()
        print(f"You asked: {question}")

        answer = ask_gpt(question)
        print(f"GPT: {answer}")

        speak_answer(answer)

if __name__ == "__main__":
    main()