class UserRepository:
    def __init__(self, session):
        self.session = session

    async def get_user(self):
        return self.session.get("")

    @classmethod
    async def get_user_a(sesssion):
        return sesssion.get("")



async def main():
    repo = UserRepository(session=1)
    await repo.get_user()

    await UserRepository.get_user_a(sesssion=1)

