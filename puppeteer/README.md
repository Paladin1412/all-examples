主要记录puppeteer处理滑动验证码的流程和代码片段

## js获取鼠标滑动轨迹
目的: 记录滑动验证码的正确轨迹, 供后续分析使用

使用: 
1. 新建 `snippet` 后运行
2. 执行 `JSON.stringify(positions)` 后复制, 第一个元素是开始点击位置需要手动移除

#### web端
```js
/*
 获取滑动验证码路径
 */

positions = []

function mousedown(event){
	console.log('pos: ' + event.pageX + ',' + event.pageY);
    positions.push([event.pageX, event.pageY]);
	// 鼠标移动事件
	document.addEventListener('mousemove', mousemove, false);
}

function mousemove(event){
	console.log('pos: ' + event.pageX + ',' + event.pageY);

	start_x = positions[0][0]
	start_y = positions[0][1]

	sub_x = event.pageX - start_x
	sub_y = event.pageY - start_y
	
	positions.push([sub_x, sub_y])
	// 鼠标松开事件
	document.addEventListener('mouseup', remove, false);
}

function remove(event){
	// 移除鼠标所有事件
	document.removeEventListener('mousemove', mousemove, false);
}

// 鼠标点击事件
document.addEventListener('mousedown', mousedown, false);
```
#### 移动端
和web端主要区别是事件不一样
```js
/*
 获取滑动验证码路径
 */

positions = []

function touchstart(event){
	console.log('pos: ' + event.touches[0].pageX + ',' + event.touches[0].pageY);
    positions.push([event.touches[0].pageX, event.touches[0].pageY]);
	// 鼠标移动事件
	document.addEventListener('touchmove', touchmove, false);
}

function touchmove(event){
	console.log('pos: ' + event.touches[0].pageX + ',' + event.touches[0].pageY);

	start_x = positions[0][0]
	start_y = positions[0][1]

	sub_x = event.touches[0].pageX - start_x
	sub_y = event.touches[0].pageY - start_y
	
	positions.push([sub_x, sub_y])

    console.log(JSON.stringify(positions))
	// 鼠标松开事件
	document.addEventListener('touchend', touchend, false);
}

function touchend(event){
	// 移除鼠标所有事件
	document.removeEventListener('touchmove', touchmove, false);
}

// 鼠标点击事件
document.addEventListener('touchstart', touchstart, false);
```


## 获取cookie方式
主要是puppeteer获取cookie的方式
```js
// 获取当前域的cookie存储到map中
var cookies = {};
var tmp_cookies = await page.cookies();
tmp_cookies.forEach(function (e) {
    cookies[e.name] = e.value;
});

// 获取所有cookie
var all_cookies = await page._client.send('Network.getAllCookies');

```

## 拖动滑块的js代码
以下是js进行拖动滑块的代码, 由浏览器环境去执行, 可以在Chrome中的snippet中进行调试

web端和移动端同样是 事件 不一样, 不同的事件可能触发不一样的反爬虫策略, 需要做前期调研
#### web端
主要使用以下事件
- `mousedown`
- `mousemove`
- `mouseup`

```js
// 创建鼠标事件
var createEvent = function (eventName, ofsx, ofsy) {
    var evt = document.createEvent('MouseEvents');
    evt.initMouseEvent(eventName, true, false, null, 0, 0, 0, ofsx, ofsy, false, false, false, false, 0, null);
    return evt;
};

// 开始移动
async function move(obj) {
    // 点击鼠标
    obj.dispatchEvent(createEvent('mousedown', 0, 0));

    console.log('move create mousedown event ...');

    var move_time = 0;

    for (i = 0; i < poses.length; i++) {
        x_pos = poses[i][0];
        // 移动
        obj.dispatchEvent(createEvent('mousemove', x_pos, 0));

        var sleep_time = Math.random();
        move_time += sleep_time;
        await sleep(sleep_time)
    }

    console.log('tb_captcha time: ', move_time);

    // 松开
    obj.dispatchEvent(createEvent('mouseup', x_pos, 0))
}
```
#### 移动端
主要使用以下事件
- `touchstart`
- `touchmove`
- `touchend`

```js
// 模拟手指拖动
function sendTouchEvent(evenvName, element, x, y) {
    const touchObj = new Touch({
      identifier: Date.now(),
      target: element,
      clientX: x,
      clientY: y,
      radiusX: 2.5,
      radiusY: 2.5,
      rotationAngle: 10,
      force: 0.5,
    });
  
    const touchEvent = new TouchEvent(evenvName, {
      cancelable: true,
      bubbles: true,
      touches: [touchObj],
      targetTouches: [],
      changedTouches: [touchObj],
      shiftKey: true,
    });
  
    element.dispatchEvent(touchEvent);
}

// 开始移动
async function move(obj) {
    sendTouchEvent('touchstart', obj, 0, 0);

    var move_time = 0;

    for (i = 0; i < poses.length; i++) {
        x_pos = poses[i][0];
        sendTouchEvent('touchmove', obj, x_pos, 0);
        var sleep_time = Math.random();
        move_time += sleep_time;
        await sleep(sleep_time)
    }

    console.log('tb_captcha time: ', move_time);

    obj.dispatchEvent(createEvent('touchend'))
}
```

## 恢复浏览器环境
场景: 已经有一个网站的登录cookie, 打开一个全新的浏览器直接注入cookie来恢复登录状态

工具: 
- `editThisCookie`: Chrome插件, 可以一键导出所有cookie进行快速验证

```js
// 所有cookie, 可能有多个在一个数组中
const cookies = [
    {
        "domain": "localhost", // google.com, yahoo.com etc. Without the host
        "hostOnly": true,
        "httpOnly": true,
        "name": "connect.sid", // here is the actual cookie name
        "path": "/",
        "sameSite": "no_restriction",
        "secure": false,
        "session": true,
        "storeId": "0",
        "value": "s%3AliYZ-M8urEQLfgn2_kSG_FIPwVTr5VQs.5rrJW7hzuXebekzTRgPYFTYri5nljhGCp8Dz%2FgLoSN4", // and the value
        "id": 1
    },
    {
        "domain": "localhost", // google.com, yahoo.com etc. Without the host
        "hostOnly": true,
        "httpOnly": true,
        "name": "connect.sid", // here is the actual cookie name
        "path": "/",
        "sameSite": "no_restriction",
        "secure": false,
        "session": true,
        "storeId": "0",
        "value": "s%3AliYZ-M8urEQLfgn2_kSG_FIPwVTr5VQs.5rrJW7hzuXebekzTRgPYFTYri5nljhGCp8Dz%2FgLoSN4", // and the value
        "id": 1
    }
]

const puppeteer = require('puppeteer');


const browser = await puppeteer.launch()

const page = await browser.newPage()
// 注入cookie
await page.setCookie(...cookies)

await page.goto('https://www.paypal.com/signin')
await page.screenshot({
    path: 'paypal_login.png'
})
await browser.close()
```

#### 参考
- https://stackoverflow.com/questions/50418994/pass-signed-cookie-to-puppeteer


