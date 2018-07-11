<?php
header("Content-Type:text/html;charset=utf-8");
// A list of permitted file extensions
$allowed = array('xls','xlsx');

if(isset($_FILES['upl']) && $_FILES['upl']['error'] == 0){

	$extension = pathinfo($_FILES['upl']['name'], PATHINFO_EXTENSION);

	if(!in_array(strtolower($extension), $allowed)){
		echo '{"status":"error"}';
        echo "<script>alert('上传失败！');</script>"; 
		exit;
	}
$a=urldecode($_FILES['upl']['name']);
$a=mb_convert_encoding($a, 'GB2312', 'UTF-8');
	if(move_uploaded_file($_FILES['upl']['tmp_name'], './uploads/'.$a)){
		echo '{"status":"success"}';
		exit;
	}
}

echo '{"status":"error"}'; 
exit;
?>