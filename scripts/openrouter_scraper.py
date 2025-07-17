import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://openrouter.ai/models"


def get_models():
    resp = requests.get(URL, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    models = []
    for card in soup.select("div.model-card"):
        name_elem = card.select_one("h3")
        price_elem = card.select_one(".price")
        link_elem = card.select_one("a")
        name = name_elem.text.strip() if name_elem else ""
        price = price_elem.text.strip() if price_elem else ""
        link = link_elem["href"] if link_elem else ""
        models.append({"name": name, "price": price, "link": link})

    return models


def main():
    models = get_models()
    df = pd.DataFrame(models)
    df.to_csv("openrouter_models.csv", index=False)
    print("Saved", len(df), "models to openrouter_models.csv")


if __name__ == "__main__":
    main()
