'''Retrieve configvar, preferably from ENV'''
import os

APPS = [
    "meets",
    "helper"
]

TOKEN = os.getenv('TOKEN')

LOG_LEVEL = "INFO"
