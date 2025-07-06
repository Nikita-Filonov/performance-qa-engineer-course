from diagrams import Cluster, Diagram
from diagrams.aws.storage import S3
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.queue import Kafka
from diagrams.programming.language import Python

with Diagram("Operation Flow Architecture", filename="operations", direction="TB", outformat="png", show=False):
    minio = S3("minio")
    kafka = Kafka("kafka")
    postgres = PostgreSQL("postgres")

    with Cluster("Cards"):
        cards_service = Python("cards-service")

    with Cluster("Accounts"):
        accounts_service = Python("accounts-service")

    with Cluster("Payments"):
        payments_mock_service = Python("payments-mock-service")

    with Cluster("Documents"):
        documents_service = Python("documents-service")

    with Cluster("Operations"):
        operations_service = Python("operations-service")

    documents_service >> [minio, kafka]
    operations_service >> [
        kafka,
        postgres,
        cards_service,
        accounts_service,
        payments_mock_service
    ]
