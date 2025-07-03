from diagrams import Cluster, Diagram
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.queue import Kafka
from diagrams.programming.language import Python

with Diagram(
        show=False,
        name="Operations Service Architecture",
        filename="architecture",
        direction="TB",
        outformat="png",
):
    kafka = Kafka("kafka")
    postgres = PostgreSQL("postgres")

    with Cluster("Cards"):
        cards_service = Python("cards-service")

    with Cluster("Accounts"):
        accounts_service = Python("accounts-service")

    with Cluster("Operations"):
        operations_service = Python("operations-service")

    operations_service >> [kafka, postgres, cards_service, accounts_service]
