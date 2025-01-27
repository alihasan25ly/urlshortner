
from pydantic import BaseModel

class URLBase(BaseModel):
    target_url: str

class URL(URLBase):
    url: str

    class Config:
        from_attributes = True
