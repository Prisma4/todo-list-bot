from typing import Type, Optional, Union

from pydantic import BaseModel


class Endpoint:
    def __init__(
            self,
            path: str,
            request_model: Type[BaseModel],
            response_model: Optional[Type[BaseModel]] = None,
            method: str = 'POST'
    ):
        self.path = path
        self.request_model = request_model
        self.response_model = response_model
        self.method = method

    async def validate_input_data(self, data: dict) -> BaseModel:
        return self.request_model(**data)

    async def validate_response_data(self, data: Union[dict, list]) -> Union[BaseModel, dict, list]:
        if self.response_model is None:
            return data

        if isinstance(data, dict):
            return self.response_model(**data)
        elif isinstance(data, list):
            return [self.response_model(**obj) for obj in data]
