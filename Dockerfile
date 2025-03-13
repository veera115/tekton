# Template for python 3.13 Dockerfile
FROM python:3.13-slim

# Default labels
LABEL title="Python-ExampleService"

# Default build arguments

# Set working directory
WORKDIR /app

# Copy project files
COPY github-template-python-service/ .

# Set environment variables
ENV PYTHONPATH="/app/lib/:/app"
ENV ASPNETCORE_URLS="http://localhost:8080"

#opentelemetry configuration
ENV OTEL_SERVICE_NAME="Python-ExampleService"
ENV OTEL_EXPORTER_OTLP_ENDPOINT="http://collector-release-opentelemetry-collector.default.svc.cluster.local:4317"
ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED="true"

# Install opentelemetry dependencies
RUN pip install opentelemetry-distro
RUN pip install opentelemetry-exporter-otlp
RUN opentelemetry-bootstrap -a install


# Expose port, avoid port numbers <1025
EXPOSE 8080

# Run the application
ENTRYPOINT ["opentelemetry-instrument", "python3", "src/app/app.py"]

