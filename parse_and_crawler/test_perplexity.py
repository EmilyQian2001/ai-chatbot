from openai import OpenAI

YOUR_API_KEY = "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"

messages = [
    {
        "role": "system",
        "content": (
            "You are an artificial intelligence assistant and you need to "
            "engage in a helpful, detailed, polite conversation with a user."
        ),
    },
    {
        "role": "user",
        "content": (
            "I want to buy a espresso machine. Can you help me find product link that fits my budget (300 dollars)?"
        ),
    },
]

client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

response = client.chat.completions.create(
    model="llama-3.1-sonar-large-128k-online",
    messages=messages,
)
with open('response_regular.txt', 'w', encoding='utf-8') as f:
    f.write(str(response))

response_stream = client.chat.completions.create(
    model="llama-3.1-sonar-large-128k-online",
    messages=messages,
    stream=True,
)
with open('response_stream.txt', 'w', encoding='utf-8') as f:
    for response in response_stream:
        f.write(str(response) + '\n')