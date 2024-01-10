from enum import Enum
from typing import Optional, List

from openai._types import NotGiven
from openai.types.chat import ChatCompletionMessageParam


class GPTType(Enum):
    ChatStream = 0,
    Image = 1,
    Speech = 2,
    Transcription = 3,
    Translation = 4


def _create_body_data(packet_type, bodyPacket):
    if packet_type == GPTType.ChatStream.value:
        return ChatStreamPacket(**bodyPacket)
    elif packet_type == GPTType.Image.value:
        return ImagePacket(**bodyPacket)
    else:
        raise ValueError("Invalid packet_type")


class Packet:
    def __init__(self, type, body, baseUrl: Optional[str] = None, apiKey: Optional[str] = None):
        self.type = type
        self.body = self._create_body_data(type, body)
        self.baseUrl = baseUrl
        self.apiKey = apiKey

    def _create_body_data(self, packet_type, bodyPacket):
        if packet_type == 0 or packet_type == 1:
            return ChatStreamPacket(**bodyPacket)
        elif packet_type == 2:
            return ImagePacket(**bodyPacket)
        elif packet_type == 3:
            return TTSPacket(**bodyPacket)
        elif packet_type == 4 :
            return STTPacket(**bodyPacket)
        else:
            raise ValueError("Invalid packet_type")

    def __str__(self):
        return f"Packet: type={self.type}, body_data={self.body}, baseUrl={self.baseUrl}, apiKey={self.apiKey}"


class ChatStreamPacket:
    def __init__(self, model: str,
                 messages: List[ChatCompletionMessageParam],
                 max_tokens: int,
                 stream: bool,
                 frequency_penalty: Optional[float] | NotGiven = NotGiven,
                 presence_penalty: Optional[float] | NotGiven = NotGiven,
                 temperature: Optional[float] | NotGiven = NotGiven,
                 top_p: Optional[float] | NotGiven = NotGiven
                 ):
        self.model = model
        self.messages = messages
        self.frequency_penalty = frequency_penalty
        self.max_tokens = max_tokens
        self.presence_penalty = presence_penalty
        self.stream = True
        self.temperature = temperature
        self.top_p = top_p

    def __str__(self):
        return f"ChatStreamPacket: model={self.model}," \
               f" frequency_penalty={self.frequency_penalty}, " \
               f"messages={self.messages}, max_tokens={self.max_tokens}, " \
               f"presence_penalty={self.presence_penalty}, " \
               f"temperature={self.temperature}, top_p={self.top_p} "


class ImagePacket:
    def __init__(self, model, prompt, n: Optional[str] | NotGiven = NotGiven, size: Optional[str] | NotGiven = NotGiven,
                 quality: Optional[str] | NotGiven = NotGiven,
                 response_format: Optional[str] | NotGiven = NotGiven,
                 style: Optional[str] | NotGiven = NotGiven
                 ):
        self.model = model
        self.prompt = prompt
        self.n = n
        self.size = size
        self.quality = quality
        self.response_format = response_format
        self.style = style

    def __str__(self):
        return (f"ImagePacket: model={self.model}, prompt={self.prompt}, "
                f"n={self.n}, size={self.size}, quality={self.quality}, "
                f"response_format={self.response_format}, style={self.style}")


class TTSPacket:
    def __init__(self, model: str, input: str, voice: str, response_format: Optional[str] | NotGiven = NotGiven,
                 speed: Optional[float] | NotGiven = NotGiven
                 ):
        self.model = model
        self.input = input
        self.voice = voice
        self.speed = speed
        self.response_format = response_format

    def __str__(self):
        return f"TTSPacket(model={self.model}, input={self.input}, voice={self.voice}, speed={self.speed} response_format={self.response_format})"


class STTPacket:
    def __init__(self, model, transcription: bool, prompt: Optional[str] | NotGiven = NotGiven,
                 language: Optional[str] | NotGiven = NotGiven,
                 temperature: Optional[float] | NotGiven = NotGiven
                 ):
        self.model = model
        self.transcription = transcription
        self.prompt = prompt
        self.language = language
        self.temperature = temperature

    def __str__(self):
        return f"STTPacket(model={self.model}, transcription={self.transcription}, prompt={self.prompt}, language={self.language}, temperature={self.temperature})"
