FROM python@sha256:9bb659dc6d5218917236f3711e866a5634bb4c2f208de9d4533aa4863f57c1d3 AS builder
ENV PATH=/opt/venv/bin:/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8
COPY wheelhouse/ /wheelhouse/
COPY app/requirements/runner-py312-linux-arm64.lock /build/requirements.lock
RUN python3.12 -m venv /opt/venv && /opt/venv/bin/python -m pip install --no-index --find-links=/wheelhouse --require-hashes -r /build/requirements.lock
COPY app/ /build/app/
RUN /opt/venv/bin/python -m pip install --no-index --no-deps --no-build-isolation /build/app && rm -rf /opt/venv/lib/python3.12/site-packages/pip* /opt/venv/bin/pip*
FROM python@sha256:9bb659dc6d5218917236f3711e866a5634bb4c2f208de9d4533aa4863f57c1d3
LABEL org.opencontainers.image.title="AI Ready Lab Runner" org.opencontainers.image.licenses="Apache-2.0" ai-ready.issue="9"
ENV PATH=/opt/venv/bin:/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 HOME=/run/runner PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
COPY --from=builder /opt/venv /opt/venv
COPY project/ /opt/project/
RUN rm -rf /usr/local/lib/python3.12/site-packages/pip* /usr/local/bin/pip* && find /opt/project /opt/venv -type d -exec chmod 0555 {} + && find /opt/project /opt/venv -type f -exec chmod 0444 {} +
USER 65532:65532
WORKDIR /workspace
ENTRYPOINT ["python3.12","-I","-m","lab_runner.container_supervisor"]
