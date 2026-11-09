import time
from flask import Response, g
from app.metrics import metrics
from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST
)

http_requests_total = Counter(
    "amigos_http_requests_total",
    "Número total de peticiones HTTP recibidas por Amigos"
)

http_errors_total = Counter(
    "amigos_http_errors_total",
    "Número total de respuestas HTTP de error"
)

http_request_duration_seconds = Histogram(
    "amigos_http_request_duration_seconds",
    "Tiempo de respuesta de las peticiones HTTP en segundos"
)

@metrics.before_app_request
def before_request():
    g.start_time = time.perf_counter()

@metrics.after_app_request
def after_request(response):
    http_requests_total.inc()
    if response.status_code >= 400:
        http_errors_total.inc()
    duration = time.perf_counter() - g.start_time
    http_request_duration_seconds.observe(duration)
    return response

@metrics.route("/metrics")
def metrics_endpoint():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )