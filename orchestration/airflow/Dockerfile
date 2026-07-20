# Lightweight orchestration profile image: official Airflow base + the
# pipeline's Python deps (duckdb/dbt-duckdb/faker) so TaskFlow tasks can
# call the generator/loader/dbt callables directly inside the container.
FROM apache/airflow:3.1.0-python3.12

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
