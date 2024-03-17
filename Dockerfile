FROM alpine:latest

# Install Python and necessary packages
RUN apk add --no-cache python3 python3-dev py3-pip postgresql-libs

# Set working directory
WORKDIR /app

# Copy your Python script into the container
COPY script.py /app/

# Install dependencies
RUN pip3 install psycopg2-binary

# Run the Python script
CMD ["python3", "script.py"]
