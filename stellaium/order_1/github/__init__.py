from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

from stellaium.order_1.github.config import GithubConfig

config = GithubConfig()  # type: ignore

transport = AIOHTTPTransport(url="https://api.github.com/graphql", headers={
    "Authorization": f"Bearer {config.access_token}",
})

github_gql = Client(transport=transport, fetch_schema_from_transport=True)

from . import resources