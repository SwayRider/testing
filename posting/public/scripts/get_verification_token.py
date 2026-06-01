from posting import Posting
import httpx


def on_response(response: httpx.Response, posting: Posting) -> None:
    if response.status_code == 200:
        json = response.json()
        user_id = json["user_id"]
        token = json["token"]
        posting.set_variable("registered_user_id", user_id)
        posting.set_variable("registered_user_verification_token", token)
