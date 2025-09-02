# models.py

import os
import aiohttp
from loguru import logger

# Models configuration map
models = {
    "text": {
        # "endpoint": "http://localhost:8000/v1/chat",
        "endpoint": "https://api.openai.com/v1/chat/completions",
        "system_prompt": "You are an AI assistant"
    }
}

async def generate_text(model: str, prompt: str, temperature: float = 0.7) -> str:
    if model not in models:
        raise ValueError(f"Unsupported model: {model}")
    
    model_config = models[model]
    system_prompt = model_config["system_prompt"]
    endpoint = model_config["endpoint"]
    
    message = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
    ]
    data = {"temperature": temperature, "messages": message, "model": "gpt-4o"}
    headers = {"Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}"}
    try:
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                    endpoint, json=data, headers=headers
                    )
            predictions = await response.json()
    except Exception as e:
        logger.error(f"Failed to obtain predictions from vLLM - Error: {e}")
        return (
            "Failed to obtain predictions from vLLM - "
            "See server logs for more details"
        )
    try: 
        
        output = predictions["choices"][0]["message"]["content"]
        logger.debug(f"Generated text: {output}")
        return output
    except Exception as e:
        logger.error(f"Failed to parse predictions from vLLM - Error: {e}")
        print(e)
        return (
            "Failed to parse predictions from vLLM - "
            "See server logs for more details"
        )
