import re
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

WEBSITE_URL = "https://bidtoart.com"


def parse_website(*, num_pages: int = 500) -> pd.DataFrame:

    observations: list[dict[str, str]] = []

    for i in range(1, num_pages + 1):

        auction_results_url: str = WEBSITE_URL + f"/auction-results?page={i}&size=20"
        auction_results_response: bytes = requests.get(auction_results_url).content
        auction_results_soup: BeautifulSoup = BeautifulSoup(auction_results_response, "html.parser")

        for auction_result in auction_results_soup.find_all("div", {"class": "auction-result-item clearfix row"}):
            auction_url: str = WEBSITE_URL + auction_result.find("a")["href"]
            # TODO: на аукционе может быть несколько страниц
            auction_response: bytes = requests.get(auction_url).content
            auction_soup: BeautifulSoup = BeautifulSoup(auction_response, "html.parser")

            for auction_item in auction_soup.find_all("div", {"class": "image mb-3 mb-sm-0"}):
                item_url: str = WEBSITE_URL + auction_item.find("a")["href"]
                item_response: bytes = requests.get(item_url).content
                item_soup: BeautifulSoup = BeautifulSoup(item_response, "html.parser")

                image_source = item_soup.find("img", {"class": "img-thumbnail img-fluid"})
                if image_source is None:
                    continue
                observation: dict[str, str] = {"Image Source": image_source["src"]}

                properties_table = item_soup.find("table", {"class": "product-info"})
                if properties_table is None:
                    continue
                properties = properties_table.find_all("tr")

                for row in properties:
                    cols = row.find_all("td")
                    cols = [re.sub("\s\s+", " ", col.text).replace(":", "").strip() for col in cols]
                    observation[cols[0]] = cols[1]
                    observations.append(observation)

    return pd.DataFrame(observations)


if __name__ == "__main__":
    df: pd.DataFrame = parse_website(num_pages=1)
    save_to: Path = Path(__file__).parent / "results" / "bidtoart.csv"
    df.to_csv(save_to, sep=";", encoding="utf-8-sig")
