<?php
	header("content-type:text/html;chartset=utf-8");
	date_default_timezone_set("Asia/Shanghai");
	if(isset($_POST['userid']))
		$new_dir = $_POST['userid'];
	else $new_dir = "all";
	chdir("upload");
	if(!is_dir($new_dir)){
	    mkdir($new_dir);
	    shell_exec("chmod 777 $new_dir");
	    shell_exec("cp ../m/simulation.m $new_dir/simulation.m");
	    shell_exec("cp ../m/accorsoc.m $new_dir/accorsoc.m");
	}
	setcookie("user",$new_dir,time()+3600);
	if(chdir("$new_dir")){
	$dh = opendir(".");
	$file_number = 0;
	if($dh) {
		echo '当前文件夹：',$new_dir,'<br>';
		while(($file_name = readdir($dh)) != FALSE){
				echo iconv('gbk','utf-8',$file_name);
				echo "<br>";
			$file_number++;
		}
	}
	closedir($dh);
}

?>