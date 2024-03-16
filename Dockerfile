FROM alpine:latest

# Install necessary packages
RUN apk add --no-cache python3 python3-dev py3-pip postgresql-libs

# Set working directory
WORKDIR /app

# Copy Script.py to the working directory
COPY Script.py /app/

# Create and activate a virtual environment
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Upgrade pip in the virtual environment
RUN /venv/bin/pip install --upgrade pip

# Install psycopg2-binary within the virtual environment
RUN /venv/bin/pip install psycopg2-binary

# Command to run the application
CMD ["/venv/bin/python", "Script.py"]
