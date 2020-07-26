""" Package that Handles all API Request to FPL"""
# Os import sections
from aiohttp import ClientSession, TCPConnector
import asyncio
# third party import
from fpl import FPL
# local import


class FplRequestApiHandler(FPL):
    async def createSession(email: str = None , password: str=None):
        self = FplRequestApiHandler(ClientSession)
        await self.login(email, password)
        return self
        

async def main():
    fplRequestApiHandler = await FplRequestApiHandler.createSession(email="obarbier13@gmail.com",password="<>")
    print(fplRequestApiHandler.get_team(1))


if __name__ == '__main__':
    asyncio.run(main())
    
