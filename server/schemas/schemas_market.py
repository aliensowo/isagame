from pydantic import BaseModel


class SchemaMarketPut(BaseModel):
    element: str
    cost: int
    count: int
