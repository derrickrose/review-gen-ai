from fastapi import APIRouter
from helpers import * 
import ai 
router = APIRouter()

def test_classify_comment_positive():
    return check('/classify_comment', 'You are terrible person who hates dogs.', 'abusive')

def test_classify_comment_negative():
    return check('/classify_comment', 'I love dogs.', 'ok')

@router.get("/classify_comment")
def classify_comment_abusive(text: str):
    return 'Write your code here'




def test_filter_cat_mafia():
    comments = [
        ("Hey pals! Who's up for a tail-wagging contest at the park tomorrow? Can't wait to sniff everyone there.", 'ok'),
        ("Did anyone else bury their favorite toy and then forget where? Happened to me yesterday, digging all day!", 'ok'),
        ("I just chased the mailman again! It's my favorite part of the day. Anyone else feels the same thrill?", 'ok'),
        ("Greetings! Found a new scent on my walk today. Spent a good hour figuring it out. It was just some new flowers my human planted. LOL!", 'ok'),
        ("Can someone explain the appeal of catnip? My human got some for the neighbor's cat and I just don't get it. I’d rather have a good old tennis ball any day!", 'ok'),

        ("Hello friends! What's everyone's favorite sunspot in the house? I just love a good sunbath by the window.", 'cat'),
        ("Anyone else here enjoys climbing trees or getting on top of high shelves? It’s the best view!", 'cat'),
        ("Just curious, do you all take multiple short naps or one long one? I find several short naps during the day keeps me refreshed.", 'cat'),
        ("Has anyone tried those high-pitched noises to communicate? I find it works wonders with my humans.", 'cat'),
        ("I accidentally pushed a vase off the table today. It was quite exhilarating! Does anyone else have similar experiences?", 'cat')
    ]
    right_answers = 0
    uncertain = 0
    for comment, right_answer in comments:
        answer,request_ok = GET('/filter_cat_mafia', comment)
        if test('probably', answer):
            uncertain +=1
        if test(right_answer, answer):
            right_answers+=1
            ok(comment)
        else:
            fail(comment, f'\n{answer} != {right_answer}')

    if right_answer==10:
       ok(f'{right_answers}/10')

    return fail(f'''
Accuracy: {right_answers}/10
Uncertainty: {uncertain}/10''')





@router.get('/filter_cat_mafia')
def filter_cats(text: str):
    #TODO: try to improve accuracy
    return ai.openai(f"""We need to filter messages from cats. Return one of "cat", "ok", 'probably cat', 'probably ok'.

This is a message:
    {text}
    """)



