import os
import sys
import tempfile
from enum import Enum

from openai import OpenAI, NoneType
import ujson
from packet_model import Packet


def unJsonPacket(requestBody: str,type: int):
    json_data = ujson.loads(requestBody)
    packet = Packet(type, json_data["body"], json_data["baseUrl"], json_data["apiKey"])
    return packet

class ParseType(Enum):
    Chat = 0
    Vision = 1
    Image = 2
    TTS = 3
    STT = 4


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
