FROM node:22.14.0 AS ui-builder

WORKDIR /ui
COPY ui/package*.json ./
RUN npm install
COPY ui/ ./
RUN npm run build



# Run the app
FROM python:3.13-bullseye as backend-builder

USER root

RUN groupadd user
RUN adduser --system --no-create-home --disabled-password --shell /bin/bash user

RUN apt-get update && apt-get install -y skopeo

WORKDIR /opt/ska-src-mm-image-discovery-api
COPY --chown=user --from=ui-builder /ui/dist ./ui/dist

COPY --chown=user requirements.txt requirements.txt
# RUN python3 -m pip install -r requirements.txt --extra-index-url https://gitlab.com/api/v4/projects/48060714/packages/pypi/simple
RUN python3 -m pip install -r requirements.txt

COPY --chown=user src ./src
COPY --chown=user etc/docker ./etc/docker


EXPOSE 8080

ENTRYPOINT ["/bin/bash", "etc/docker/init.sh"]
