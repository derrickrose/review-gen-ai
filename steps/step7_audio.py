from helpers import * 
from datasets import load_dataset
from transformers import pipeline
from ramda import *

def test_emotion():
    dataset = load_dataset("ashraq/esc50").filter(lambda example: example["category"].startswith("dog"))

    def get_by_filename(filename):
        return find(prop_eq('filename', filename), dataset['train'])

    # TODO: define your labels
    aggressive = ''
    cheerful = ''
    other = ''
    # TODO
 
    audio_classifier = pipeline(task="zero-shot-audio-classification", model="laion/clap-htsat-unfused")

    samples = [
        ('5-231762-A-0.wav', aggressive),
        ('1-30226-A-0.wav', cheerful),
        ('1-110389-A-0.wav', aggressive),
        ('1-100032-A-0.wav', cheerful)
    ]

    right = 0
    for file, right_label in samples:
        audio = get_by_filename(file)

        scores = audio_classifier(audio['audio']['array'], candidate_labels=[aggressive, cheerful, other])

        label = head(scores)['label']
        if label == right_label:
            right+=1
            ok(f'{audio["filename"]} {label}')
        else:
            fail(f'{audio["filename"]} {label} != {right_label}')

    if right == len(samples):
        return ok(f'Accuracy {right}/{len(samples)}')
    else:
        return fail(f'Accuracy {right}/{len(samples)}')