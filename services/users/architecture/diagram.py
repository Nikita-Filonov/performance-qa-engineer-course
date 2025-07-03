from diagrams import Cluster, Diagram
from diagrams.onprem.database import PostgreSQL
from diagrams.programming.language import Python

with Diagram(
        show=False,
        name="Users Service Architecture",
        filename="architecture",
        outformat="png"
):
    postgres = PostgreSQL("postgres")

    with Cluster("Users"):
        users_service = Python("users-service")

    users_service >> [postgres]
