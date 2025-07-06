from diagrams import Cluster, Diagram
from diagrams.generic.storage import Storage
from diagrams.programming.language import Python

with Diagram("Mock Architecture", filename="mock", direction="LR", outformat="png", show=False):
    storage = Storage("mock-files")

    with Cluster("Payments"):
        payments_mock_service = Python("payments-mock-service")

    with Cluster("Operations"):
        operations_service = Python("operations-service")

    operations_service >> [payments_mock_service]
    payments_mock_service >> [storage]
