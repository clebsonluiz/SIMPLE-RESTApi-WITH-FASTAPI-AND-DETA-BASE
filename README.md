# FASTApi with Deta Base connection

Projeto com intuito de aprendizado a respeito de de FASTApi utilização de bases non-sql, utilizando neste projeto o [FastAPI](https://fastapi.tiangolo.com/) bem como os serviços do Deta como [Deta Base](https://docs.deta.sh/docs/base/about), e possivelmente fazendo deploy com [Deta Micro](https://docs.deta.sh/docs/micros/about). Para mais informações consulte a documentação oficial [Deta Docs](https://docs.deta.sh/docs/home)

## Configuração e Utilização

### Configurando os Models

Abaixo é possivel observar uma configuração basica dos BaseModels do pydantic, desta forma é possivel obter uma definição dos objetos passados no corpo da requisição.

```python
class MessageExample(BaseModel):
    """...
    """
    ola: Optional[str] = Field(None, example="Simple example")
    por: Optional[str] = "Clébson Luiz :)"
    infos: Optional['list'] = None
    para_mais_info: Optional['list'] = Field(None)

    class Config:
        """...
        """
        schema_extra = {
            "example": {
                "ola": "...",
                "por": "Clébson Luiz :)",
                "infos": [...],
                "para_mais_info": [
                    "https://fastapi.tiangolo.com/",
                    "https://docs.deta.sh"
                ]
            }
        }

```


### Configurando Deta Base

Para usar só utilizar com os seus respectivos DETA-PROJECT-KEY e DETA-PROJECT-ID fornecidos quando é criado um projeto Deta em sua conta no [Deta](https://web.deta.sh). Já o quaisquer_deta_base, fica a seu critério o nome da base, ressaltando que cada base seria "equivalente" a uma unica tabela usando como exemplo um banco de dados relacional tipico

Para usar o projeto, primeiro é necessário configurar algumas coisas no arquivo 'main'localizando a função a seguir: 

```python
def create_api_routers() -> APIRouter:
    """...
    """
    _api_base: Base = Deta(
        project_key="DETA-PROJECT-KEY",
        project_id="DETA-PROJECT-ID"
    ).Base("quaisquer_deta_base")
    
    ...

```

- *DETA-PROJECT-KEY*: Sua key usada para acessar as propriedades da Base em um projeto Deta. Pode ser obtida na criação de um novo projeto ou criada uma nova nas configurações do projeto ou removida.
- *DETA-PROJECT-ID*: O id de seu projeto deta, obtido quando é criado um novo projeto, é imutável.
- *quaisquer_deta_base*: o nome da sua base no Deta que você deseja utilizar.

Ainda dentro da função, é criado as rotas para nosso endpoint utilizando o APIRouter do fastapi:

```python
    api_router: APIRouter = APIRouter()

    @api_router.get('/', status_code=200, response_model=List[MessageExample])
    def method_get():
        ...

    @api_router.put('/{key}', status_code=203)
    def method_put(key: str, msg: MessageExample):
        ...

    @api_router.post('/', status_code=201)
    def method_post(msg: MessageExample):
        ...

    @api_router.delete('/{key}', status_code=204)
    def method_delete(key: str):
        ...
```

Por fim, a função abaixo cria o nosso app FastAPI e inclue nele uma nova rota padrão e adiciona nossas rotas de acesso a API, ao nosso endpoint. 


```python
def create_app() -> FastAPI:
    ...
    _app = FastAPI()

    @_app.get("/")
    def read_root(opitional_param: Optional[str] = None):
        ...
    
    _api_routers = create_api_routers()
    _app.include_router(_api_routers, prefix='/api')
    return _app
```

### Configurando para localhost

Já a configuração abaixo serve apenas para rodar o uvicorn em localhost no main. No final do arquivo main, temos:

```python
if __name__ == "__main__":
    """
    Utilized to run FastApi on localhost
    """
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

```

- Desta forma, é possivel rodar a aplicação em localhost com o comando na pasta raiz:

```bash
python main.py
```
Lembrando que mesmo que usando virtual-env python e/ou for fazer deploy do projeto em algum micro serviço, é necessário especificar as dependencias do projeto no arquivo requirements.txt e instala-las.

```bash
deta==0.7
fastapi==0.61.2
pydantic==1.7.2
starlette==0.13.6
uvicorn==0.12.2
```

Para acessar o endpoint do projeto, se for local e nada foi alterado no main é pelo http://localhost:8000/, se foi feito deploy em algum micro serviço, então é pelo path fornecido por este, em meu caso, este projeto foi feito deploy usando o [Deta Micro](https://docs.deta.sh/docs/micros/about), logo nossa url fica https://<url_aleatorio_gerado>.deta.dev, este projeto se encontra atualmente em: https://wxvmfr.deta.dev/.