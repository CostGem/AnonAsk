from os import getenv
from typing import Optional

from dotenv import load_dotenv, find_dotenv

IS_DOCKER: Optional[str] = getenv("IS_DOCKER")

general_dotenv_path: str = find_dotenv(filename=".env.general")

if IS_DOCKER:
    special_dotenv_path: str = find_dotenv(filename=".env.docker")
else:
    special_dotenv_path: str = find_dotenv(filename=".env.local")

load_dotenv(dotenv_path=general_dotenv_path)
load_dotenv(dotenv_path=special_dotenv_path)
