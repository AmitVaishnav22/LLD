class HttpRequest:
    def __init__(self,url,method=None,timeout=None,headers=None,query_params=None,body=None):
        self.url = url
        self.method = method if method else "GET"
        self.timeout = timeout if timeout else 30
        self.headers = headers if headers else {}
        self.query_params = query_params if query_params else {}
        self.body = body

    def setUrl(self, url):
        self.url = url

    def setMethod(self, method):
        self.method = method

    def setTimeout(self, timeout):
        self.timeout = timeout

    def setHeaders(self, keys, value):
        self.headers[keys] = value

    def setQueryParams(self, keys, value):
        self.query_params[keys] = value

    def setBody(self, body):
        self.body = body

    
    def excute(self):
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

if __name__ == "__main__":
    request1 = HttpRequest("https://api.example.com")
    request2 = HttpRequest("https://api.example.com", method="POST")
    request3 = HttpRequest("https://api.example.com", method="PUT", timeout=60)

    request4 = HttpRequest("https://api.example.com")
    request4.setMethod("POST")
    request4.setHeaders("Content-Type", "application/json")
    request4.setQueryParams("key", "12345")
    request4.setBody('{"name": "Aditya"}')
    request4.setTimeout(60)
    request4.excute()

# problems with this approach:
# 1. The constructor can become unwieldy with many parameters.
# 2. It can be unclear which parameters are optional and which are required.
# 3. Setting parameters after object creation can lead to inconsistent states. 
