FROM python:3.13-bullseye

USER root

RUN groupadd user
RUN adduser --system --no-create-home --disabled-password --shell /bin/bash user

WORKDIR /opt/ska-src-mm-image-discovery-api

COPY --chown=user . .

RUN python3 -m pip install -e . --extra-index-url https://gitlab.com/api/v4/projects/48060714/packages/pypi/simple

ENTRYPOINT ["/bin/bash", "etc/docker/init.sh"]
