import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from schemas.article_schema import ArticleListClass

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def process_with_llm(html, instructions, truncate = True):
    if not html:
        return None
    max_length = 15000
    if truncate and len(html) > max_length:
        html = html[:max_length]

    prompt = f"""You are an expert web scraper. Extract the following information from the provided HTML content based on the instructions below. Return the results in a JSON format that matches the ArticleListClass schema.     
Instructions: {instructions}
HTML Content: {html}
"""
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=2000,
    )
    try:
        content = response.choices[0].message.content
        data = json.loads(content)
        articles = ArticleListClass(**data)
        return articles
    except Exception as e:
        print(f"Error processing LLM response: {e}")
        return None
    

