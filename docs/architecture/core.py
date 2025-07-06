from diagrams import Cluster, Diagram
from diagrams.aws.storage import S3
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.queue import Kafka
from diagrams.programming.language import Python

with Diagram("Service Architecture", filename="core", outformat="png", show=False):
    redis = Redis("redis")
    minio = S3("minio")
    kafka = Kafka("kafka")
    postgres = PostgreSQL("postgres")

    with Cluster("Users"):
        users_service = Python("users-service")

    with Cluster("Cards"):
        cards_service = Python("cards-service")

    with Cluster("Gateway"):
        gateway_service = Python("gateway-service")

    with Cluster("Accounts"):
        accounts_service = Python("accounts-service")

    with Cluster("Documents"):
        documents_service = Python("documents-service")

    with Cluster("Operations"):
        operations_service = Python("operations-service")

    with Cluster("Monitoring"):
        grafana = Grafana("grafana")
        cadvisor = Python("cadvisor")
        prometheus = Prometheus("prometheus")
        cadvisor >> prometheus
        prometheus >> grafana

    users_service >> [postgres]
    cards_service >> [postgres, accounts_service]
    accounts_service >> [postgres, users_service]
    documents_service >> [minio, kafka, accounts_service, operations_service]
    operations_service >> [kafka, postgres, cards_service, accounts_service]

    gateway_service >> [
        redis,
        kafka,
        users_service,
        cards_service,
        accounts_service,
        documents_service,
        operations_service,
    ]
