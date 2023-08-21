import requests

def get_vncs(query='text LIKE "%tty%" OR text LIKE "%linux%" OR text LIKE "%ubuntu%" ORDER BY services.updated_at', amount=25, offset=0):
    return requests.get("https://jew.69.mu/api/search", params={"query": query, "amount": amount, "offset": offset}).json()
