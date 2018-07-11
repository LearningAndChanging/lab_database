<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="pragma" content="no-cache">
	<meta http-equiv="cache-control" content="no-cache">
	<meta http-equiv="expires" content="0">  
	<title>太阳能电池银浆组</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<link rel="stylesheet" href="css/IVCurve.css">
    <link rel="stylesheet" href="css/style1.css">
</head>
<style type="text/css">
.parameter_change span{
	color: red;
}
button {
	border-radius: 10px;
	background-color: rgb(208,238,255);
	border-color: rgb(208,238,255);
}
</style>
<body>
<div class="main">
<div class="top_title"><p>Draw QE Curve（如果图片无法正常刷新，请单击图片进行刷新）</p></div>
<div class="container">
<div class="left">
<div class="loadfile">
<?php
	if(isset($_COOKIE["user"]))
		$user = $_COOKIE["user"];
	else
		$user = "all";
	echo "<div><input type='text'  id='user' contentEditable='true' placeholder='用户名' value=$user onchange='new_directory()'></div>"
?>
<form method="post" action="sss" enctype="multlpart/form-data" id="form_file">
<div>
<span class="file_text">
<input type="file" name="file[]" id="file" multiple="multiple"/>选择文件
</span></div>
<div id="choose_message" class="file_text">文件信息：未选择文件</div>
<div>
<!--
  <div>
  打印人员：
  <select name="printer" id="printer">
    <option value="liujian">刘健</option>
    <option value="chenyongji">陈勇吉</option>
    <option value="qiuyang">邱杨</option>
    <option value="wangxingbo">王星博</option>
    <option value="jiangxing">姜行</option>
    <option value="gaozhou">高舟</option>
    <option value="wangdawei">王大为</option>
  </select>
  </div>
  <div>
  烧结人员：
  <select name="sinter" id="sinter">
    <option value="liujian">刘健</option>
    <option value="chenyongji">陈勇吉</option>
    <option value="qiuyang">邱杨</option>
    <option value="wangxingbo">王星博</option>
    <option value="jiangxing">姜行</option>
    <option value="gaozhou">高舟</option>
    <option value="wangdawei">王大为</option>
  </select>
  </div>
  <div>
  硅片种类：
  <select name="silicon" id="silicon">
    <option value="mono">单晶硅片</option>
    <option value="poly">多晶硅片</option>
  </select>
  </div> --> 
  <input type="submit" value="上传" class="file_text" />
</div>
<div><span id="message"></span></div>
<div id="directory_message" class="file_text"></div>
</form>
</div>
<div id="directory">
</div>
</div>
<div class="right">
IVCurve:
<img src="pythonscript/png/RheoCurve.png?nocache="+Math.random() style='width:600px;height:450px; -0px 30px;cursor:pointer;' id='img1' onClick="this.src='pythonscript/png/RheoCurve.png?nocache='+Math.random()" />
<div class="drawarea">
<div class="drawarea2 parameter_change">
</div>
<div class="drawarea2 parameter_change">

参数设置：
<p>坐标区间 = <span contenteditable="true" id=areanow>请输入坐标区间，用空格分隔</span> point</p>
<button id="parameter">参数更改</button>
<button id="initial_parameter">原始参数</button>
<button id="draw_IV">绘制QE曲线</button>
</div>
</div>
</div>




</div>
</div>
</body>
<script src="js/jquery-3.1.1.js"></script>



<script type="text/javascript">
var form = document.getElementById("form_file"),upload_status = document.getElementById("message");
form.addEventListener("submit",function(e) {
	var file_data = new FormData(form);
	file_data.append("userid",$("#user").val());
	var req = new XMLHttpRequest();
	req.open("POST", "upload_file.php", true);
	req.onload = function() {
		$(upload_status).css("display","block");
		if(req.status == 200) {
			upload_status.innerHTML = "上传成功!";
		} else {
			upload_status.innerHTML = "Error:"+req.status+"上传失败";
		}
		setTimeout(function(){
			$(upload_status).css("display","none");
		},3000)
		new_directory();
	};
	req.send(file_data);
	e.preventDefault();
	
},false);
function new_directory(){
	var user = $("#user").val();
	var data = {
		userid:user,
	};
	$("#directory_message").load("readdir.php",data,function(){
	});
	setTimeout("new_directory()",60000);
}

function parameter() {
	var user = $("#user").val();
	var parameter_array = $(".parameter_change span");
	var data = {
		area : $(parameter_array[0]).html(),
		userid:user,
	};
	$.post("parameter.php",data,function(){
		alert("success");
		
	});
}
function initial_parameter() {
	var user = $("#user").val();
	var parameter_array = $(".parameter_change span");
	var initial_data = {
		area : 300,
		userid:user,
	};
	$(parameter_array[0]).html(300);
	$.post("parameter.php",initial_data,function(){
		
	});
}

function drawIV(){
	$.ajax({
	url: 'draw.php'
            
})
	window.location.reload();
	alert("作图完成!");
}


function deleteIV(){
	$.ajax({
	url: 'delete.php'
})
}

$(document).ready(function() {
	$("#file").change(function(){
		var files = document.getElementById("file").files;
		var files_message = "文件信息：<br>";
		var files_number = files.length;
		for(var i=0;i<files_number;i++) {
			files_message += (i+1)+":"+files[i].name+"\n "+parseInt(files[i].size/1024)+"kb<br>";
		}
		deleteIV();
		$("#choose_message").html(files_message);
	});
	new_directory();
	$("#draw_IV").click(function(){
		drawIV();
	});
	$("#parameter").click(function(){
		parameter();

	});
	$("#initial_parameter").click(function(){
		initial_parameter();
	});
	$("#fresh").click(function(){
		refresh();
		
	});	
})
</script>
</html>