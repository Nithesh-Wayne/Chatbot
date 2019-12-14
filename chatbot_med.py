import numpy
import nltk
import numpy as np
import random
import string
import os
import pygame
from gtts import gTTS
from io import BytesIO

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

f = open('chatbot.txt','r',errors='ignore')

raw = f.read()

raw = raw.lower()

nltk.download('punkt')
nltk.download('wordnet')

sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

lemmer = nltk.stem.WordNetLemmatizer()

def speak(audioString):
    
##    tts = gTTS(text=audioString, lang='en')
##    tts.save("audio.mp3")
##    pygame.mixer.init()
##    pygame.mixer.music.load(audio.mp3)
##    pygame.mixer.music.play()
##    os.system("mpg321 audio.mp3")

##    mp3 = BytesIO()
##    tts = gTTS(text=audioString, lang='en')
##    tts.write_to_fp(mp3)
    tts = gTTS(text=audioString, lang='en')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    pygame.mixer.init()
    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict =  dict((ord(punct),None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_INPUTS1 = ("how are you")
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]
GREETING_RESPONSES1 = ["Fine","Superb","Excellent","pakka"]
def greeting(sentence):
 
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            a = random.choice(GREETING_RESPONSES)
            #speak(a)
            return a 
        elif word.lower() in GREETING_INPUTS1:
            a = random.choice(GREETING_RESPONSES1)
            #speak(a)
            return a

def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response

flag=True
print("Greetings from Nithesh. This is my Virtual Assistant you can connect me with it")
print("Hi, I am Alfred. How can I help you")

while(flag==True):
    user_response = input()
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            print("Alfred: You are welcome..")
            speak("Alfred: You are welcome..")
        else:
            if(greeting(user_response)!=None):
                a = greeting(user_response)
                print("Alfred: "+a)
                speak(a)
            else:
                print("Alfred: ",end="")
                a = response(user_response)
                print(a)
                speak(a)
                sent_tokens.remove(user_response)
    else:
        flag=False
        print("Alfred: Bye! take care..")
