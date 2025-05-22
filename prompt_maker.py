import openai
import os
from api_token import API_KEY

def send_prompt(prompt):
    client = openai.OpenAI(api_key=API_KEY)  # insert your actual API key here
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a chatbot answering the student's question, split your a answer into two parts. The first part should be a based on the given summary of the lesson, the second part should be a answer based on your own knowledge. Please make sure to clearly separate the two parts. if the general knowledge part is very similar to the summary one, don't add it, return answer formatted as markdown."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Example usage
prompt = """Given this context, please provide an answer to this question. they are seperated by $$$. context: Our topic, our next topic, is the definite integral and I'm going to ask you to do the impossible and forget everything you know about snakes so far. You've 
never seen a snake before. And the reason is that what we're going to do now is going to seem at first completely but completely unrelated to indefinite integrals. And the only thing that's going to be similar is those snakes, the notation. And the reason 
for the notation is only going to be revealed later this week. Okay, so please forget everything you know about snakes, we're starting something completely different. And here we go. Our motivation, the question we're interested in now is the following. $$$ question: what is this lesson about?"""


result = send_prompt(prompt)
print(result)

