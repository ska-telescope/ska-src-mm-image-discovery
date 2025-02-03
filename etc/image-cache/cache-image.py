import requests
import urllib3
from pymongo import MongoClient, ASCENDING

# Suppress only the single InsecureRequestWarning from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# MongoDB connection
# mongo_client = MongoClient(os.getenv('MONGO_URI'))
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['image_cache']
collection = db['images']

# harbor_hosts = os.getenv('HARBOR_HOST').split()
harbor_hosts = ['images.canfar.net']

# Check if MongoDB instance is available
try:
    mongo_client.admin.command('ping')
except Exception as e:
    print("MongoDB server is not running. Please start the MongoDB server and try again.")
    exit(1)

# Create index if it does not exist
collection.create_index([('author_name', ASCENDING)], name='author_index')
collection.create_index([('types', ASCENDING)], name='types_index')
collection.create_index([('image_id', ASCENDING)], name='image_id_unique_index', unique=True)

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
                    'image_id': image_id,
                    'tag': tag,
                    'types': labels,
                    'digest': artifact['digest'],
                    'author_name': author_name,
                }

                collection.update_one(
                    {'image_id': image_id},
                    {'$set': refined_artifact},
                    upsert=True
                )
                print(f"added image {image_id}")

print("Data has been successfully inserted into MongoDB.")
