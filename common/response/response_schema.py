from datetime import datetime
from typing import Any

from fastapi import Response
from pydantic import BaseModel, ConfigDict

from common.response.response_code import CustomResponse, CustomResponseCode
from core.conf import settings
from utils.serializer import MsgSpecJSONResponse

_ExcludeData = set[int | str] | dict[int | str, Any]
__all__ = ['ResponseModel', 'response_base']


class ResponseModel(BaseModel):
    """
    HTTP请求统一返回模型
    """

    model_config = ConfigDict(json_encoders={datetime: lambda x: x.strftime(settings.DATETIME_FORMAT)})

    code: int = CustomResponseCode.HTTP_200.code
    msg: str = CustomResponseCode.HTTP_200.msg
    data: Any | None = None


class ResponseBase:
    @staticmethod
    def __response(*, res: CustomResponseCode | CustomResponse = None, data: Any | None = None):
        """
        请求成功通用返回方法
        :param res:
        :param data:
        :return:
        """
        return ResponseModel(code=res.code, msg=res.msg, data=data)

    def success(
        self, *, res: CustomResponseCode | CustomResponse = CustomResponseCode.HTTP_200, data: Any | None = None
    ) -> ResponseModel:
        return self.__response(res=res, data=data)

    def fail(
        self,
        *,
        res: CustomResponseCode | CustomResponse = CustomResponseCode.HTTP_400,
        data: Any = None,
    ) -> ResponseModel:
        return self.__response(res=res, data=data)

    @staticmethod
    def fast_success(
        *, res: CustomResponseCode | CustomResponse = CustomResponseCode.HTTP_200, data: Any | None = None
    ) -> Response:
        return MsgSpecJSONResponse({'code': res.code, 'msg': res.msg, 'data': data})


response_base: ResponseBase = ResponseBase()
