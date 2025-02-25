# SKA SRC Mm-Image-Discovery API

This service is used to register and retrieve metadata for SKA Image containers.

This service has 2 endpoints `/image/search` and `/image/register` for searching by name or by metadata and registering a new image.

## API and response

### Search for images based on type

#### Request

```http
GET /v1/image/search?type=headless
```

#### Response
```json
[
	{
		"image_id": "images.canfar.net/canfar/base-3.12:v0.4.1",
		"author_name": "majorb",
		"types": [
			"headless"
		],
		"digest": "sha256:d3a1bfad817a2208752e1722c67dcbfad9510f0b4fd21f529af75bd8fb3b0ac8",
		"tag": "v0.4.1"
	},
	{
		"image_id": "images.canfar.net/canucs/test:1.2.5",
		"author_name": "admin",
		"types": [
			"headless"
		],
		"digest": "sha256:8e3823ee29e30861b4f30261aba9938cd43c82eb327c61a948d74d55334fd485",
		"tag": "1.2.5"
	}
]
```

### Search by image name

#### Request

```http
GET /v1/image/search?image_id=images.canfar.net/canfar/base-3.12:v0.4.1
```

#### Response
```json
{
   "image_id": "images.canfar.net/canfar/base-3.12:v0.4.1",
   "author_name": "majorb",
   "types": [
      "headless"
   ],
   "digest": "sha256:d3a1bfad817a2208752e1722c67dcbfad9510f0b4fd21f529af75bd8fb3b0ac8",
   "tag": "v0.4.1"
}
```

### Register a new image

#### Request

```http
POST /v1/image/register?image_url=images.canfar.net/canfar/base-3.12:v0.4.1
```

```json
{
    "image_id": "images.canfar.net/canfar/base-3.12:v0.4.1",
    "author_name": "majorb",
    "types": [
        "headless"
    ],
    "digest": "sha256:d3a1bfad817a2208752e1722c67dcbfad9510f0b4fd21f529af75bd8fb3b0ac8",
    "tag": "v0.4.1"
}
```



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
