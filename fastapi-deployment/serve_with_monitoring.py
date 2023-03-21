from mlem.api import load_meta, serve
from mlem.contrib.fastapi import FastAPIServer, Middlewares
from mlem.contrib.prometheus import PrometheusFastAPIMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

model = load_meta("price")

server = FastAPIServer(
    standardize=True,
    middlewares=Middlewares(
        __root__=[PrometheusFastAPIMiddleware(instrumentator=Instrumentator())]
    ),
)

serve(
    model=model,
    server=server,
)
