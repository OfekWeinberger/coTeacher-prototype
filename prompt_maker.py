import openai
import os
from api_token import API_KEY

p = '''You are a chatbot answering a student's question, split your a answer into two parts, seperated by $$$.
return an answer formatted as markdown and math as mathjax.
try to keep answers short, to the point, and without some sort of intro.
make sure the two answers are clearly seperated, and if they are similar ommit the internet one.
The first part should be a based on the given summary of the lesson,
the second part should be an answer based on your own knowledge.'''

SYS_CONTENT = '''You are a chatbot answering a student's question.
you are going to be given a transcript of the lesson up to that point and a question.
please answer the question based on the context of the transcript, and keep it under 3 sentences.
dont include any intro, and format the math into mathjax and the answer in markdown.
the transcript will be {start in miliseconds},{end in miliseconds},{sentence}.'''

def send_prompt(prompt):
    client = openai.OpenAI(api_key=API_KEY)  # insert your actual API key here
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYS_CONTENT},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

