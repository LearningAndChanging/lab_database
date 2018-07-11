<?php
#@set_time_limit(0);
#chmod('D:/phpStudy/WWW/test/drawonepng.py ',777);
$output = shell_exec("draw.py");
#echo "1";
/*
header("Content-type: image/png");
$source = imagecreatefrompng("./pythonscript/png/IVCurve.png");
$width = imagesx($source); $height = imagesy($source);
$n_width = $width /5; $n_height = $height /5;
$destination = imagecreate($n_width, $n_height);
imagecopyresampled($destination, $source,0, 0,0, 0,$n_width, $n_height, $width, $height);
imagepng($destination);
*/
#shell_exec("delete.py");
#echo $output;

/*
 function my_exec($cmd, $input='')
 {$proc=proc_open($cmd, array(0=>array('pipe', 'r'), 1=>array('pipe', 'w'), 2=>array('pipe', 'w')), $pipes);
     fwrite($pipes[0], $input);fclose($pipes[0]);
     $stdout=stream_get_contents($pipes[1]);fclose($pipes[1]);
     $stderr=stream_get_contents($pipes[2]);fclose($pipes[2]);
     $rtn=proc_close($proc);
     return array('stdout'=>$stdout,
         'stderr'=>$stderr,
         'return'=>$rtn
     );
 }
$str = "D:/phpStudy/WWW/test/drawonepng.py";  //此处为我要检测是否执行成功的指令" julia 12.jl"
var_export(my_exec($str));
    echo "finished!";
*/
?>
