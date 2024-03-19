# """
# File: api_client.py
# Author: Farid Maghraoui
# Description: This file contains an API client class for making HTTP requests to a specified base URL.
# """
# import requests
#
#
# class APIClient:
#     def __init__(self, base_url):
#         self.base_url = base_url
#
#     def get(self, endpoint, params=None):
#         url = f"{self.base_url}/{endpoint}"
#         response = requests.get(url, params=params)
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         return response.json()
#
#     def post(self, endpoint, data=None):
#         url = f"{self.base_url}/{endpoint}"
#         response = requests.post(url, json=data)
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         return response.json()
#

import aiohttp

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    async def get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                response.raise_for_status()  # Raise an exception for HTTP errors
                return await response.json()

    async def post(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                response.raise_for_status()  # Raise an exception for HTTP errors
                return await response.json()
