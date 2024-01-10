import asyncio
from abc import ABC
from openai import NoneType
from typing import List
import tornado.web
from handlers.tools import unJsonPacket, eraseDefault, ParseType
from openai_model import Image, encodeImage
from openai_provider import provideOpenai


class ImageHandler(tornado.web.RequestHandler, ABC):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")  # 允许所有来源访问，也可以指定特定的来源
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")  # 可接受的请求方法

    async def post(self):
        self.set_header('Content-Type', 'text/event-stream')
        self.set_header('Cache-Control', 'no-cache')
        self.set_header('Connection', 'keep-alive')
        try:
            json_str = self.request.body.decode('utf-8')
            packet = unJsonPacket(json_str,ParseType.Image.value)
            inner = packet.body
            openai_client = provideOpenai()
            openai_client = eraseDefault(packet, openai_client)
            imageList: List[Image] = await process_multiple_requests(openai_client, inner)
            datas = encodeImage(imageList)
            self.write(datas)
        except Exception as e:
            print("except", e)
            self.write(str(e))
            # print()
            # self.write("error")
        await self.flush()
        await self.finish()
        # print("closed")

    def options(self):
        # 响应 OPTIONS 请求
        self.set_header('Content-Type', 'text/event-stream')
        self.set_header('Cache-Control', 'no-cache')
        self.set_header('Connection', 'keep-alive')
        self.set_status(204)
        self.finish()


async def process_request(openaiClient, inner):
    try:
        # print("start")
        response = openaiClient.images.generate(
            model=inner.model,
            prompt=inner.prompt,
            size=inner.size,
            n=1,
            response_format=inner.response_format,
            style=inner.style,
            quality=inner.quality
        )
        # print("error ")
        image = response.data[0]
        # print(image)
        rImage: Image
        if isinstance(image.b64_json, NoneType):
            # print("is None")
            rImage = Image(image.revised_prompt, image.url, '')
        else:
            rImage = Image(image.revised_prompt, image.url, image.b64_json)
        # print(encodeImage(rImage))
        return rImage  # 返回响应的数据部分
    except Exception as e:
        print(f"Exception in processing request here: {e}")
        return None


# 异步处理多个请求
async def process_multiple_requests(openaiClient, inner):
    tasks = []

    # 创建多个异步任务
    for _ in range(inner.n):
        task = asyncio.create_task(process_request(openaiClient, inner))
        tasks.append(task)

    # 并发执行所有任务
    responses = await asyncio.gather(*tasks)
    images: List[Image] = []
    # 处理每个响应
    for response_data in responses:
        if response_data:
            if isinstance(response_data, Image):
                images.append(response_data)
    return images
