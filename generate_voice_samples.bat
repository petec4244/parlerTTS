@echo off
REM Batch script to generate TTS samples for multiple speakers.

REM ~~~ Male speakers ~~~
for %%S in (Jon Gary Mike Will Patrick Eric Rick) do (
    echo Generating TTS for male speaker: %%S
    python .\args_voice.py ^
        -m parler-tts/parler-tts-mini-v1 ^
        -d "%%S is a friendly, down-to-earth narrator in his mid-thirties with a relaxed, conversational American accent. He speaks at a steady, medium pace with a warm, approachable tone and just a hint of excitement. His voice feels close-up and personal, as though he is speaking directly to a friend. He enunciates clearly, but there's an informal and slightly playful quality to his words, making him sound relatable and genuine." ^
        -p "Hello there! My name is %%S, and I am excited to meet you all. The quick brown fox jumps over the lazy dog at sunrise, setting the stage for a marvelous day. Would you like to join me for coffee at ten A M tomorrow?" ^
        -o ".\%%S.wav" ^
        -f default ^
        -v
)

REM ~~~ Female speakers ~~~
for %%S in (Lea Jenna Laura Lauren Eileen Alisa Karen Barbara Carol Emily Rose Anna Tina) do (
    echo Generating TTS for female speaker: %%S
    python .\args_voice.py ^
        -m parler-tts/parler-tts-mini-v1 ^
        -d "%%S is a friendly, down-to-earth narrator in her mid-thirties with a relaxed, conversational American accent. She speaks at a steady, medium pace with a warm, approachable tone and just a hint of excitement. Her voice feels close-up and personal, as though she is speaking directly to a friend. She enunciates clearly, but there's an informal and slightly playful quality to her words, making her sound relatable and genuine." ^
        -p "Hello there! My name is %%S, and I am excited to meet you all. The quick brown fox jumps over the lazy dog at sunrise, setting the stage for a marvelous day. Would you like to join me for coffee at ten A M tomorrow?" ^
        -o ".\%%S.wav" ^
        -f default ^
        -v
)
