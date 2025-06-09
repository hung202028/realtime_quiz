import prometheus_client.context_managers
from prometheus_client import Gauge, Histogram

from app.monitor.base import Monitor


class Prometheus(Monitor):
    def __init__(self, *args, **kwargs):
        gauge_name = kwargs.get("gauge_name")
        gauge_documentation = kwargs.get("gauge_documentation")
        histogram_name = kwargs.get("histogram_name")
        histogram_documentation = kwargs.get("histogram_documentation")

        self._gauge = Gauge(name=gauge_name, documentation=gauge_documentation)
        self._histogram = Histogram(name=histogram_name, documentation=histogram_documentation)

    def record_connection_established(self):
        self._gauge.inc()

    def record_connection_terminated(self):
        self._gauge.dec()

    def time_request(self) -> prometheus_client.context_managers.Timer:
        return self._histogram.time()
