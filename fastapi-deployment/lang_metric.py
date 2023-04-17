import numpy as np
from prometheus_client import Counter, Gauge
from prometheus_fastapi_instrumentator.metrics import Info

RANDOM_VALUE = Gauge(
    "random_value", "Random value that is set to show monitoring works"
)


def random_value(info: Info) -> None:
    RANDOM_VALUE.set(np.random.random())


METRIC_EXAMPLE = Counter(
    "http_requested_languages_total",
    "Number of times a certain language has been requested.",
    labelnames=("langs",),
)


def http_requested_languages_total(info: Info) -> None:
    langs = set()
    lang_str = info.request.headers["Accept-Language"]
    for element in lang_str.split(","):
        element = element.split(";")[0].strip().lower()
        langs.add(element)
    for language in langs:
        METRIC_EXAMPLE.labels(language).inc()
