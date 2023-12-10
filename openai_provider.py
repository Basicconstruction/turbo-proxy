from typing import List

from openai import OpenAI


class Configuration:
    def __init__(self, baseUrl: str, apiKey: str, allowKeys: List[str], free: bool = False):
        self.baseUrl = baseUrl
        self.apiKey = apiKey
        self.allowKeys = allowKeys
        self.free = free


def provideOpenai():
    return OpenAI(
        #
        base_url='',
        api_key=''
    )

def init_openai_config():
    return True
