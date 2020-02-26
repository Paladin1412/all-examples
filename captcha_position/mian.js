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