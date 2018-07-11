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
if ($_FILES["file"]["error"][0] > 0) {
    echo "Return Code: " . $_FILES["file"]["error"][0] . "<br />";
        print_r($_FILES['file']);
} else {
    for($i=0;$i<count($_FILES["file"]['name']);$i++) {
        echo "Upload: " . $_FILES["file"]["name"][$i] . "<br />";
        echo "Type: " . $_FILES["file"]["type"][$i] . "<br />";
        echo "Size: " . ($_FILES["file"]["size"][$i] / 1024) . " Kb<br />";
        echo "Temp file: " . $_FILES["file"]["tmp_name"][$i] . "<br />";
        $utf_name = iconv("UTF-8","gbk", $_FILES["file"]["name"][$i]);
        move_uploaded_file($_FILES["file"]["tmp_name"][$i],"$new_dir/" . $utf_name);
        echo "Stored in: " . "$new_dir/" . $utf_name;
    }
}
?>