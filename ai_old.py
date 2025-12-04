from openai import OpenAI
import os
import requests


# https://huggingface.co/spaces/CohereForAI/c4ai-command-r-plus
# API is deprecated don't use
def claude(prompt='Say "test"'):
    from gradio_client import Client
    claude_client = Client("https://cohereforai-c4ai-command-r-plus.hf.space/--replicas/501wi/")
    return claude_client.predict(prompt, api_name="/generate_response")[0][1]

def openai(prompt, model="gpt-3.5-turbo", temperature=None):
    openai_client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    chat_completion = openai_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
        temperature=temperature
    )
    return chat_completion.choices[0].message.content

def ollama(prompt, model='tinyllama'):
    response = requests.post(
        'http://ollama:11434/api/generate',
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    ).json()
    try:
        return response['response']
    except:
        raise Exception(response)

from pezzo.client import pezzo
import re

def pezzo_openai(prompt, **variables):
    #https://docs.pezzo.ai/introduction/tutorial-observability/overview
    # TODO: don't setup openai.base_url, and openai.default_headers
    # TODO: pass base_url and default_headers to OpenAI()
    #https://docs.pezzo.ai/introduction/tutorial-prompt-management/overview
    prompt = pezzo.get_prompt(prompt)
    openai_client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url='https://proxy.pezzo.ai/openai/v1',
        default_headers={
            "X-Pezzo-Api-Key": os.environ.get("PEZZO_API_KEY"),
            "X-Pezzo-Project-Id": os.environ.get("PEZZO_PROJECT_ID"),
            "X-Pezzo-Environment": "Production",
        },
    )
    chat_completion = openai_client.chat.completions.create(
        messages=[{**m, 'content': re.sub(r'{(.*?)}', lambda x: variables[x.group(1)], m['content'])} for m in prompt.content['messages']],
        model=prompt.settings['model'],
    )
    return chat_completion.choices[0].message.content

def embeddings_openai(text, model='text-embedding-3-small'):
    openai_client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    response = openai_client.embeddings.create(
        input=[text],
        model=model
    )
    return response.data[0].embedding
