FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the project code into the container
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# cleanup
RUN apt-get clean && \
rm -rf /var/lib/apt/lists/* && \
rm -rf /tmp/*

# Set a non-root user
RUN useradd -ms /bin/bash faridmagh \
    && chown -R faridmagh:faridmagh /app

USER faridmagh
