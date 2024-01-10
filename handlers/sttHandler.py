import os
import random
import time
from abc import ABC

import tornado
from openai._types import NotGiven

from handlers import tools
from handlers.tools import eraseDefault, unJsonPacket, ParseType
from openai_provider import provideOpenai


class STTHandler(tornado.web.RequestHandler, ABC):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")  # 允许所有来源访问，也可以指定特定的来源
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")  # 可接受的请求方法

    async def post(self):
        self.set_header('Content-Type', 'text/event-stream')
        self.set_header('Cache-Control', 'no-cache')
        self.set_header('Connection', 'keep-alive')
        try:
            absolutePath = tools.path() + "\\tmp"
            if not os.path.exists(absolutePath):
                os.makedirs(absolutePath)
            files = self.request.files
            path = F"{time.time().__floor__()}{random.randint(1, 1000)}.mp3"
            file_path = absolutePath + "\\" + path
            for file_field in files:
                if len(files[file_field]) < 1:
                    self.write("没有传输音频文件")
                    return
                file0 = files[file_field][0]
                with open(file_path, "wb") as fileTmp:
                    fileTmp.write(file0['body'])
            print("path: " + file_path)

            packetStr = self.get_body_argument('packet')
            packet = unJsonPacket(packetStr,ParseType.STT.value)
            inner = packet.body
            openai_client = provideOpenai()
            openai_client = eraseDefault(packet, openai_client)
            openedMp3 = open(file_path, "rb")
            print(inner)
            if (inner.transcription):
                language = ''
                if not (isinstance(inner.language, NotGiven) or inner.language is NotGiven):
                    language = inner.language
                temperature = 0
                if not (isinstance(inner.temperature, NotGiven) or inner.temperature is NotGiven):
                    temperature = inner.temperature
                prompt = ""
                if not (isinstance(inner.prompt, NotGiven) or inner.prompt is NotGiven):
                    prompt = inner.prompt
                transcript = openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=openedMp3,
                    language=language,
                    prompt=prompt,
                    response_format="text",
                    temperature=temperature
                )
                self.write(transcript.text)
            else:
                print("转译")
                temperature = 0
                if not isinstance(inner.temperature, NotGiven):
                    temperature = inner.temperature
                prompt = ""
                if not isinstance(inner.prompt, NotGiven):
                    prompt = inner.prompt
                # 转译
                translation = openai_client.audio.translations.create(
                    model="whisper-1",
                    file=openedMp3,
                    prompt=prompt,
                    response_format="text",
                    temperature=temperature
                )
                self.write(translation.text)
            time.sleep(0.2)
            openedMp3.close()
            os.remove(file_path)
        except Exception as e:
            print("except", e)
            self.write(str(e))
        await self.flush()
        await self.finish()

    def options(self):
        # 响应 OPTIONS 请求
        self.set_header('Content-Type', 'text/event-stream')
        self.set_header('Cache-Control', 'no-cache')
        self.set_header('Connection', 'keep-alive')
        self.set_status(204)
        self.finish()
