import os
from openai import OpenAI
import replicate

class OpenAIClient:
    def __init__(self):
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.model = "gpt-4o"
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def generate_text(self, prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=280  # Twitter length limit
        )
        return response.choices[0].message.content

    def analyze_content(self, prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{
                "role": "system",
                "content": "Analyze the content and respond with JSON indicating if it needs an image or text response"
            }, {
                "role": "user",
                "content": prompt
            }],
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content

class ReplicateClient:
    def __init__(self):
        self.client = replicate.Client(api_token=os.environ.get("REPLICATE_API_TOKEN"))

    def generate_image(self, prompt):
        output = self.client.run(
            "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
            input={
                "prompt": prompt,
                "negative_prompt": "",
                "width": 768,
                "height": 768,
                "num_outputs": 1,
                "scheduler": "K_EULER",
                "num_inference_steps": 50,
                "guidance_scale": 7.5,
            }
        )
        return output[0]  # Returns URL to generated image
