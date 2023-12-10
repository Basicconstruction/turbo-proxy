from abc import ABC

import tornado


class MainHandler(tornado.web.RequestHandler, ABC):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")  # 允许所有来源访问，也可以指定特定的来源
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")  # 可接受的请求方法

    def get(self):
        self.write("Hello, Tornado!")

    def post(self):
        self.write("Hello, Tornado!")

    def options(self):
        # 响应 OPTIONS 请求
        self.set_status(204)
        self.finish()