from traceback import format_exc
from typing import Optional, TypeVar, Type, Union, Dict, List

import fastapi
from pydantic import BaseModel

from api.logging.logger import Logger

_T = TypeVar("_T")


class DefaultError(BaseModel):
    title: str
    description: Union[str, dict]
    translation: Optional[str]
    traceback: Optional[str]
    http_status: int

    @property
    def http_error(self):
        return HTTPError(**dict(self))

    @classmethod
    def default(cls: Type[_T]) -> _T:
        return cls(
            title="Internal Error",
            description="An internal error has occurred and its being investigated.",
            translation="Um erro interno aconteceu e está sendo investigado",
            http_status=500,
        )


class HTTPError(fastapi.HTTPException):
    def __init__(
        self,
        title: str,
        exception: Exception = None,
        description: str = None,
        translation: str = None,
        http_status: int = None,
        traceback: str = None,
    ):

        self.logger = Logger

        self.exception = exception
        self.error = DefaultError(
            title=title,
            description=description,
            translation=translation,
            http_status=http_status,
            traceback=traceback,
        )

        if self.exception:
            tb = format_exc()
            if tb:
                tb = tb.splitlines()
                tb_dict = {"traceback": tb[1:]}
                for i in range(0, len(tb_dict["traceback"])):
                    tb_dict["traceback"][i] = (
                        tb_dict["traceback"][i].replace('"', "").strip()
                    )

                self.error.traceback = tb_dict

        super().__init__(status_code=http_status, detail=self.error.dict())


def format_traceback() -> Dict[str, List[str]]:
    trace = format_exc().splitlines()

    traceback_dict = {"traceback": trace[1:]}

    for i in range(0, len(traceback_dict["traceback"])):
        traceback_dict["traceback"][i] = (
            traceback_dict["traceback"][i].replace('"', "").strip()
        )

    return traceback_dict


class PartnerNotFound(HTTPError):
    def __init__(self, id: str, traceback: str = None):
        super().__init__(
            http_status=404,
            title="Partner Not Found",
            description=f"No partner found for the given id {id}",
            translation=f"Nenhum parceiro encontrado para o id fornecido {id}",
            exception=traceback,
        )


class NearestNotFound(HTTPError):
    def __init__(self, long: float, lat: float, traceback: str = None):
        super().__init__(
            http_status=404,
            title="Nearest Not Found",
            description=f"Could not find any partner near the given location: {long}, {lat}",
            translation=f"Não foi possível encontrar nenhum parceiro próxima da localização fornecida: {long}, {lat}",
            exception=traceback,
        )
