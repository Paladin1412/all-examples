from mitmproxy import ctx

def request(flow):
    # 获取当前url
    url = flow.request.url
    # 更改headers
    flow.request.headers['User-Agent'] = 'MitmProxy'

def response(flow):
    log = ctx.log

    url = flow.request.url
    response = flow.response

    log.info(response.status_code)
    log.info(response.headers)
    log.info(response.cookies)
    log.info(response.content)
    
