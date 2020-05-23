import frida, sys


# 接受下面js代码中send出来的内容, 也可以在js中直接用consule.log
def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


# with open('test.js') as f:
#     jscode = f.read()

jscode = """
Java.perform(function () {
    // Function to hook is defined here
    // 获取一个指向某个类的指针，指向要hook的那个类
    var MainActivity = Java.use('com.example.seccon2015.rock_paper_scissors.MainActivity');

    // Whenever button is clicked
    var onClick = MainActivity.onClick;
    
    // hook类中的onClick方法, 函数的参数要和原函数一样
    onClick.implementation = function (v) {
        // Show a message to know that the function got called
        send('onClick');

        // Call the original onClick handler
        // 调用了原始方法
        onClick.call(this, v);

        // Set our values after running the original onClick handler
        // 修改了返回的值
        this.m.value = 0;
        this.n.value = 1;
        this.cnt.value = 999;

        // Log to the console that it's done, and we should have the flag!
        console.log('Done:' + JSON.stringify(this.cnt));
    };
});
"""
# 获取指定app当前运行的进程
process = frida.get_usb_device().attach('com.example.seccon2015.rock_paper_scissors')
# 注入js代码
script = process.create_script(jscode)
script.on('message', on_message)
print('[*] Running CTF')
script.load()

# 输出日志
sys.stdin.read()