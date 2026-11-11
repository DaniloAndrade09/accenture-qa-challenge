import requests


class BookStoreAPI:
    BASE_URL = "https://demoqa.com"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def create_user(self, username, password):
        return self.session.post(
            f"{self.BASE_URL}/Account/v1/User",
            json={
                "userName": username,
                "password": password,
            },
            timeout=30,
        )

    def generate_token(self, username, password):
        return self.session.post(
            f"{self.BASE_URL}/Account/v1/GenerateToken",
            json={
                "userName": username,
                "password": password,
            },
            timeout=30,
        )

    def authorize_user(self, username, password):
        return self.session.post(
            f"{self.BASE_URL}/Account/v1/Authorized",
            json={
                "userName": username,
                "password": password,
            },
            timeout=30,
        )

    def list_books(self):
        return self.session.get(
            f"{self.BASE_URL}/BookStore/v1/Books",
            timeout=30,
        )

    def reserve_books(self, user_id, token, isbns):
        return self.session.post(
            f"{self.BASE_URL}/BookStore/v1/Books",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "userId": user_id,
                "collectionOfIsbns": [
                    {"isbn": isbn} for isbn in isbns
                ],
            },
            timeout=30,
        )

    def get_user(self, user_id, token):
        return self.session.get(
            f"{self.BASE_URL}/Account/v1/User/{user_id}",
            headers={
                "Authorization": f"Bearer {token}",
            },
            timeout=30,
        )
