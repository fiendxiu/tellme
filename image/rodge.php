<?php
//echo $_FILES["pic"]["name"];
//echo $_FILES["pic"]["type"];
//echo $_FILES["pic"]["size"];
$upload_dir = "uploads/".$_POST['cid'];

if($_FILES["pic"]["size"]>512*1024){
	echo $_POST["name"];
	echo "invalidate file type";
}else{
    if(!file_exists($upload_dir)){
            mkdir($upload_dir);
        }
      $upfile=$upload_dir.'/'.$_FILES['pic']["name"];
    
    if(file_exists($upfile)){
        $upfile=$upload_dir.'/'.rand(0,100).$_FILES['pic']['name'];
        }
       
    move_uploaded_file($_FILES["pic"]["tmp_name"],$upfile);
   echo "<font color='red'>已经成功上传文件,文件名为:</font> <font color='blue'>".$upfile."<br>";
	// move_uploaded_file($_FILES["pic"]["tmp_name"],"uploads/.$_FILES["pic"]["name"]);
	//echo $_FILES["pic"]["name"];
    //	 echo $_POST["cid"];
}
?>
