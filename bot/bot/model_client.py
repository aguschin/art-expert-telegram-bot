from dataclasses import dataclass
from io import BytesIO

from httpx import AsyncClient
from pydantic import BaseModel

InputFileType = bytes | BytesIO


class ModelPredictResponse(BaseModel):
    price: float


@dataclass
class ModelClient:
    model_api_url: str
    httpx_client: AsyncClient

    async def predict(self, image_bytes: InputFileType) -> ModelPredictResponse:
        files = {"file": image_bytes}
        resp = await self.httpx_client.post(
            f"{self.model_api_url}/predict", files=files
        )
        resp.raise_for_status()
        return ModelPredictResponse.parse_obj(resp.json())
