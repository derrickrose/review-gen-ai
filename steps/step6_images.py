from fastapi import APIRouter
import requests
from helpers import * 
import ai 
from fastapi import UploadFile, File

router = APIRouter()

from helpers import ok, fail

def recognize(image_path, expected_breed):
    with open(image_path, 'rb') as file:
        response = requests.post("http://server:8000/recognize_dog_breed", files={'file': (image_path, file, 'image/jpeg')})
        if response.status_code == 200:
            data = response.json()
            highest_matching_breed = None
            try:
                highest_matching_breed = data[0]['label']
            except:
                fail(data)
            if highest_matching_breed == expected_breed:
                return ok(highest_matching_breed)

            return fail(f"{image_path}. Expected breed: {expected_breed}, Detected breeds: {', '.join(pluck('label', data))}")
        else:
            return fail(f"{image_path}. Status code: {response.status_code}")

def test_recognize_poodle():
    return recognize('./images/poodle.jpeg', 'standard_poodle'),

def test_recognize_terrier():
    return recognize('./images/scottish-terrier.jpeg', 'scotch_terrier')



@router.post("/recognize_dog_breed")
async def recognize_dog_breed(file: UploadFile = File(...)):
    content = await file.read()
    return "Write your code here"
