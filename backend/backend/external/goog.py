import requests
from fastapi import HTTPException

def image_search(query, key, app, num=5, page=1, site_search: str | None = "www.amazon.com"):
    params = {
      "cx": app,
      "q": query,
      "safe": "active",
      "searchType": "image",
      "siteSearch": site_search,
      "key": key,
      "start": num*(page - 1) + 1,
      "num": num,
    }

    response = requests.get("https://customsearch.googleapis.com/customsearch/v1", params=params)

    if response.status_code != 200:
        raise HTTPException(detail=f"{response.status_code}: Bad search response")

    data = response.json()
    items = data["items"]
    return [item["link"] for item in items]
