import json
import requests

import ai.models.abstract_model


class QwenModel(
    ai.models.abstract_model.AbstractModel,
):
    def send_request(self, token, history):
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                #"model": "qwen/qwen3-14b:free",
                "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
                "messages": history,
            })
        )
        print(response.text)
        return response.json()["choices"][0]["message"]["content"]
