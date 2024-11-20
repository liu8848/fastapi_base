from starlette.responses import JSONResponse
from typing import Any
from msgspec import json

class MsgSpecJSONResponse(JSONResponse):
    """
    JSON response using the high-performance msgspec library to serialize data to JSON.
    """

    def render(self, content: Any) -> bytes:
        return json.encode(content)