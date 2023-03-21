from typing import Callable

from mlem.api import load_meta, serve
from mlem.contrib.fastapi import FastAPIServer, Middlewares
from mlem.contrib.prometheus import PrometheusFastAPIMiddleware
from prometheus_fastapi_instrumentator.metrics import Info
from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator


def http_requested_languages_total() -> Callable[[Info], None]:
    METRIC = Counter(
        "http_requested_languages_total",
        "Number of times a certain language has been requested.",
        labelnames=("langs",)
    )

    def instrumentation(info: Info) -> None:
        langs = set()
        lang_str = info.request.headers["Accept-Language"]
        for element in lang_str.split(","):
            element = element.split(";")[0].strip().lower()
            langs.add(element)
        for language in langs:
            METRIC.labels(language).inc()

    return instrumentation

instrumentator = Instrumentator()
instrumentator.add(http_requested_languages_total())

model = load_meta("price")

server = FastAPIServer(
    standardize=True,
    middlewares=Middlewares(
        __root__=[PrometheusFastAPIMiddleware(instrumentator=instrumentator)]
    ),
)

serve(
    model=model,
    server=server,
)
