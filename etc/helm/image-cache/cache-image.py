import os

import requests
import urllib3
from pymongo import MongoClient, ASCENDING

# Suppress only the single InsecureRequestWarning from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

harbor_hosts = os.getenv('HARBOR_HOST', 'images.canfar.net').split()
print(f"Harbor hosts: {harbor_hosts}")

# MongoDB connection
mongo_db_uri = os.getenv('MONGO_URI', 'mongodb://root:password@localhost:27017/?authSource=admin')
mongo_db_name = os.getenv('MONGO_DB_NAME', 'software_metadata')
collection_name = os.getenv('MONGO_COLLECTION_NAME', 'docker-container')

mongo_client = MongoClient(mongo_db_uri)
db = mongo_client[mongo_db_name]
collection = db[collection_name]

# Check if MongoDB instance is available
try:
    mongo_client.admin.command('ping')
except Exception as e:
    print("MongoDB server is not running. Please start the MongoDB server and try again.")
    exit(1)

# Create index if it does not exist
collection.create_index([('executable.location', ASCENDING)], name='image_location_unique_index', unique=True)

for harbor_host in harbor_hosts:
    url = f"https://{harbor_host}/api/v2.0/projects?page_size=100"
    project_url = f"https://{harbor_host}/api/v2.0/projects"

    print(f"Fetching the images host: {url}")
    response = requests.get(url, verify=False)
    projects = response.json()

    for project in projects:
        project_name = project['name']
        author_name = project['owner_name']
        project_data = requests.get(f"{project_url}/{project_name}/repositories?page_size=-1", verify=False).json()

        if not project_data:
            continue

        for repo in project_data:
            repo_name = repo['name']
            name = repo_name.split('/')[-1]
            repo_data = requests.get(
                f"{project_url}/{project_name}/repositories/{name}/artifacts?detail=true&with_label=true&page_size=-1",
                verify=False).json()

            for artifact in repo_data:
                if not artifact.get('tags', [{}]):
                    continue
                tag = artifact.get('tags', [{}])[0].get('name')

                if not tag:
                    continue

                image_id = f"{harbor_host}/{project_name}/{name}:{tag}"
                labels = artifact.get('labels', [])

                if not labels:
                    print(f"No labels found for {image_id}")
                    continue

                labels = [label['name'] for label in labels]

                refined_artifact = {
                    "executable": {
                        "location": image_id,
                        "name": name,
                        "type": "docker-container",
                    },
                    "metadata": {
                        "description": f"This is a {",".join(labels)} {name} image",
                        "version": tag,
                        "tag": tag,
                        "authorName": author_name,
                        "digest": artifact['digest'],
                        "specifications": labels
                    },
                    "resources": {
                        "cores": {
                            "min": 5,
                            "max": 15
                        },
                        "memory": {
                            "min": 3,
                            "max": 9
                        }
                    }
                }

                collection.update_one(
                    {'executable.location': image_id},
                    {'$set': refined_artifact},
                    upsert=True
                )
                print(f"added image {image_id}")

print("Data has been successfully inserted into MongoDB.")
