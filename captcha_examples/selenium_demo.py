from selenium.webdriver import Chrome, ActionChains, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager


# 初始化
option = ChromeOptions()
option.add_argument('no-sandbox')
option.add_argument('disable-dev-shm-usage')
option.add_argument('--proxy-server=http://127.0.0.1:8080')

web = Chrome(ChromeDriverManager().install(), options=option)


# 反检测
# 移除webdriver
script = 'Object.defineProperty(navigator, "webdriver", {get: () => undefined,});'
web.execute_script(script)


# 保存canvas内容
canvas = web.find_element_by_css_selector('#dx_captcha_basic_bg_1 > canvas')
# get the canvas as a PNG base64 string
canvas_base64 = web.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
# decode
canvas_png = base64.b64decode(canvas_base64)
# save to a file
with open(bg_img, 'wb') as f:
    f.write(canvas_png)


paths = [[1, 2], [3, 4]]
# 按住滑块不放
ActionChains(web).click_and_hold(slide).perform()
time.sleep(0.5)

for path in paths:
    x, y = path
    ActionChains(web).move_by_offset(xoffset=x, yoffset=y).perform()

# 释放滑块
ActionChains(web).release().perform()