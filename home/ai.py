import os
import base64
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)


def analyze_product(image_path):

    # Read image
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
You are an AI assistant for an e-commerce website.

Analyze the uploaded product image carefully.

IMPORTANT RULES:
- Do NOT guess information.
- If something is not clearly visible, write "Not Visible".
- Do NOT mention the image background.
- Do NOT mention image quality.
- Base every answer only on what is visible.

Return the response exactly in this format:

## Product Category
<Category Name>

## Brand
<Brand Name if clearly visible, otherwise "Not Visible">

## Product Description
<Write a professional e-commerce product description in 3-5 sentences based only on the visible product.>

## Product Tags
- tag1
- tag2
- tag3
- tag4
- tag5

## SEO Title
<Short SEO-friendly title>

## SEO Meta Description
<One sentence under 160 characters suitable for search engines>
"""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    }
                ]
            }
        ],
        max_tokens=500,
    )

    return response.choices[0].message.content