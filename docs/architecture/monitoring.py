from diagrams import Cluster, Diagram
from diagrams.onprem.client import User
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.programming.language import Python

with Diagram("Monitoring Architecture", filename="monitoring", outformat="png", show=False):
    user = User("user")

    with Cluster("Monitoring"):
        grafana = Grafana("Grafana")
        prometheus = Prometheus("Prometheus")
        cadvisor = Python("cAdvisor")

        cadvisor >> prometheus
        prometheus >> grafana
        user >> grafana
