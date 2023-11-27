from openai import OpenAI

from src.generative_ai.image_generation import CONFIG
from utils.logging import set_logger
from utils.misc import base64_to_img

logger = set_logger(__file__)

model_config = CONFIG["DALL-E 2"]


def dall_e_image(
    prompt: str,
    width: int = 1024,
    height: int = 1024,
):
    client = OpenAI()
    response = client.images.generate(
        model=model_config["string"],
        prompt=prompt,
        size=f"{width}x{height}",
        n=1,
        response_format="b64_json",
    )
    base64 = response.data[0]["b64_json"]
    return base64_to_img(base64)