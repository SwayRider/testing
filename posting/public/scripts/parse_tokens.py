from posting import Posting
import httpx


def on_response(response: httpx.Response, posting: Posting) -> None:
    if response.status_code == 200:
        json = response.json()
        access_token = json["access_token"]
        refresh_token = json["refresh_token"]
        posting.set_variable("access_token", access_token)
        posting.set_variable("refresh_token", refresh_token)
