import os
from email.mime.text import MIMEText
from textwrap import dedent

import openai
import pandas as pd
from mail import send_email

MODEL = "gpt-3.5-turbo"
openai.api_key = os.environ.get("API_KEY")


def chat_with_chatgpt(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.2,
    )

    message = response["choices"][0]["message"]["content"]
    return dedent(message)


def main():
    df = pd.read_csv("data/quizlet.csv")

    template = """
    You helping me to learn German by providing one example sentence (A1/A2 level),
    along with the English translation with each of the given words: {word1}, {word2}, {word3}, {word4}, {word5}.

    Don't say anything else except the example sentences. The format should be:
    1. sentence 1 (translation 1)
    2. sentence 2 (translation 2)
    3. sentence 3 (translation 3)
    4. sentence 4 (translation 4)
    5. sentence 5 (translation 5)
    """

    examples = df.sample(n=5).values
    word1, word2, word3, word4, word5 = examples[:, 0]
    translation1, translation2, translation3, translation4, translation5 = examples[:, 1]
    prompt = template.format(word1=word1, word2=word2, word3=word3, word4=word4, word5=word5)

    response = chat_with_chatgpt(prompt, model=MODEL)
    response = str.split(response, "\n")
    example1, example2, example3, example4, example5 = response

    body = dedent(
        f"""
    Guetn Tag! I am wurstGPT, here are your daily german words:

    1. {word1} - {translation1}
    2. {word2} - {translation2}
    3. {word3} - {translation3}
    4. {word4} - {translation4}
    5. {word5} - {translation5}

    Example sentences:
    {example1}
    {example2}
    {example3}
    {example4}
    {example5}

    Tschüss!
    """
    )

    email = os.environ.get("EMAIL")
    pwd = os.environ.get("EMAIL_PASSWORD")
    send_email(user=email, pwd=pwd, recipient=email, subject="WurstGPT", body=body)


if __name__ == "__main__":
    main()


# TODO: set up cron job as a GitHub action
# TODO: set up cron job as a GitHub action
