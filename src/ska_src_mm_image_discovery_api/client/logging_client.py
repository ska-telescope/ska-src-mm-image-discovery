import logging


def setup_logger() -> logging.Logger:
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(funcName)s() | %(message)s'
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger("uvicorn")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.propagate = False

    return logger
