#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import time
import random
import json
import requests
import thehive4py

from thehive4py.api import TheHiveApi
from thehive4py.query import *
import thehive4py.models

from walkoff_app_sdk.app_base import AppBase

class MicrosoftSecurity(AppBase):
    __version__ = "1.0.0"
    app_name = "oauth2-example"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    async def authenticate(self, access_token, refresh_token):
        s = requests.Session()
        s.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer %s" % access_token
        }

        return s

    # UserAuthenticationMethod.ReadWrite.All
    async def reset_password(self, access_token, refresh_token, userId, passwordId, newPassword=""):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(access_token, refresh_token)

        url = "https://graph.microsoft.com/beta/users/%s/authentication/passwordMethods/%s/resetPassword" % (userId, passwordId)
        response = session.post(url)
        print(response.status_code)
        return response.text

    # UserAuthenticationMethod.ReadWrite.All
    async def get_password_methods(self, access_token, refresh_token):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(access_token, refresh_token)

        url = "https://graph.microsoft.com/beta/me/authentication/passwordMethods"
        response = session.get(url)
        print(response.status_code)
        return response.text
    
if __name__ == "__main__":
    asyncio.run(MicrosoftSecurity.run(), debug=True)
