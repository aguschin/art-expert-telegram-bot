from mlem.api import load_meta, serve
from mlem.contrib.fastapi import FastAPIServer, Middlewares
from mlem.contrib.prometheus import PrometheusFastAPIMiddleware


def main():
    model = load_meta("models/orig_dataset/mlem_orig_dataset")

    api_middleware = PrometheusFastAPIMiddleware(
        metrics=[
            "lang_metric.random_value",
            "lang_metric.http_requested_languages_total",
        ]
    )
    server = FastAPIServer(
        standardize=True,
        middlewares=Middlewares(__root__=[api_middleware]),
        port=8080,
    )

    serve(
        model=model,
        server=server,
    )


if __name__ == "__main__":
    main()
