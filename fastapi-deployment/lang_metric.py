from prometheus_fastapi_instrumentator.metrics import Info
import numpy as np
from PIL import Image
from prometheus_client import Counter, Histogram, Gauge


RANDOM_VALUE = Gauge(
    "random_value",
    "Random value that is set to show monitoring works"
)

def random_value(info: Info) -> None:
    RANDOM_VALUE.set(np.random.random())



METRIC_EXAMPLE = Counter(
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
        METRIC_EXAMPLE.labels(language).inc()


MEAN_PIXEL_VALUE = Histogram(
    'image_middle_pixel_value',
    'Mean pixel value of the image',
    buckets=(0, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275),
)


async def image_middle_pixel_value(info: Info) -> None:
    # this would have been a way to load the image
    # and calculate some metrics, but it doesn't work
    # (limitations of `prometheus_fastapi_instrumentator`)
    # keeping the code piece as an example though
    form = await info.request.form()
    im = Image.open(form['file'].file)
    mean_value = np.array(im).mean()
    MEAN_PIXEL_VALUE.observe(mean_value)
