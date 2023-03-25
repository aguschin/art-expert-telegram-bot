from prometheus_client import Counter
from prometheus_fastapi_instrumentator.metrics import Info


METRIC = Counter(
    "http_requested_languages_total",
    "Number of times a certain language has been requested.",
    labelnames=("langs",)
)


def http_requested_languages_total(info: Info) -> None:
    langs = set()
    lang_str = info.request.headers["Accept-Language"]
    for element in lang_str.split(","):
        element = element.split(";")[0].strip().lower()
        langs.add(element)
    for language in langs:
        METRIC.labels(language).inc()
