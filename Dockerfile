FROM continuumio/miniconda3

WORKDIR /app

# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "cfback", "/bin/bash", "-c"]

# The code to run when container is started:
COPY . .

# Enable entrypoint shell permissions
RUN ["chmod", "+x", "src/entrypoint.sh"]

# Don't need this because of shell script in docker-compose file
#ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "cfback", "flask", "run","--host=0.0.0.0"]
