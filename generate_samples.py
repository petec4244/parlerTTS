#!/usr/bin/env python3
import subprocess

male_speakers = ["Jon","Gary","Mike","Will","Patrick","Eric","Rick"]
female_speakers = ["Lea","Jenna","Laura","Lauren","Eileen","Alisa","Karen","Barbara","Carol","Emily","Rose","Anna","Tina"]

for speaker in male_speakers:
    desc = (f"{speaker} is a friendly, down-to-earth narrator in his mid-thirties "
            "with a relaxed, conversational American accent. He speaks at a steady, "
            "medium pace with a warm, approachable tone and just a hint of excitement. "
            "His voice feels close-up and personal, as though he's speaking directly "
            "to a friend. He enunciates clearly, but there is an informal and slightly "
            "playful quality to his words, making him sound relatable and genuine.")
    prompt = (f"Hello there! My name is {speaker}, and I am excited to meet you all. "
              "The quick brown fox jumps over the lazy dog at sunrise, setting the stage "
              "for a marvelous day. Would you like to join me for coffee at ten A M tomorrow?”")

    cmd = [
        "python", ".\\args_voice.py",
        "-m", "parler-tts/parler-tts-mini-v1",
        "-d", desc,
        "-p", prompt,
        "-o", f".\\{speaker}.wav",
        "-f", "default",
        "-v"
    ]
    subprocess.run(cmd, check=True)

for speaker in female_speakers:
    desc = (f"{speaker} is a friendly, down-to-earth narrator in her mid-thirties "
            "with a relaxed, conversational American accent. She speaks at a steady, "
            "medium pace with a warm, approachable tone and just a hint of excitement. "
            "Her voice feels close-up and personal, as though she's speaking directly "
            "to a friend. She enunciates clearly, but there is an informal and slightly "
            "playful quality to her words, making her sound relatable and genuine.")
    prompt = (f"Hello there! My name is {speaker}, and I am excited to meet you all. "
              "The quick brown fox jumps over the lazy dog at sunrise, setting the stage "
              "for a marvelous day. Would you like to join me for coffee at ten A M tomorrow?”")

    cmd = [
        "python", ".\\args_voice.py",
        "-m", "parler-tts/parler-tts-mini-v1",
        "-d", desc,
        "-p", prompt,
        "-o", f".\\{speaker}.wav",
        "-f", "default",
        "-v"
    ]
    subprocess.run(cmd, check=True)
