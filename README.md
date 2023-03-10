OpenAPI Text Classifier Client
=============================

This is a Python client for the [OpenAI Text Classifier](https://platform.openai.com/ai-text-classifier). Here is a [live demo](https://openai-text-classifier-client.streamlit.app/).

Here's an example of how to use it:
1. You can get an OpenAI API key [here](https://platform.openai.com/account/api-keys).
2. Set the environment variable `OPENAI_API_KEY` to your OpenAI API key.
3. Run the following code:
```python
    api_key = os.getenv('OPENAI_API_KEY')
    classifier = OpenAiTextClassifier(api_key)
    score, category = classifier.detect(YOUR_TEXT)
```
