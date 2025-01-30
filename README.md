# SKA SRC Mm-Image-Discovery API

This API has been generated from a templated SRCNet API. Please fill out this section with details about what the API
does.

[TOC]

## Authentication

The following sections assume that the API has been integrated with both IAM and the Permissions API. This involves:

- Creating an IAM client (for Services to obtain access via a `client_credentials` grant),
- Passing the credentials (id/secret) to either `.env` files (docker-compose) or in the `values.yaml` (helm), and
- Creating the permissions policy and loading it in to the Permissions API.

Access can then be granted for either a User or Service.

### User

To access this API as a user, the user needs to have first authenticated with the SRCNet and to have exchanged the token 
resulting from this initial authentication with one that allows access to this specific service. See the Authentication 
Mechanism and Token Exchange Mechanism sections of the Authentication API for more specifics.

### Service

For service-to-service interactions, it is possible to obtain a token via a ***client_credentials*** grant to the
ska-src-mm-image-discovery-api IAM client.

## Authorisation

Hereafter, the caller (either a user or another service) is assumed to have a valid token allowing access to this API. 
Authenticated requests are then made by including this token in the header.

The token audience must also match the expected audience, also defined in the mm-image-discovery-api permissions 
policy (default: “mm-image-discovery-api”).

### Restricting user access to routes using token scopes

The presented token must include a specific scope expected by the service to be permitted access to all API routes. This 
scope is defined in the mm-image-discovery-api permissions policy 
(default: “mm-image-discovery-api-service”). 

**This scope must also be added to the IAM permissions client otherwise the process of token instrospection will drop 
this scope.**

## Development

Makefile targets have been included to facilitate easier and more consistent development against this API. The general 
recipe is as follows:

1. Depending on the fix type, create a new major/minor/patch branch, e.g. 
    ```bash
    $ make patch-branch NAME=some-name
    ```
    Note that this both creates and checkouts the branch.
2. Make your changes.
3. Create new code samples if necessary.
   ```bash
   $ make code-samples
   ```
4. Add your changes to the branch:
    ```bash
   $ git add ...
    ```
5. Either commit the changes manually (if no version increment is needed) or bump the version and commit, entering a 
   commit message when prompted:
    ```bash
   $ make bump-and-commit
    ```
6. Push the changes upstream when ready:
    ```bash
   $ make push
    ```

Note that the CI pipeline will fail if python packages with the same semantic version are committed to the GitLab 
Package Registry.

### Code Structure

The repository is structured as follows:

```
.
├── .env.template
├── .gitlab-ci.yml
├── bin
├── docker-compose.yml
├── Dockerfile
├── etc
│   ├── docker
│   │   └── init.sh
│   ├── helm
│   │   ├── Chart.yaml
│   │   ├── templates
│   │   └── values.yaml.template
│   └── scripts
│       ├── generate-code-samples.sh
│       ├── increment-app-version.sh
│       └── increment-chart-version.sh
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
├── src
│   └── 
│       ├── client
│       ├── common
│       ├── models
│       └── rest
├── TODO.md
└── VERSION
```

The API endpoint logic is within the `src/rest/server.py` with `/ping` and `/health` endpoints provided as a reference.

### Bypassing AuthN/Z

AuthN/Z can be bypassed for development by setting `DISABLE_AUTHENTICATION=yes` in the environment.

## Deployment

Deployment is managed by docker-compose or helm.

The docker-compose file can be used to bring up the necessary services locally i.e. the REST API, setting the mandatory
environment variables. Sensitive environment variables, including those relating to the IAM client, should be kept in
`.env` files to avoid committing them to the repository.

There is also a helm chart for deployment onto a k8s cluster.

### Example via docker-compose

Edit the `.env.template` file accordingly and rename to `.env`, then:

```bash
eng@ubuntu:~/SKAO/ska_src_mm_image_discovery_api$ docker-compose up
```

When the service has been deployed, navigate to http://localhost:8080/v1/www/docs/oper to view the (swagger) frontend.

Similarly, you can test the service locally by calling http://localhost:8080/v1/ping.

### Example via Helm

After editing the `values.yaml` (template in `/etc/helm/`):

```bash
$ create namespace ska_src_mm_image_discovery_api
$ helm install --namespace ska_src_mm_image_discovery_api ska_src_mm_image_discovery_api .
```

## References
