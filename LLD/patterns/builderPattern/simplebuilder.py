class HttpRequest:
    def __init__(self):
        self.url=None
        self.method=None
        self.headers={}
        self.query_params={}
        self.body=""
        self.timeout=None

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
        self.req=HttpRequest()

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
        if self.req.timeout<=0:
            self.req.timeout = 30
        return self.req

if __name__ == "__main__":
    request=(
        HttpRequestBuilder()
        .setUrl("https://api.example.com")
        .setMethod("POST")
        .setHeaders("Content-Type", "application/json")
        .setQueryParams("key", "12345")
        .setBody('{"name": "Aditya"}')
        .setTimeout(60)
        .build()
    )
    request.execute()
