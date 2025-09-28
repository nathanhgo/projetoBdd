import os
import requests

API_BASE = "https://www.googleapis.com/books/v1"
API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY", "")

def search_volumes(query: str, start: int = 0, limit: int = 10) -> dict:
    """
    Faz uma busca na Google Books API e retorna o JSON bruto do Google.
    Params:
      - query: string de busca (ex: "intitle:Clean Code+inauthor:Martin", "isbn:9780132350884")
      - start: startIndex (paginação)
      - limit: maxResults (1..40)
    """
    params = {
        "q": query,
        "startIndex": max(start, 0),
        "maxResults": min(max(limit, 1), 40),
        "orderBy": "relevance",
        "printType": "books",
        "projection": "full",
    }
    if API_KEY:
        params["key"] = API_KEY

    resp = requests.get(f"{API_BASE}/volumes", params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()