import requests
import re
from ramda import *
import ai

def fail(message, explanation=''):
    print(f"\033[91mFAIL \033[0m{message} {explanation}\n")
    return 'FAIL'

def ok(message):
    print(f"\033[92mOK\033[0m {message}\n")
    return "OK"

def yellow(message):
    return f"\033[93m{message}\t\033[0m"

def green(message):
    return f"\033[92m{message}\t\033[0m"
def red(message):
    return f"\033[91m{message}\t\033[0m"

def check_server_response():
    try:
        response = requests.get('http://server:8000')
        if not response.status_code == 200:
            fail("Server responded with unexpected status code", str(response.status_code))
    except requests.exceptions.RequestException as e:
        fail("Server request failed", str(e))

def GET(endpoint, query):
    try:
        response = requests.get(f'http://server:8000{endpoint}', params={'text': query})
        if response.ok:
            return response.text, response.ok
        else:
            return f'Failed response: {endpoint}', False
    except requests.exceptions.RequestException as e:
            return f'Failed response: {endpoint}', False
    
def match_regex(text, regex):
    pattern = re.compile(regex, re.IGNORECASE | re.MULTILINE | re.DOTALL)
    return re.search(pattern, text)

def check_ai(endpoint, text, question, regex):
    response, ok_ = GET(endpoint, text)

    question = replace('{text}', '\n'+text+'\n', replace('{response}', '\n'+response+'\n', question))
    aianswer = ai.openai(question)
    
    ok_ = ok_ and match_regex(aianswer, regex)
    message  = "\n\t\t".join([
        endpoint, 
        f"{yellow('QUERY')}{text}", 
        f"{yellow('ANSWER')}{response}", 
        f"{yellow('AICHECK QUERY')}{question}\n",
        f"{yellow('AICHECK')}{aianswer}",
        f"{green('OK')}/{regex}/" if ok else f"{red('FAIL')}/{regex}/"
    ])
    return ok(message) if ok_ else fail(message)


def check(endpoint, text, regex):
    response, ok_ = GET(endpoint, text)

    ok_ = ok_ and match_regex(response, regex)

    message  = "\n\t\t".join([
        endpoint, 
        f"{yellow('QUERY')}{text}", 
        f"{yellow('ANSWER')}{response}", 
        f"{green('OK')}/{regex}/" if ok_ else f"{red('FAIL')}/{regex}/"
    ])
    return ok(message) if ok_ else fail(message)

import os
import importlib

def find_steps():
    steps_path = os.path.join(os.path.dirname(__file__), 'steps')
    for module_name in sorted(os.listdir(steps_path)):
        if module_name.endswith('.py') and module_name != '__init__.py':
            module_name = module_name[:-3]  # Remove .py extension
            module = importlib.import_module(f'steps.{module_name}')
            yield module, module_name