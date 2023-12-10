import base64
import os
import random
import time
from abc import ABC

import tornado
import ujson

from handlers import tools
from handlers.tools import eraseDefault, unJsonPacket, path
from openai_provider import provideOpenai


class TTSHandler(tornado.web.RequestHandler, ABC):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")  # 允许所有来源访问，也可以指定特定的来源
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")  # 可接受的请求方法

    async def post(self):
        self.set_header('Content-Type', 'text/event-stream')
        self.set_header('Cache-Control', 'no-cache')
        self.set_header('Connection', 'keep-alive')
        try:
            # authorization_header = self.request.headers.get("Authorization")
            absolutePath = tools.path() + "\\tmp"
            if not os.path.exists(absolutePath):
                os.makedirs(absolutePath)

            files = self.request.files
            prompt = ""
            for file_field in files:
                for file_data in files[file_field]:
                    prompt += file_data['body'].decode("utf-8")
            #
            packetStr = self.get_body_argument('packet')
            packet = unJsonPacket(packetStr)
            inner = packet.body
            path = F"{time.time()}{random.randint(1,1000)}"
            file_path = absolutePath+"\\"+path
            openai_client = provideOpenai()
            openai_client = eraseDefault(packet, openai_client)
            response = openai_client.audio.speech.create(
                model=inner.model,
                voice=inner.voice,
                input=prompt+inner.input,
                response_format=inner.response_format,
                speed=inner.speed
            )
            response.stream_to_file(file_path)

            with open(file_path, 'rb') as file:
                file_content = file.read()
                file_base64 = base64.b64encode(file_content).decode('utf-8')  # 将文件内容编码为Base64字符串
                self.write(file_base64)
            # 删除文件
            os.remove(file_path)
            print("delete tmp file",file_path)
        except Exception as e:
            print("except", e)
            self.write(str(e))
        await self.flush()
        await self.finish()

    def options(self):
        self.set_header('Content-Type', 'text/event-stream')
        self.set_header('Cache-Control', 'no-cache')
        self.set_header('Connection', 'keep-alive')
        self.set_status(204)
        self.finish()


