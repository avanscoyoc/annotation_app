# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the environment.yaml file to the container
COPY environment.yaml .

# Install necessary system dependencies including curl and tkinter
RUN apt-get update && apt-get install -y \
    bash \
    curl \
    python3-tk \
    && apt-get clean

# Install Conda (using the ARM64 version for M1/M2 Macs)
RUN curl -sSL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh -o miniconda.sh \
    && bash miniconda.sh -b -p /opt/conda \
    && rm miniconda.sh \
    && /opt/conda/bin/conda init bash

# Add Conda to PATH
ENV PATH=/opt/conda/bin:$PATH

# Create the environment using environment.yaml
RUN conda env create -f environment.yaml

# Activate the environment
SHELL ["conda", "run", "-n", "annotation_app", "/bin/bash", "-c"]

# Copy the rest of the application code into the container
COPY . /app

# Expose the port your app will run on (if necessary)
EXPOSE 5000

# Set the command to run the application (starting from main.py)
CMD ["python", "main.py"]
