<?php
$target_url = "http://172.19.222.203:5000/predict";
$file_name_with_full_path = $_FILES['file']['tmp_name'];
if (function_exists('curl_file_create')) { // php 5.5+
  $cFile = curl_file_create($file_name_with_full_path);
} else { // php < 5.5
  $cFile = '@' . realpath($file_name_with_full_path);
}
$post = array('file'=> $cFile);
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL,$target_url);
curl_setopt($ch, CURLOPT_POST,1);
curl_setopt($ch, CURLOPT_POSTFIELDS, $post);
curl_setopt($ch, CURLOPT_RETURNTRANSFER,1);
$result=curl_exec ($ch);
curl_close ($ch);
echo $result;
?>
