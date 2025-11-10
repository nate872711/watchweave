import httpx
from rich import print


class TheTVDBClient:
    BASE = "https://api4.thetvdb.com/v4"

    def __init__(self, api_key: str, pin: str):
        self.api_key = api_key
        self.pin = pin
        self.token = None

    async def authenticate(self):
        url = f"{self.BASE}/login"
        payload = {"apikey": self.api_key, "pin": self.pin}

        try:
            async with httpx.AsyncClient() as client:
                r = await client.post(url, json=payload)
                data = r.json()

                if "data" in data:
                    self.token = data["data"]["token"]
                    print("[green]TheTVDB authenticated")
                else:
                    print(f"[red]TheTVDB auth error: {data}")
        except Exception as e:
            print(f"[red]TheTVDB connection error: {e}")

    async def _get(self, endpoint):
        if not self.token:
            print("[red]TheTVDB: No token, authenticate first")
            return None

        headers = {"Authorization": f"Bearer {self.token}"}
        url = f"{self.BASE}{endpoint}"

        async with httpx.AsyncClient() as client:
            r = await client.get(url, headers=headers)
            return r.json()

    async def search(self, query):
        return await self._get(f"/search?query={query}")

    async def get_series(self, tvdb_id):
        return await self._get(f"/series/{tvdb_id}")
