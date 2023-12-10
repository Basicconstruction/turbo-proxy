from abc import ABC

import tornado

from handlers.tools import unJsonPacket, eraseDefault
from openai_provider import provideOpenai


class VisionHandler(tornado.web.RequestHandler, ABC):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")  # 允许所有来源访问，也可以指定特定的来源
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")  # 可接受的请求方法

    async def post(self):
        self.set_header('Content-Type', 'text/event-stream')
        self.set_header('Cache-Control', 'no-cache')
        self.set_header('Connection', 'keep-alive')
        try:
            authorization_header = self.request.headers.get("Authorization")
            # TODO 添加验证，如果有
            json_str = self.request.body.decode('utf-8')
            packet = unJsonPacket(json_str)
            inner = packet.body
            openai_client = provideOpenai()
            openai_client = eraseDefault(packet, openai_client)
            max_tokens = inner.max_tokens
            if max_tokens >= 4096:
                max_tokens = 4096
            response = openai_client.chat.completions.create(
                model=inner.model,
                messages=inner.messages,
                stream=True,  # 是否开启流式输出
                max_tokens=max_tokens,
                temperature=inner.temperature,
            )

            # 按流读取数据
            for message in response:
                if type(message.choices[0].delta.content) is str:
                    self.write(message.choices[0].delta.content)
                await self.flush()
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
