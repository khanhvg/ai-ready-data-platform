FROM python@sha256:55842c72c6b3584d06ec84c731fc516b30b8a53ad262ebd085e47ab568b3bfc1 AS builder
ENV PATH=/opt/venv/bin:/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8
COPY wheelhouse/ /wheelhouse/
COPY app/requirements/runner-py312-linux-arm64.lock /build/requirements.lock
RUN python3.12 -m venv /opt/venv && /opt/venv/bin/python -m pip install --no-index --find-links=/wheelhouse --require-hashes -r /build/requirements.lock
COPY app/ /build/app/
RUN cp -a /build/app/src/lab_runner /opt/venv/lib/python3.12/site-packages/lab_runner && rm -rf /opt/venv/lib/python3.12/site-packages/pip* /opt/venv/bin/pip* && mkdir -p /image-dirs/runner
FROM python@sha256:55842c72c6b3584d06ec84c731fc516b30b8a53ad262ebd085e47ab568b3bfc1 AS sanitized
LABEL org.opencontainers.image.title="AI Ready Lab Runner" org.opencontainers.image.licenses="Apache-2.0" ai-ready.issue="9"
RUN rm -rf /usr/local/lib/python3.12/site-packages/pip* /usr/local/bin/pip*
FROM scratch
LABEL org.opencontainers.image.title="AI Ready Lab Runner" org.opencontainers.image.licenses="Apache-2.0" ai-ready.issue="9"
ENV PATH=/opt/venv/bin:/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 HOME=/run/runner PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 MALLOC_ARENA_MAX=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
COPY --from=sanitized /usr/local /usr/local
COPY --from=sanitized /usr/lib /usr/lib
COPY --from=sanitized /lib /lib
COPY --from=sanitized /etc/ssl /etc/ssl
COPY --from=sanitized /etc/passwd /etc/passwd
COPY --from=sanitized /etc/group /etc/group
COPY --from=sanitized /usr/share/zoneinfo /usr/share/zoneinfo
COPY --from=sanitized /usr/share/doc /usr/share/doc
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder --chown=65532:65532 /image-dirs/runner /run/runner
COPY app/tests/fixtures/ /opt/runner-fixtures/
COPY project/ /opt/project/
USER 65532:65532
WORKDIR /workspace
ENTRYPOINT ["python3.12","-I","-m","lab_runner.container_supervisor"]
