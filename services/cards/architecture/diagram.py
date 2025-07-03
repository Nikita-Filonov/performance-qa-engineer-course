from diagrams import Cluster, Diagram
from diagrams.onprem.database import PostgreSQL
from diagrams.programming.language import Python

with Diagram(
        show=False,
        name="Cards Service Architecture",
        filename="architecture",
        direction="TB",
        outformat="png",
):
    postgres = PostgreSQL("postgres")

    with Cluster("Cards"):
        cards_service = Python("cards-service")

    with Cluster("Accounts"):
        accounts_service = Python("accounts-service")

    cards_service >> [postgres, accounts_service]
