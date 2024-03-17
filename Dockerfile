FROM alpine:latest

# Install Python and necessary packages
RUN apk add --no-cache python3 python3-dev py3-pip postgresql-libs

# Set working directory
WORKDIR /app

# Copy your Python script into the container
COPY script.py /app/

# Create a virtual environment
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Upgrade pip in the virtual environment
RUN /venv/bin/pip install --upgrade pip

# Install psycopg2-binary within the virtual environment
RUN /venv/bin/pip install psycopg2-binary

# Run the Python script
CMD ["/venv/bin/python3", "script.py"]
