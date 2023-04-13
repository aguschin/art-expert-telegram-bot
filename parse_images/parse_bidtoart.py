"""Parse BidToArt auctions."""

import re
import shutil
import typing
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

WEBSITE_URL: str = "https://bidtoart.com"
RESULT_PATH: Path = Path(__file__).parent / "bidtoart"
AUCTION_HOUSES: list[str] = [
    "eclectic",
    "journey-through-france-a-private-collection-of-post-impressionist-paintings",
    "european-paintings-drawings-sculpture",
    "the-rafael-valls-sale",
    "modern-and-contemporary-african-art-online",
    "joseph-h-hirshhorn-collector-for-a-nation-an-online-sale",
    "erotic-online",
    # Phillips
    "auction-27022019",
    "phillips-auction-07-12-2017",
    "phillips-20th-century-contemporary-art-design-evening-sale-hk010417",
    "phillips-latin-america-ny010917",
    "phillips-20th-century-contemporary-art-evening-sale-ny010717",
    "20th-century-contemporary-art-day-sale-afternoon-session",
    "20th-century-contemporary-art-day-sale-morning-session",
    "phillips-auction-19092017",
    "phillips-20th-century-contemporary-art-day-sale-uk010517",
    "phillips-20th-century-contemporary-art-design-evening-sale",
    "phillips-latin-america-1",
    "phillips-20th-century-contemporary-art-evening-sale-1",
    "phillips-20th-century-contemporary-art-day-sale-2",
    "phillips-new-now",
    "phillips-20th-century-contemporary-art-evening-sale-uk010416",
    "phillips-20th-century-contemporary-art-day-sale-1",
    "phillips-20th-century-contemporary-art-evening-sale-2",
    "phillips-new-now-uk010316",
    "new-now-day-sale",
    # Heritage Auctions
    "heritage-auction-08122017-5333",
    "heritage-auction-08122017-5337",
    "fine-decorative-arts-auction-featuring-the-gentleman-collector-signature",
    "heritage-fine-art-painting-5287",
    "heritage-fine-art-painting-5300",
    "texas-art-signature-auction-dallas",
    "fine-art-internet-auction",
    "heritage-auction-14052015",
    "heritage-auction-16052015",
    # Bonhams
    "bonhams-modern-and-contemporary-middle-eastern-art-1",
    "the-grice-collection",
    "19th-century-and-british-impressionist-art",
    "bonhams-made-in-california-3",
    "bonhams-the-greek-sale-4",
    "bonhams-the-marine-sale-6",
    "bonhams-british-and-european-art-3",
    "bonhams-modern-contemporary-african-art-1",
    "bonhams-modern-british-and-irish-art-9",
    "ritual-culture-online",
    "bonhams-modern-contemporary-african-art-4",
    "california-and-western-art",
    "bonhams-modern-contemporary-art-2",
    "bonhams-old-master-paintings-6",
    "bonhams-the-russian-sale-2",
    "bonhams-modern-and-contemporary-middle-eastern-art-online-sale-1",
    "bonhams-modern-british-and-irish-art-8",
    "bonhams-modern-and-contemporary-art-2",
    "the-eddie-basha-collection",
    "bonhams-19th-century-european-paintings-4",
    "bonhams-modern-british-and-irish-art-10",
    "bonhams-the-greek-sale-2",
    "bonhams-british-and-european-art-6",
    "bonhams-impressionist-modern-art-2",
    "bonhams-modern-and-contemporary-middle-eastern-art-3",
    "bonhams-old-master-paintings-4",
    "bonhams-scottish-art",
    "bonhams-impressionist-and-modern-art-2",
    "modern-contemporary-african-art-online-sale",
    "bonhams-modern-contemporary-african-art-3",
    "bonhams-post-war-contemporary-art-10",
    "bonhams-old-master-paintings-9",
    "bonhams-british-and-european-art-5",
    "bonhams-modern-contemporary-art-1",
    "bonhams-impressionist-modern-art-1",
    "bonhams-the-marine-sale-4",
    "bonhams-19th-century-european-paintings-3",
    "bonhams-decorative-art-design-2",
    "bonhams-california-and-western-paintings-and-sculpture-5",
    "bonhams-old-master-paintings-3",
    "bonhams-the-south-african-sale-1",
    "bonhams-post-war-contemporary-art-8",
    "bonhams-the-russian-sale-1",
    "bonhams-modern-british-and-irish-art-7",
    # China Guardian Auctions
    "china-guardian-auction-27032016-45-2",
    "china-guardian-auction-26032016-45-2",
    "china-guardian-auction-20122014-2",
    "china-guardian-auction-07102014",
    "china-guardian-auction-16112013-2",
    # Artcurial
    "the-golden-age-of-danish-painting",
    "art-du-xxe-siecle-entre-avant-garde-et-renouveau",
    "old-master-19th-century-art",
    "artcurial-old-master-19th-century-art-3321",
    "auction-30122017",
    "sale-impressionist-modern-art-2",
    "artcurial-old-master-19th-century-art-3271",
    "artcurial-post-war-contemporary-art-3282",
    "humanus-versus-animal-a-belgian-collection",
    "paul-lombard-collection",
    "artcurial-old-master-19th-century-art-3236",
    "impressionist-modern-art-ii",
    "artcurial-impressionist-modern-art-3164",
    "artcurial-post-war-contemporary-art-3157",
    "artcurial-auction-07062016",
    # ADER
    "vente-online-art-moderne-et-contemporain-arts-decoratifs-du-xxeme",
    "tableaux-modernes-art-naif-art-brut",
    "ader-furniture-and-art-objects",
    "ader-tableaux-anciens-mobilier-objets-dart-2",
    "art-impressionniste-et-moderne-prestige",
    "ader-art-russe-3",
    "ader-art-russe-2",
    "ader-modern-and-contemporary-paintings-2",
    "antique-paintings-miniatures-furniture-works-of-art",
]


