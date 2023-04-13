"""Parse Artsy items."""

import os
import shutil
import typing
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

WEBSITE_URL: str = "https://www.artsy.net/collection/painting"
RESULT_PATH: Path = Path(__file__).parent / "artsy"


def parse_page(*, page: int) -> pd.DataFrame:
    """Parse a single page."""

    (RESULT_PATH / "images" / f"{page}").mkdir(exist_ok=True)

    observations: list[dict[str, typing.Any]] = []
    id_: int = 0

    collection_url: str = WEBSITE_URL + f"?page={page}"
    collection_response: bytes = requests.get(collection_url).content
    collection_soup: BeautifulSoup = BeautifulSoup(collection_response, "html.parser")
    items = collection_soup.find_all("div", {"data-test": "artworkGridItem"})

    for item in items:
        source: str = item.find("img")["src"]
        author: str = item.find("div", {"class": "Box-sc-15se88d-0 Text-sc-18gcpao-0 ilQWRL"}).text
        title: str = item.find("div", {"class": "Box-sc-15se88d-0 Text-sc-18gcpao-0 caIGcn iVSzqj"}).text
        price: str = item.find("div", {"class": "Box-sc-15se88d-0 Text-sc-18gcpao-0 eXbAnU bfCidL"}).text

        observations.append(
            {"page": page, "id": id_, "source": source, "author": author, "title": title, "price": price}
        )

        with open(RESULT_PATH / "images" / f"{page}" / f"{id_}.jpeg", "wb") as f:
            f.write(requests.get(source).content)

        id_ += 1

    return pd.DataFrame(observations)


def combine_results() -> None:
    """Combine splits."""

    cols: list[str] = ["page", "id", "source", "author", "title", "price"]
    df: pd.DataFrame = pd.DataFrame(columns=cols)

    for csv_file in os.listdir(RESULT_PATH / "prices"):
        df_new: pd.DataFrame = pd.read_csv(RESULT_PATH / "prices" / csv_file, usecols=cols)
        df = pd.concat([df, df_new])
        df = df.drop_duplicates(subset=["source"], keep="first")

    df = df.reset_index().drop(columns=["index"])

    for i, row in df.iterrows():
        image: Path = RESULT_PATH / "images" / str(row.page) / f"{row.id}.jpeg"
        shutil.copy(image, RESULT_PATH / "final" / "images" / f"{i}.jpeg")

    df = df.drop(columns=["page", "id"])
    df.to_csv(RESULT_PATH / "final" / "artsy.csv")


if __name__ == "__main__":
    for p in range(1, 100 + 1):
        df_: pd.DataFrame = parse_page(page=p)
        df_.to_csv(RESULT_PATH / "prices" / f"{p}.csv")
    combine_results()
