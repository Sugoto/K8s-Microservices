FROM python:3.12.4-slim@sha256:740d94a19218c8dd584b92f804b1158f85b0d241e5215ea26ed2dcade2b9d138 as base

FROM base as builder

COPY requirements.txt .

RUN pip install --prefix="/install" -r requirements.txt

FROM base

WORKDIR /loadgen

COPY --from=builder /install /usr/local

COPY locustfile.py .

ENV GEVENT_SUPPORT=True

ENTRYPOINT locust --host="http://${FRONTEND_ADDR}" --headless -u "${USERS:-10}" 2>&1
