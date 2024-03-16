FROM alpine:latest

# Install necessary packages
RUN apk add --no-cache python3 python3-dev py3-pip postgresql-libs

# Set working directory
WORKDIR /app

# Copy script.py and app.py to the working directory
COPY . /app/

# Create and activate a virtual environment
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Upgrade pip in the virtual environment
RUN /venv/bin/pip install --upgrade pip

# Install Flask and psycopg2-binary within the virtual environment
RUN /venv/bin/pip install psycopg2-binary

# Command to run the application
CMD ["/venv/bin/python", "script.py"]
