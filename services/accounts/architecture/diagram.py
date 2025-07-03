from diagrams import Cluster, Diagram
from diagrams.onprem.database import PostgreSQL
from diagrams.programming.language import Python

with Diagram(
        show=False,
        name="Accounts Service Architecture",
        filename="architecture",
        direction="TB",
        outformat="png",
):
    postgres = PostgreSQL("postgres")

    with Cluster("Users"):
        users_service = Python("users-service")

    with Cluster("Accounts"):
        accounts_service = Python("accounts-service")

    accounts_service >> [postgres, users_service]
