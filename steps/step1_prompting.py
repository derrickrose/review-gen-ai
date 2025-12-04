from fastapi import APIRouter
from helpers import * 
import ai 
router = APIRouter()

def test_summarize():
    return check_ai('/summarize', 
             """Ducks are fascinating creatures known for their versatile habitats, ranging from freshwater lakes to coastal shorelines. These birds are admired for their vibrant plumage and distinctive quacking sounds. Ducks play a crucial role in their ecosystems by helping control insect and aquatic plant populations. They're also migratory, often traveling long distances between breeding and wintering grounds. Ducks' waterproof feathers and unique swimming ability make them adept at surviving in various environments. Their diet includes aquatic plants, small fish, and insects, showcasing their adaptability. In many cultures, ducks are symbols of freedom and grace, embodying the serene beauty of nature.""",
             """Is "{response}" is a valid summarization of this text: {text}.  Answer yes or no. Just single word""", 
             '^yes')

@router.get("/summarize")
async def summarize(text: str):
    return 'Write your code here'




def test_sentiment():
    return check('/sentiment', 'Kinda ok.', 'neutral') and \
           check('/sentiment', 'I\'m so glad. That awesome', 'positive') and \
           check('/sentiment', "Feeling terrible. It's awful", 'negative')

@router.get("/sentiment")
async def sentiment(text: str):
    return 'Write your code here'




def test_generate_code():
    return check('/generate_code', 'Write hello world in python', 'print(.*hello.*world.*)')

@router.get("/generate_code")
async def generate_code(text: str):
    return 'Write your code here'




def test_keypoints():
    return check_ai('/keypoints', 
             "Artificial intelligence is a branch of computer science that aims to create machines that can perform tasks that typically require human intelligence. This includes tasks like problem-solving, recognizing speech, translating languages, and more. AI systems are powered by algorithms, use deep learning and machine learning to process data, and can improve their performance over time as they acquire more data.",
             "Do the key points extracted from the text: {text} match the following summary: {response}? Answer yes or no. Just single word", 
             '^yes')

@router.get("/keypoints")
async def keypoints(text: str):
    return 'Write your code here'




def test_questions():
    return check_ai('/questions', 
             "What are the implications of quantum computing on current encryption methods? With the potential to process information at significantly faster rates, quantum computers could theoretically break many of the cryptographic algorithms that keep our digital communications secure. As a result, there is a growing need for quantum-resistant encryption methods that can withstand the processing power of quantum technology.",
             "Do the questions extracted from the text: {text} match the following: {response}? Answer yes or no. Just single word", 
             '^yes')

@router.get("/questions")
async def questions(text: str):
    return 'Write your code here'