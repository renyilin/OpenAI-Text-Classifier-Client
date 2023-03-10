import math
import os
import requests as requests

from text_examples import AI_TEXT, HUMAN_TEXT


class IncorrectApiKeyException(Exception):
    pass

class OpenAiTextClassifier:
    ai_generated_category = {
        'very unlikely': [0, 10],
        'unlikely': [10, 45],
        'unclear if it is': [45, 90],
        'possibly': [90, 98],
        'likely': [98, 100.01]
    }

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = 'https://api.openai.com/v1/completions'
        self.header = {
            'Accept': '*/*',
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }

    def detect(self, text: str) -> (float, str):
        payload = {
            'prompt': text + "\n<|disc_score|>",
            'max_tokens': 1,
            'temperature': 1,
            'top_p': 1,
            'n': 1,
            'logprobs': 5,
            'stop': '\n',
            'stream': False,
            'model': 'model-detect-v2',
        }

        response = requests.post(self.url, headers=self.header, json=payload)
        if response.status_code == 200:
            choices = response.json()['choices'][0]
            logprobs = choices['logprobs']['top_logprobs'][0]
            if '!' in logprobs:
                score = 100 - 100 * math.e ** logprobs['!']
            else:
                score = 100 * math.e ** logprobs['"']
            category = [key for key, score_range in self.ai_generated_category.items() if
                        score_range[0] <= score < score_range[1]][0]
            return score, category
        elif response.status_code == 401:
            raise IncorrectApiKeyException(response.json()['error']['message'])
        else:
            raise Exception(response.json()['error']['message'])

def main():
    api_key = os.getenv('OPENAI_API_KEY')
    classifier = OpenAiTextClassifier(api_key)
    score, category = classifier.detect(AI_TEXT)
    print(f"The OpenAI text classifier considers the text to be {category} AI-generated.({score:.2f}%)")
    score, category = classifier.detect(HUMAN_TEXT)
    print(f"The OpenAI text classifier considers the text to be {category} AI-generated.({score:.2f}%)")

if __name__ == '__main__':
    main()
