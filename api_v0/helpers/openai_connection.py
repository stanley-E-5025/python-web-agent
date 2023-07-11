import sys, os
from pathlib import Path

tenant_directory, root_dir = (
    Path(__file__).resolve().parent.parent,
    Path(__file__).resolve().parent.parent.parent,
)
sys.path.insert(0, str(root_dir))
sys.path.append(str(tenant_directory))

from config import openai

def transcribe_audio(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    os.remove(audio_file_path) 
    return transcript


def generate_text(input_prompt):
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo-0613", messages=[{"role": "assistant", "content": input_prompt}])
    return response