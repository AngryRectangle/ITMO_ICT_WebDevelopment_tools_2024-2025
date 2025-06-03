import requests
from fastapi import FastAPI, HTTPException


def fetch_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) "
                      "Gecko/20100101 Firefox/138.0"
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.text


def parse_data(url: str):
    html = fetch_html(url)
    title = html.split('<title itemprop="headline">')[1].split('</title>')[0]
    wealth = html.split('profile-info__item-value">$')[1].split('B</div>')[0]
    return {
        "title": title,
        "wealth": wealth
    }


app = FastAPI()


@app.get("/parse")
def parse(url: str):
    try:
        return parse_data(url)
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
