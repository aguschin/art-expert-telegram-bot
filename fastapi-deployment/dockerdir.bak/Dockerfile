FROM python:3.9.16-slim
WORKDIR /app


# install Git in case something in requirements.txt will be installed from Git repo
RUN apt-get update && apt-get -y upgrade && apt-get install --no-install-recommends -y git && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt && pip cache purge
RUN pip install mlem==0.4.12 && pip cache purge

COPY . ./
ENV MLEM_DEBUG=true
ENV MLEM_EXTENSIONS=mlem.contrib.callable,mlem.contrib.github,mlem.contrib.gitlabfs,mlem.contrib.bitbucketfs,mlem.contrib.pip,mlem.contrib.requirements,mlem.contrib.venv


CMD sh run.sh