def parse_auction(*, auction_house: str) -> pd.DataFrame:
    """Parse a single auction by its name."""

    id_: int = 0
    observations: list[dict[str, typing.Any]] = []
    (RESULT_PATH / auction_house / "images").mkdir(parents=True, exist_ok=True)

    for j in range(1, 1000):

        auction_url: str = WEBSITE_URL + f"/auction-houses/{auction_house}?page={j}&size=20"
        auction_response: bytes = requests.get(auction_url).content
        auction_soup: BeautifulSoup = BeautifulSoup(auction_response, "html.parser")
        auction_items = auction_soup.find_all("div", {"class": "item-result pt-4"})

        if len(auction_items) == 0:
            break

        for item in auction_soup.find_all("div", {"class": "item-result pt-4"}):
            image_source: str = item.find("div", {"class": "image mb-3 mb-sm-0"}).find("a")["href"]
            image_source = WEBSITE_URL + image_source
            image_response: bytes = requests.get(image_source).content
            image_soup: BeautifulSoup = BeautifulSoup(image_response, "html.parser")
            image = image_soup.find("img", {"class": "img-thumbnail img-fluid"})
            if image is None:
                continue
            image_source = image["src"]

            author: str = item.find("a", {"class": "artist-name"}).text.strip()
            title: str = item.find("h2", {"class": "title"}).text.strip()
            medium: str = item.find("span", {"class": "medium"}).text.strip()
            price: str = item.find("label", {"class": "price"}).text.strip()

            properties_table = image_soup.find("table", {"class": "product-info"})
            props: dict[str, str] = {}
            if properties_table is not None:
                properties = properties_table.find_all("tr")
                for row in properties:
                    cols = row.find_all("td")
                    cols = [re.sub("\s\s+", " ", col.text).replace(":", "").strip() for col in cols]
                    props[cols[0]] = cols[1]

            observations.append(
                {
                    "auction": auction_house,
                    "id": id_,
                    "author": author,
                    "title": title,
                    "medium": medium,
                    "price": price,
                    "category": props.get("Category"),
                    "auction_house": props.get("Auction house"),
                    "painting_date": props.get("Date of painting"),
                    "description": props.get("Lot description"),
                    "auction_date": props.get("Auction date"),
                    "image_source": image_source,
                }
            )

            with open(RESULT_PATH / auction_house / "images" / f"{id_}.jpg", "wb") as f:
                f.write(requests.get(image_source).content)

            id_ += 1

    return pd.DataFrame(observations)


def combine_results():
    """Combine splits."""

    cols: list[str] = [
        "auction",
        "id",
        "author",
        "title",
        "medium",
        "price",
        "category",
        "auction_house",
        "painting_date",
        "description",
        "auction_date",
        "image_source",
    ]
    df: pd.DataFrame = pd.DataFrame(columns=cols)

    for auction_house in AUCTION_HOUSES:
        df_new: pd.DataFrame = pd.read_csv(RESULT_PATH / auction_house / "prices.csv", usecols=cols)
        df = pd.concat([df, df_new])

    df = df[df["category"].isin(["Paintings", "Works on paper", "Prints & Graphic Art"])]
    df = df.reset_index().drop(columns=["index"])

    for i, row in df.iterrows():
        image: Path = RESULT_PATH / row.auction / "images" / f"{row.id}.jpg"
        shutil.copy(image, RESULT_PATH / "final" / "images" / f"{i}.jpg")

    df = df.drop(columns="id")
    df.to_csv(RESULT_PATH / "final" / "bidtoart.csv")


if __name__ == "__main__":
    for auction in AUCTION_HOUSES:
        try:
            df_: pd.DataFrame = parse_auction(auction_house=auction)
            df_.to_csv(RESULT_PATH / auction / "prices.csv")
        except Exception as err:
            print(auction, err)
    combine_results()
