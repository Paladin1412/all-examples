def request(flow):
    # 获取当前url
    url = flow.request.url
    # 更改headers
    flow.request.headers['User-Agent'] = 'MitmProxy'

def response(flow):
    url = flow.request.url

    response = flow.response

    print(response.status_code)
    print(response.headers)
    print(response.cookies)
    print(response.content)
    
