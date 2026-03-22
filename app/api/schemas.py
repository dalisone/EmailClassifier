from typing import Literal

from pydantic import BaseModel, Field


class ProcessEmailResponse(BaseModel):
    category: Literal["Produtivo", "Improdutivo"]
    reply: str = Field(..., min_length=1, max_length=1200)

