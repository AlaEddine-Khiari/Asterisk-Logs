FROM alpine:latest

# Install Python and necessary packages
RUN apk del --purge $(apk info | grep -v '^python3' | grep -v '^musl' | grep -v '^apk-tools' | grep -v '^busybox' | cut -d' ' -f1)
RUN apk add --no-cache python3 python3-dev py3-pip postgresql-libs

# Set working directory
WORKDIR /app

# Create the recordings directory
RUN mkdir -p /ext/recordings
RUN chmod 777 /ext/recordings  

# Copy your Python script into the container
COPY app.py /app/

# Create a virtual environment
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Upgrade pip in the virtual environment
RUN /venv/bin/pip install --upgrade pip

# Install psycopg2-binary within the virtual environment
RUN /venv/bin/pip install Flask psycopg2-binary

# Expose port 5000
EXPOSE 4000

# Run the Python script
CMD ["/venv/bin/python3", "app.py"]
