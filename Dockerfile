FROM python:3.8-bullseye

USER root

RUN groupadd user
RUN adduser --system --no-create-home --disabled-password --shell /bin/bash user

COPY --chown=user . /opt/ska-src-mm-image-discovery-api

RUN cd /opt/ska-src-mm-image-discovery-api && python3 -m pip install -e . --extra-index-url https://gitlab.com/api/v4/projects/48060714/packages/pypi/simple

WORKDIR /opt/ska-src-mm-image-discovery-api

ENTRYPOINT ["/bin/bash", "etc/docker/init.sh"]
