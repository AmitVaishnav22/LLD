class HttpRequest:
    def __init__(self):
        self.url = None
        self.method = None
        self.timeout = 0
        self.headers = {}
        self.query_params = {}
        self.body = None
    
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

class UrlBuilder:
    def __init__(self,req):
        self.req = req
    def setUrl(self, url):
        self.req.url = url
        return MethodBuilder(self.req)

class MethodBuilder:
    def __init__(self, req):
        self.req = req
    def setMethod(self, method):
        self.req.method = method
        return HeaderBuilder(self.req)

class HeaderBuilder:
    def __init__(self, req):
        self.req = req
    def setHeaders(self, key, value):
        self.req.headers[key] = value
        return TimeoutBuilder(self.req)

class TimeoutBuilder:
    def __init__(self, req):
        self.req = req
    def setTimeout(self, timeout):
        self.req.timeout = timeout
        return OptionalBuilder(self.req)

class OptionalBuilder:
    def __init__(self,req):
        self.req = req
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

class HttpRequestBuilder:
    @staticmethod
    def builder():
        req = HttpRequest()
        return UrlBuilder(req)
    
if __name__ == "__main__":
    request = (
        HttpRequestBuilder
        .builder()
        .setUrl("http://example.com/api")
        .setMethod("POST")
        .setHeaders("Content-Type", "application/json")
        .setTimeout(60)
        .setBody('{"key": "value"}')
        .build()
    )
    request.execute()


# why not interfaces in python like java.
# beacause python abc,abstract base class doesnot care about the order of method calls
# so we use separate builder classes for each step to enforce the order of method calls