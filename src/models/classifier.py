import os 
import configparser
from openai import OpenAI
from transformers import pipeline
from utils.constants import OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)

#LLM
def  classify_llm(review):
    if review:
        try:
            completion = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                                {
                                    "role": "user",
                                    "content": f"""Classify the following reviews into three classes: POSITIVE, NEGATIVE,NEUTRAL.
                                This is review: {review}"""
                                }
    ]
                    )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return "Error"
    return "Empty"


#use local model from Standford
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def classify_local(text):
    if not text:
        return None
    result = classifier(text, truncation=True)[0]
    label = result['label']
    return label

