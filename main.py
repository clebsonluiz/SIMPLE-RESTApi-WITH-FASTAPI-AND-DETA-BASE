__author__ = 'Clébson Luiz'
__version__ = "1.0-alpha"
__description__ = "Projeto para aprendizado de micro-serviços e api's com DETA e FASTApi"


import uvicorn

from typing import Optional, List
from pydantic import BaseModel, Field

from deta import Deta, Base

from fastapi import FastAPI
from fastapi.routing import APIRouter


#Default Data Json Example
_JSON_MESSAGE = {
    "ola": "</Sertão Dev>",
    "por": "Clébson Luiz :)",
    "infos": [
        {
            "Micro Serviço Usado Para Deploy": "Deta Micros",
            "Acesse a Documentação": "https://wxvmfr.deta.dev/docs",
            "Outrem...": "https://wxvmfr.deta.dev/redoc"
        },
        "Aplicação simples desenvolvida em Python " +
        "utilizando o modulo FastApi para fins de teste e aprendizado!",
    ],
    "para_mais_info": [
        "https://fastapi.tiangolo.com/",
        "https://docs.deta.sh"
    ]
}


class MessageExample(BaseModel):
    """
    BaseModel used by custom json to FastApi
    """
    ola: Optional[str] = Field(None, example="</Sertão Dev>")
    por: Optional[str] = "Clébson Luiz :)"
    infos: Optional['list'] = None
    para_mais_info: Optional['list'] = Field(None)

    class Config:
        """
        Used to create a example schema to documentation in '/docs'
        """
        schema_extra = {
            "example": _JSON_MESSAGE
        }


def create_api_routers() -> APIRouter:
    """
    Creates the rest api routers and includes a 
    connection in deta project to create a deta base.
    :return: APIRouter
    """
    _api_base: Base = Deta(
        project_key="DETA-PROJECT-KEY",
        project_id="DETA-PROJECT-ID"
    ).Base("quaisquer_deta_base")
    
    api_router: APIRouter = APIRouter()

    @api_router.get('/', status_code=200, response_model=List[MessageExample])
    def method_get():
        """
        Find and return all objects from deta base
        :returns: json
        """
        return next(_api_base.fetch())


    @api_router.put('/{key}', status_code=203)
    def method_put(key: str, msg: MessageExample):
        """
        Find by key and uptade a entry in deta base
        :returns: json
        """
        _finded = _api_base.get(key)
        to_update = MessageExample(**(_finded if _finded != None else {}))
        new_data = msg.dict(exclude_unset=True)
        updated = to_update.copy(update=new_data)
        return _api_base.put(updated.dict(), key)


    @api_router.post('/', status_code=201)
    def method_post(msg: MessageExample):
        """
        Insert a new entry in deta base
        :returns: json
        """
        return _api_base.insert(msg.dict())


    @api_router.delete('/{key}', status_code=204)
    def method_delete(key: str):
        """
        Delete by key a entry in deta base
        """
        _api_base.delete(key)

    return api_router


def create_app() -> FastAPI:
    """
    create a main FastAPI app and includes routers to endpoint.
    :returns: FastAPI
    """
    _app = FastAPI()

    @_app.get("/")
    def read_root(opitional_param: Optional[str] = None):
        """
        Main Test of endpoint
        :returns: json
        """
        _json = MessageExample(**_JSON_MESSAGE).dict()
        if opitional_param:
            _temp = _json.copy()
            _temp["Parametro Opcional foi..."] = opitional_param
            return _temp
        return _json
    
    _api_routers = create_api_routers()
    _app.include_router(_api_routers, prefix='/api')
    return _app

app = create_app()

if __name__ == "__main__":
    """
    Utilized to run FastApi on localhost
    """
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
