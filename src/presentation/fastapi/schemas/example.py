from pydantic import BaseModel


class ExampleRequest(BaseModel):
    id: int


class ExampleResponse(BaseModel):
    status: bool
