OpenAPI Text Classifier Client
=============================

This is a Python client for the [OpenAI Text Classifier](https://platform.openai.com/ai-text-classifier). Here is a [live demo](https://renyilin-openai-text-classifier-client-app-d3jmqb.streamlit.app/).

Here's an example of how to use it:
1. Set the environment variable `OPENAI_API_KEY` to your OpenAI API key.
2. Run the following code:
```python
    api_key = os.getenv('OPENAI_API_KEY')
    classifier = OpenAiTextClassifier(api_key)
    score, category = classifier.detect(YOUR_TEXT)
```
