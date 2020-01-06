from urlparse import urlparse

def request(flow):
    # 获取当前url
    url = flow.request.url
    # 更改headers
    flow.request.headers['User-Agent'] = 'MitmProxy'

def response(flow):
    response = flow.response
    # 获取响应内容
    content = response.content

    log = ctx.log

    tmp = urlparse(flow.request.url)
    
    log.info(str(tmp.path))
    log.info(str(tmp.query))
    log.info(str(response.status_code))
    log.info(str(response.headers))
    log.info(str(response.cookies))
    log.info(str(response.text))