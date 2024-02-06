import requests

from .model import InferenceResponse, Question


class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_headers(self) -> dict:
        return {"Content-Type": "application/json"}

    def inference(self, question: str) -> InferenceResponse:
        endpoint = f"{self.base_url}/inference"
        body = Question(question=question)
        response = requests.post(endpoint, json=body.model_dump_json(), headers=self.get_headers())
        response.raise_for_status()
        inference_body = InferenceResponse(**response.json())
        return inference_body
