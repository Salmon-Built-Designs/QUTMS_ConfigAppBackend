FROM continuumio/miniconda3

WORKDIR /app

# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "config-hub-env", "/bin/bash", "-c"]

# The code to run when container is started:
COPY backend/main.py /app
ENTRYPOINT ["conda", "run", "-n", "config-hub-env", "python", "main.py"]