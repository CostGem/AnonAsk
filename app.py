from src.containers.app import AppContainer
from src.main import start_bot

if __name__ == "__main__":
    container: AppContainer = AppContainer()
    container.init_resources()

    start_bot()
