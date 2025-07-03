from diagrams import Cluster, Diagram
from diagrams.aws.storage import S3
from diagrams.onprem.queue import Kafka
from diagrams.programming.language import Python

with Diagram(
        show=False,
        name="Documents Service Architecture",
        filename="architecture",
        direction="TB",
        outformat="png",
):
    minio = S3("minio")
    kafka = Kafka("kafka")

    with Cluster("Accounts"):
        accounts_service = Python("accounts-service")

    with Cluster("Documents"):
        documents_service = Python("documents-service")
        kafka_documents = Python("kafka-documents")

    documents_service >> [minio, accounts_service]
    kafka_documents >> [kafka, minio]
