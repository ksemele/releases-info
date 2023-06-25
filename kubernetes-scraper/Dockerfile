FROM python:3.11.3 AS builder
COPY requirements.txt .

# install dependencies to the local user directory (eg. /root/.local)
RUN pip install --user -r requirements.txt



FROM python:3.11.3-slim-buster
WORKDIR /app

# copy only the dependencies that are needed for our application and the source files
COPY --from=builder /root/.local /root/.local
COPY ./source .

# update PATH
ENV PATH=/root/.local:$PATH

# make sure you include the -u flag to have our stdout logged
# CMD [ "python", "-u", "./main.py" ]
# CMD [ "bash", "./run.sh" ]
CMD [ "python", "scraper.py" ]


# RUN apt update && apt upgrade -y && pip install poetry

# WORKDIR /app

# COPY . .

# RUN poetry config virtualenvs.create false
# RUN poetry install