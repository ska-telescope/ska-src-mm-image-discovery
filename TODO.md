# TODO

- [ ] Add Gateway API/Nginx for service 
- [X] Add `rest/server`.py
- [ ] Modify docker/init.sh for launching new server
- [X] Update .gitlab-ci.yml
- [X] Complete docker-compose.yml, etc/docker/init.sh, Dockerfile
- [x] Mongodb connection
- [ ] Check Router in fastapi
- [ ] Check suitable UI
- [ ] Separate images/search
- [ ] Add indexing on location for every software type
- [ ] Add indexing on metadata.specification for docker-container only
- [ ] Explore this query later, when add software metadata is in development

```js
collection.update_one(
    {'executable.location': {'$in': software_metadata.executable.location}},
    {'$set': software_metadata.dict()},
    upsert = True
)
```
- [ ] Separate images/search