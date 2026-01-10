class HttpRequest:
    def __init__(self):
        self.method = None
        self.url = None
        self.headers = {}
        self.query_params = {}
        self.body = ""
        self.timeout = 0

    def execute(self):
        print(f"Executing {self.method} request to {self.url}")
        if self.query_params:
            print("Query Parameters:")
            for k, v in self.query_params.items():
                print(f"  {k}={v}")
        if self.headers:
            print("Headers:")
            for k, v in self.headers.items():
                print(f"  {k}: {v}")
        if self.body:
            print("Body:")
            print(self.body)
        print(f"Timeout: {self.timeout} seconds")
        print("Request executed successfully.")

class HttpRequestBuilder:
    def __init__(self):
        self.req = HttpRequest()

    def setUrl(self, url):
        self.req.url = url
        return self

    def setMethod(self, method):
        self.req.method = method
        return self

    def setTimeout(self, timeout):
        self.req.timeout = timeout
        return self

    def setHeaders(self, key, value):
        self.req.headers[key] = value
        return self

    def setQueryParams(self, key, value):
        self.req.query_params[key] = value
        return self

    def setBody(self, body):
        self.req.body = body
        return self

    def build(self):
        if not self.req.url:
            raise ValueError("URL is required")
        if not self.req.method:
            self.req.method = "GET"
        if self.req.timeout <= 0:
            self.req.timeout = 30  # default timeout
        return self.req


class HttpDirector:
    @staticmethod
    def createGetRequest(url):
        return (
            HttpRequestBuilder()
            .setUrl(url)
            .setMethod("GET")
            .setTimeout(30)
            .build()
        )
    @staticmethod
    def createPostRequest(url, body):
        return (
            HttpRequestBuilder()
            .setUrl(url)
            .setMethod("POST")
            .setBody(body)
            .setTimeout(60)
            .build()
        )
    
if __name__ == "__main__":
    get_request = HttpDirector.createGetRequest("https://api.example.com/data")
    get_request.execute()

    post_request = HttpDirector.createPostRequest(
        "https://api.example.com/submit", '{"name": "John", "age": 30}'
    )
    post_request.execute()