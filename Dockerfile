FROM continuumio/miniconda3

# This ensure all python output is directly printed out instead of being buffered.
# This is great for ensuring the logs are realtime.
ENV PYTHONUNBUFFERED=1

WORKDIR /

# Note, in the future only copy the config here and the other files after the shell is built.
# This will be easy once the --exclude flag for copy is on stable.
COPY . .

RUN conda env create -f deliberate_practice.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "deliberate_practice", "/bin/bash", "-c"]

EXPOSE 8181
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "deliberate_practice"]
CMD ["python", "./manage.py", "runserver", "0.0.0.0:8181"]
