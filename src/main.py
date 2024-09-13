import logging.config
from app import app

import uvicorn

import logging

import json

import os


def filter_maker(level):
    level = getattr(logging, level)

    def filter(record):
        return record.levelno <= level

    return filter


with open(os.path.join(os.getcwd(), "src/auth/config_logger.conf")) as file:
    config = json.load(file)
config['filters']['warnings_and_below']['()'] = __name__ + '.filter_maker'
logging.config.dictConfig(config)

logger = logging.getLogger()

if __name__ == "__main__":
    logger.info('Сервер запушен')
    uvicorn.run("main:app", reload=True)
    logger.info('Сервер прекратил работу')

