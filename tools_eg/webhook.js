const http = require('http');
const exec = require('child_process').exec

var port = 8081
var basePath = '~/home/www-data/'
var branch = 'develop'

http.createServer(function (req, res) {
    // 定义了一个post变量，用于暂存请求体的信息
    var body = '';     

    // 通过req的data事件监听函数，每当接受到请求体的数据，就累加到post变量中
    req.on('data', function(chunk){    
        body += chunk;
    });
    
    // 在end事件触发后，通过querystring.parse将post解析为真正的POST请求格式，然后向客户端返回。
    req.on('end', function(){    
        try{
            parseBody = JSON.parse(body)
            let now = new Date().toLocaleString();
            
            
            console.log(`
                *******************************************
                ${now}
                user                    : ${parseBody.user_name}
                commit_total            : ${parseBody.commits.length}
                repository_name         : ${parseBody.repository.name}
                repository_homepage     : ${parseBody.repository.homepage}
                repository_description  : ${parseBody.repository.description}
    
                __________________________________________
                *******************************************
            `)
    
            // 拉取代码
            let command = `cd ${basePath}/${parseBody.repository.name} && git pull origin ${branch}`
            exec(command, () => {
                console.log(`git pull success from branch: ${branch}, command:${command}`)
                res.write('success')
                res.end()
            }, (error) => {
                console.log(`error = ${error}`)
                res.write(`error = ${error}`)
                res.end()
            })
        } catch(e){
            console.log(`body = ${body} error = ${e}`);
        }

    });
    

}).listen(port);

// 终端打印如下信息
console.log(`Server running at port: ${port}`);



/*
gitlab post数据格式如下

{
    "object_kind":"push",
    "event_name":"push",
    "before":"5583aa1b40b698c5eb192859a0ed316467ad420e",
    "after":"5234a6053dfc1820bfdf10f5e141df7a0d886e1b",
    "ref":"refs/heads/master",
    "checkout_sha":"5234a6053dfc1820bfdf10f5e141df7a0d886e1b",
    "message":null,
    "user_id":1680,
    "user_name":"qin.jianxun",
    "user_username":"qin.jianxun",
    "user_email":"",
    "user_avatar":"https://secure.gravatar.com/avatar/306d358cde149a2be5913e78ba7ee676?s': '80&amp;d=identicon",
    "project_id":15122,
    "project":{
        "id":15122,
        "name":"spider_admin_api",
        "description":"spider对接后台api",
        "web_url":"https://git.wemomo.com/handsome/spider_admin_api",
        "avatar_url":null,
        "git_ssh_url":"git@git.wemomo.com:handsome/spider_admin_api.git",
        "git_http_url":"https://git.wemomo.com/handsome/spider_admin_api.git",
        "namespace":"handsome",
        "visibility_level":0,
        "path_with_namespace":"handsome/spider_admin_api",
        "default_branch":"master",
        "ci_config_path":"",
        "homepage":"https://git.wemomo.com/handsome/spider_admin_api",
        "url":"git@git.wemomo.com:handsome/spider_admin_api.git",
        "ssh_url":"git@git.wemomo.com:handsome/spider_admin_api.git",
        "http_url":"https://git.wemomo.com/handsome/spider_admin_api.git"
    },
    "commits":[
        {
            "id":"5234a6053dfc1820bfdf10f5e141df7a0d886e1b",
            "message":"update port",
            "title":"update port",
            "timestamp":"2020-08-04T21:18:11 08:00",
            "url":"https://git.wemomo.com/handsome/spider_admin_api/-/commit/5234a6053dfc1820bfdf10f5e141df7a0d886e1b",
            "author":{
                "name":"MOMO",
                "email":"qin.jianxun@immomo.com"
            },
            "added":[

            ],
            "modified":[
                "run.sh"
            ],
            "removed":[

            ]
        },
        {
            "id":"3cb54fe32a5539852d1f8be856044332db864c13",
            "message":"fix time query range",
            "title":"fix time query range",
            "timestamp":"2020-08-04T17:03:46 08:00",
            "url":"https://git.wemomo.com/handsome/spider_admin_api/-/commit/3cb54fe32a5539852d1f8be856044332db864c13",
            "author":{
                "name":"MOMO",
                "email":"qin.jianxun@immomo.com"
            },
            "added":[

            ],
            "modified":[
                "api/service/job.py",
                "api/service/task.py"
            ],
            "removed":[

            ]
        },
        {
            "id":"5583aa1b40b698c5eb192859a0ed316467ad420e",
            "message":"加入返回统计参数",
            "title":"加入返回统计参数",
            "timestamp":"2020-08-04T16:36:25 08:00",
            "url":"https://git.wemomo.com/handsome/spider_admin_api/-/commit/5583aa1b40b698c5eb192859a0ed316467ad420e",
            "author":{
                "name":"MOMO",
                "email":"qin.jianxun@immomo.com"
            },
            "added":[

            ],
            "modified":[
                "api/dao/mongo/cnt_spider.py",
                "api/dao/mongo/job_execution.py",
                "api/libs/spiders.py",
                "api/router/task.py",
                "api/service/job.py",
                "api/service/task.py"
            ],
            "removed":[

            ]
        }
    ],
    "total_commits_count":3,
    "push_options":{

    },
    "repository":{
        "name":"spider_admin_api",
        "url":"git@git.wemomo.com:handsome/spider_admin_api.git",
        "description":"spider对接后台api",
        "homepage":"https://git.wemomo.com/handsome/spider_admin_api",
        "git_http_url":"https://git.wemomo.com/handsome/spider_admin_api.git",
        "git_ssh_url":"git@git.wemomo.com:handsome/spider_admin_api.git",
        "visibility_level":0
    }
}
*/