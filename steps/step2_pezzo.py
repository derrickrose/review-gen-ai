from fastapi import APIRouter
from helpers import * 
import ai 
router = APIRouter()
from pezzo.client import pezzo


def test_pezzo_settings():
    prompt = pezzo.get_prompt("Test")
    error_messages = []
    if prompt.settings['model'] != 'gpt-3.5-turbo-16k':
        error_messages.append("Expected model parameter in settings to be 'gpt-3.5-turbo-16k'.")
    if prompt.settings['top_p'] != .8:
        error_messages.append("Expected Top P parameter in settings to be 0.8.")
    if prompt.settings['max_tokens'] != 10:
        error_messages.append("Expected Max tokens parameter in settings to be 10.")
    if prompt.settings['temperature'] != 0:
        error_messages.append("Expected Temperature parameter in settings to be 0.")
    if prompt.settings['presence_penalty'] != 0.2:
        error_messages.append("Expected Presence penalty parameter in settings to be 0.2.")
    if prompt.settings['frequency_penalty'] != 1:
        error_messages.append("Expected Frequency penalty parameter in settings to be 1.")
    
    expected_messages = [
        {'role': 'system', 'content': 'Do not describe your answers. Answer in json.'},
        {'role': 'user', 'content': 'Answer "test".'}
    ]
    result_messages = prompt.content['messages']
    if result_messages != expected_messages:
        error_messages.append(f"Expected messages: {expected_messages}, but got: {result_messages}")
    
    if error_messages:
        map(fail, error_messages)
        return fail("Set settings in pezzo, commit, and publish!")
    
    return ok("All parameters in settings and content are as expected.")


def test_pezzo_test():
    return check_ai('/pezzo_test', '', 'Does {response} looks like {"answer":"test"}. Answer yes or no', 'yes')

@router.get("/pezzo_test")
async def pezzo_test(prompt='Test'):
    return ai.pezzo_openai(prompt)



def test_pezzo_variables():
    return check('/pezzo_variables?value=foobar', '', 'foobar')

@router.get("/pezzo_variables")
async def pezzo_test(prompt='Variables', value='unset'):
    return ai.pezzo_openai(prompt, value=value)