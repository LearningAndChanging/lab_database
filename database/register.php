<!DOCTYPE html>
<html>
<head>
 <meta charset="utf-8" />
 <title>注册</title>
 <script>
 function init(){
    if(myform.username.value=="")
    {
        alert("请输入用户名");
        //将光标移动到文本框中
        myform.username.focus();
        return false;
    }
    if (myform.userpwd.value=="")
    {
        alert("请输入密码");
        myform.userpwd.focus();
        return false;
    }
    if (myform.confirm.value=="")
    {
        alert("请再输入一次密码");
        myform.confirm.focus();
        return false;
    }
    if (myform.code.value=="")
    {
        alert("请输入验证码");
        myform.code.focus();
        return false;
    }
}
</script>
<style type="text/css">
    .code{
        width:80px;
    }
    .titl{
        font-weight:bold;
        font-size:20px;
        position:relative;
        left:50px;
    }
    .bd{
        background-color:#f0f0f0;
        width:230px;
    }
</style>
</head>
<body>
<form action="regcheck.php" method="post" onsubmit="return init();" name="myform" >
<div class="bd">
    <div class="titl">用户注册</div>
    <div >
        <span >用&nbsp&nbsp户&nbsp名:</span>
        <span><input type="text" name="username" id="username" placeholder="请输入用户名" /></span>
    </div>
    <div >
        <span >密&#12288&#12288码:</span>
        <span><input type="password" name="userpwd" id="userpwd" placeholder="请输入密码" ></span>
    </div>
    <div >
        <span >确认密码:</span>
        <span><input type="password" name="confirm" id="confirm" placeholder="请再输入一次密码" ></span>
    </div>
    <div >
        <span >验&nbsp&nbsp证&nbsp码:</span>
        <span><input type="text" name="code" class="code" id="code" placeholder="请输入验证码"></span>
        <span><img src="pic.php" onClick="this.src='pic.php?nocache='+Math.random()" style="cursor:pointer"></span>
    </div>
    <div >
        <span><button class="button">立即注册</button></span>
    </div>
    <span><input  type = "hidden" name = "hidden"  value = "hidden"  /></span>
</form>
</body>
</html>