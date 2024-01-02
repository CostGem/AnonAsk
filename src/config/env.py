from os import getenv
from typing import Optional

from dotenv import load_dotenv, find_dotenv

IS_DOCKER: Optional[str] = getenv("IS_DOCKER")

if IS_DOCKER:
    dotenv_path = find_dotenv(filename=".env.docker")
else:
    dotenv_path = find_dotenv(filename=".env.local")

load_dotenv(dotenv_path=dotenv_path)
