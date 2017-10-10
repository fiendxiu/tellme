<?php
 
$base_path = isset($_POST['siteid']) ? 'cid_image/'.$_POST['siteid'].'/' : 'uploads/';   //接收文件目录
$imgs = array();  //定义一个数组存放上传图片的路径
$isSave = false;
if (!file_exists($base_path)) {
    mkdir($base_path);
}

foreach ($_FILES["image"]["error"] as $key => $error) {
    if ($error == UPLOAD_ERR_OK) {
        $tmp_name = $_FILES["image"]["tmp_name"][$key];
        $name = $_FILES["image"]["name"][$key];
        $uploadfile = $base_path . $name;
        $isSave = move_uploaded_file($tmp_name, $uploadfile);
        if ($isSave){
            $imgs[]=$uploadfile;
        }
    }
}

if ($isSave) {
    $array = array("message" =>"Upload Success!");
    echo json_encode($array);
} else {
    $array = array("message" => "Upload Failed...", "error"=>$name);
    echo json_encode($array,TRUE);
}
?>
