<?php 
session_start();
//注册处理界面 regcheck.php
 if(isset($_POST["hidden"]) && $_POST["hidden"] == "hidden") 
 { 
 $user = trim($_POST["username2"]);//trim()函数移除字符串两侧的空白字符
 $psw = md5(trim($_POST["userpwd2"])); 
 $psw_confirm = md5(trim($_POST["confirm2"])); 
 $code = $_POST["code2"];
 $regp = $_POST["groups"];
 if($user == "" || $psw == "" || $psw_confirm == "" || $regp == "" ) 
 { 
 echo "<script>alert('请确认信息完整性！'); history.go(-1);</script>"; 
 }
 else if($code != $_SESSION['ver_code2']){
 echo "<script>alert('验证码不正确，请重新输入！'); history.go(-1);</script>";
 }
 else if((strlen($user)-mb_strlen($user,"UTF8"))/2 < 2){
 echo "<script>alert('请输入中文姓名作为账号！'); history.go(-1);</script>"; 
 } 
 else if((strlen($user)-((strlen($user)-mb_strlen($user,"UTF8"))/2*3)) >0){
 echo "<script>alert('请不要在账号中输入字母和数字！'); history.go(-1);</script>"; 
 } 
 else if(strlen($psw)<6){
 echo "<script>alert('密码长度过短！'); history.go(-1);</script>"; 
 }
 else   
 { 
 if($psw == $psw_confirm) 
 { 
 $conn = mysqli_connect("localhost","root","root"); //连接数据库,帐号密码为自己数据库的帐号密码 
 if(mysqli_errno($conn)){
 echo mysqli_error($conn);
 exit;
 }
 mysqli_select_db($conn,"userdb"); //选择数据库 
 mysqli_set_charset($conn,'utf8'); //设定字符集 
 $sql = "select username from user where username = '$user'"; //SQL语句
 $result = mysqli_query($conn,$sql); //执行SQL语句 
 $num = mysqli_num_rows($result); //统计执行结果影响的行数 
 
 if($num) //如果已经存在该用户 
 { 
 echo "<script>alert('用户名已存在'); history.go(-1);</script>"; 
 } 
 else //不存在当前注册用户名称 
 {
     
 $ip=getIp(); // 把ip地址转换成整型
 $time=time();
 $sql_insert = "insert into `user` (`username`,`userpwd`,`createtime`,`createip`,`researchgroup`) values('" . $user . "','" . $psw ."','".$time."','".$ip."','".$regp."')"; 
 $res_insert = mysqli_query($conn,$sql_insert); 
 if($res_insert) 
 { 
 echo "<script>alert('注册成功！');window.location.href='../index.php';</script>"; 
 } 
 else 
 { 
 echo "<script>alert('系统繁忙，请稍候！'); history.go(-1);</script>"; 
 } 
 } 
 } 
 else 
 { 
 echo "<script>alert('密码不一致！'); history.go(-1);</script>"; 
 } 
 } 
 } 
 else 
 { 
 echo "<script>alert('提交未成功！');</script>"; 
 } 
 //ip处理
function getIp()
    {

        if(!empty($_SERVER["HTTP_CLIENT_IP"]))
        {
            $cip = $_SERVER["HTTP_CLIENT_IP"];
        }
        else if(!empty($_SERVER["HTTP_X_FORWARDED_FOR"]))
        {
            $cip = $_SERVER["HTTP_X_FORWARDED_FOR"];
        }
        else if(!empty($_SERVER["REMOTE_ADDR"]))
        {
            $cip = $_SERVER["REMOTE_ADDR"];
        }
        else
        {
            $cip = '';
        }
        preg_match("/[\d\.]{7,15}/", $cip, $cips);
        $cip = isset($cips[0]) ? $cips[0] : 'unknown';
        unset($cips);
        $nip=preg_replace("/\./",'', $cip);
        return $nip;
    }
?> 