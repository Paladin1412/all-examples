## Scrapy
scrapy和scrapy-redis常用配置和模板


### scrapy_examples
通用配置和方法

- `__init__`初始化重写
- `scrpay`和`scrapy-redis`多配置参数
- 接收任务参数封装Request请求, 不再局限一个url
- `GET/POST(form)/POST(json)` 请求
- 统计插件
- `DOWNLOADER_MIDDLEWARES`中间件更改url
- 从start_urls中取任务改为批量取, 提升速度

### aliyun_oss
阿里云oss配置pipeline, 需要在settings中配置oss信息