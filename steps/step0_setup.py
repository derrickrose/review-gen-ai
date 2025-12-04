from sys import path

path.append("..")

from helpers import *

import os
os.environ.setdefault("PEZZO_API_KEY", "UNSET"),
os.environ.setdefault("PEZZO_PROJECT_ID", "UNSET"),
os.environ.setdefault("OPENAI_API_KEY", "UNSET")
os.environ.setdefault("HUGGING_FACE_API_KEY", "UNSET")

def test_hugging_face_key():
    api_key = os.environ.get("HUGGING_FACE_API_KEY")

    if api_key == "UNSET":
        return fail("HUGGING_FACE_API_KEY environment variable is not set properly. Visit: https://huggingface.co/settings/tokens")
    else:
        return ok("HUGGING_FACE_API_KEY environment variable is set properly")

def test_pezzo_keys():
    api_key = os.environ.get("PEZZO_API_KEY")
    project_id = os.environ.get("PEZZO_PROJECT_ID")

    if api_key == "UNSET" or project_id == "UNSET":
        return fail("PEZZO environment variables are not set properly. Visit: https://app.pezzo.ai/")
    else:
        return ok("PEZZO environment variables are set properly")

def test_openai_keys():
    openai_key = os.environ.get("OPENAI_API_KEY")
    if openai_key == "UNSET":
        return fail("OPENAI environment variable is not set properly.")
    else:
        return ok("OPENAI environment variable is set properly.")

def test_ollama_models():
    for model in ['mistral', 'tinyllama']:
        try:
            response = ai.ollama(prompt='Say "test"', model=model)
            if "test" not in response:
                return fail(f"Ollama model {model} is not working properly.")
        except Exception as e:
            return fail(f"Ollama model {model} encountered an error: {e}")
    return ok("Ollama models tinyllama, mistral are working properly.")