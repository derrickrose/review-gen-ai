from openai import OpenAI
import os
import requests
import re


# ---------------------------
# CLAUDE (legacy HF endpoint)
# ---------------------------
def claude(prompt='Say "test"'):
    from gradio_client import Client
    claude_client = Client("https://cohereforai-c4ai-command-r-plus.hf.space/--replicas/501wi/")
    return claude_client.predict(prompt, api_name="/generate_response")[0][1]


# ---------------------------
# BASIC OPENAI CALL
# ---------------------------
def openai(prompt, model="gpt-4o-mini", temperature=None):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    return response.choices[0].message.content


# ---------------------------
# OLLAMA LOCAL MODEL
# ---------------------------
def ollama(prompt, model='tinyllama'):
    response = requests.post(
        "http://ollama:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    ).json()

    if "response" in response:
        return response["response"]
    raise Exception(response)


# -------------------------------------------------------
# ⭐ REPLACEMENT FOR pezzo_openai() — Local Template Call
# -------------------------------------------------------
#
# Instead of pezzo.get_prompt(prompt_name), you now pass a dict
# e.g.:
#   prompt_template = {
#       "model": "gpt-4o-mini",
#       "messages": [
#           {"role": "system", "content": "You are a helper."},
#           {"role": "user", "content": "Hello {name}"}
#       ]
#   }
#
# Then call:
#   pezzo_openai(prompt_template, name="John")
#
def pezzo_openai(prompt_template, **variables):

    # Ensure prompt_template contains required fields
    model = prompt_template["model"]
    messages = prompt_template["messages"]

    # Replace {variables} inside prompt content
    rendered_messages = []
    for m in messages:
        rendered = re.sub(
            r'{(.*?)}',
            lambda x: variables.get(x.group(1), f"{{{x.group(1)}}}"),
            m["content"]
        )
        rendered_messages.append({**m, "content": rendered})

    # Call OpenAI normally (no Pezzo proxy)
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model=model,
        messages=rendered_messages
    )

    return response.choices[0].message.content


# ---------------------------
# EMBEDDINGS
# ---------------------------
def embeddings_openai(text, model='text-embedding-3-small'):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(
        model=model,
        input=[text]
    )
    return response.data[0].embedding
