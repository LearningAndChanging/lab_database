<?php
	header("content-type:text/html;chartset=utf-8");
	date_default_timezone_set("Asia/Shanghai");
	if(isset($_POST['userid']))
		$new_dir = $_POST['userid'];
	else $new_dir = "all";
	$value = array('area');
	$value_data[] = $_POST['area'];
	chdir("tmp");
	$new_m = implode("", $value_data);
	file_put_contents("parameter.txt",$new_m);
?>