from typing import Dict, Type, Optional, Any

import httpx
from pydantic import BaseModel

from api.base.endpoint import Endpoint


class ApiClient:
    def __init__(
            self,
            base_url: str,
            auth_key: Optional[str] = None,
            auth_header: str = "Authorization",
            auth_prefix: str = "Token ",
    ):
        self.base_url = base_url
        self.auth_key = auth_key
        self.auth_header = auth_header
        self.auth_prefix = auth_prefix

        headers = {}
        if auth_key:
            headers[auth_header] = f"{auth_prefix}{auth_key}"

        self.client = httpx.AsyncClient(
            headers=headers,
            timeout=30.0,
            follow_redirects=True,
        )
        self.endpoints: Dict[str, Endpoint] = {}

    def register_endpoint(
            self,
            name: str,
            path: str,
            request_model: Type[BaseModel],
            response_model: Optional[Type[BaseModel]] = None,
            method: str = 'POST'
    ):
        self.endpoints[name] = Endpoint(path, request_model, response_model, method)

    def __getattr__(self, name: str):
        if name not in self.endpoints:
            raise AttributeError(f"Endpoint '{name}' not registered.")

        endpoint = self.endpoints[name]

        async def request(
                data: Optional[dict] = None,
                params: Optional[dict] = None,
                json: Optional[Any] = None,
                **kwargs: Any,
        ) -> Any:
            body_data = None
            query_params = params or {}

            if data is not None:
                validated = await endpoint.validate_input_data(data)
                validated_dict = validated.model_dump(exclude_unset=True)

                if endpoint.method in ("POST", "PUT", "PATCH"):
                    body_data = json if json is not None else validated_dict
                elif endpoint.method == "GET":
                    query_params = {**query_params, **validated_dict}

            url = f"{self.base_url}/{endpoint.path}"

            response = await self.client.request(
                method=endpoint.method,
                url=url,
                json=body_data,
                params=query_params,
                **kwargs,
            )

            response.raise_for_status()
            validated_response = await endpoint.validate_response_data(response.json())

            try:
                return validated_response
            except Exception:
                return response.text

        return request
