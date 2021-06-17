import os
from contextlib import suppress

APP_PATH = os.path.dirname(__file__)

with suppress(Exception):
	ROOT_PATH, _ = os.path.dirname(os.path.abspath(__file__)).split("/src")