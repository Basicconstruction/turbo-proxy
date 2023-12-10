import ujson


class Image:
    def __init__(self,revised_prompt:str,url:str,b64_json:str):
        self.revised_prompt = revised_prompt
        self.url = url
        self.b64_json = b64_json

    def to_json(self):
        return {
            "revised_prompt": self.revised_prompt,
            "url": self.url,
            "b64_json": self.b64_json
        }

    def __str__(self):
        return f"Image(revised_prompt='{self.revised_prompt}', url='{self.url}', b64_json={self.b64_json})"


def encodeImage(obj):
    return ujson.dumps(obj, default=lambda o: o.to_json(), indent=2)
