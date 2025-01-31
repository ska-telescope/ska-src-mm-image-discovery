import traceback
from functools import wraps

import requests
from fastapi import HTTPException

from src.ska_src_mm_image_discovery_api.common.exceptions import CustomException, CustomHTTPException


def handle_exceptions(func):
    """ Decorator to handle server exceptions. """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            detail = f"HTTP error occurred: {e}, response: {e.response.text}"
            raise HTTPException(status_code=status_code, detail=detail)
        except HTTPException as e:
            raise e
        except CustomException as e:
            raise Exception(message=e.message)
        except CustomHTTPException as e:
            raise HTTPException(status_code=e.http_error_status, detail=e.message)
        except Exception as e:
            detail = "General error occurred: {}, traceback: {}".format(
                repr(e), ''.join(traceback.format_tb(e.__traceback__)))
            raise HTTPException(status_code=500, detail=detail)
    return wrapper