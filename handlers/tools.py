import os
import sys
import tempfile

from openai import OpenAI, NoneType
import ujson
from packet_model import Packet


def unJsonPacket(requestBody: str):
    # print(requestBody)
    json_data = ujson.loads(requestBody)
    # print("not error "+json_data)
    packet = Packet(json_data["type"], json_data["body"], json_data["baseUrl"], json_data["apiKey"])
    return packet


def eraseDefault(packet: Packet, openai: OpenAI):
    if (not isinstance(packet.baseUrl, NoneType)) and len(packet.baseUrl.strip()) > 0:
        openai.base_url = packet.baseUrl
    else:
        openai.base_url = 'https://api.openai.com/v1'
    if (not isinstance(packet.apiKey, NoneType)) and len(packet.apiKey.strip()) > 0:
        openai.api_key = packet.apiKey
    return openai


def path():
    temp_directory = tempfile.gettempdir()
    return temp_directory
    # return os.path.dirname(sys.executable)
