FROM python:3.11-slim

# This Dockerfile defines a simple simulation container for an ISR node.
# The container will replay telemetry from the `telemetry/` directory and
# optionally respond to mission control messages via MQTT or another bus.

WORKDIR /app

# Copy only the necessary files for the simulation
COPY telemetry/ ./telemetry/
COPY telemetry/parse_telemetry.py ./

# Install minimal runtime dependencies. Avoid caching for smaller images.
RUN pip install --no-cache-dir pyyaml paho-mqtt

# By default the container runs the parser against the sample stream to
# produce an event log. In a real node this command would launch the
# full node software and join the fleet network.
CMD ["python", "parse_telemetry.py", "--input", "telemetry/sample_stream.json", "--output", "telemetry/event_log.csv"]

LABEL org.opencontainers.image.source="https://github.com/23Nimbus/aether-wraith-isr-fleet"
