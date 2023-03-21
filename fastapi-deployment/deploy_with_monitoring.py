from mlem.api import load_meta, deploy
from mlem.contrib.fastapi import FastAPIServer, Middlewares
from mlem.contrib.prometheus import PrometheusFastAPIMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

model = load_meta("price")

instrumentator = Instrumentator()

server = FastAPIServer(
    standardize=True,
    middlewares=Middlewares(
        __root__=[PrometheusFastAPIMiddleware(instrumentator=instrumentator)]
    ),
)

deploy(
    "app-fastapi.mlem",
    model=model,
    server=server,
    app_name="art-expert-fastapi",
)
