import logging

logger = logging.getLogger("uvicorn")

def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        logger.debug("class name: %s", cls)
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper