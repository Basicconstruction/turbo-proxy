import tornado

from handlers.chatHandler import ChatStreamHandler
from handlers.defultHandler import MainHandler
from handlers.imageHandler import ImageHandler
from handlers.sttHandler import STTHandler
from handlers.ttsHandler import TTSHandler
from handlers.visionHandler import VisionHandler


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/chat", ChatStreamHandler),
        (r"/image", ImageHandler),
        (r"/tts", TTSHandler),
        (r"/stt", STTHandler),
        (r"/vision", VisionHandler)
    ])
