<?php
//echo $_FILES["pic"]["name"];
//echo $_FILES["pic"]["type"];
//echo $_FILES["pic"]["size"];
if(empty($_POST['cid']) || !isset($_POST['cid']) || $_POST['cid']=='' || $_POST['cid']==null){
echo 'Error !! SITEID is NULL ';
}else{
   // $upload_dir = "uploads/".$_POST['cid'];
   $upload_dir = "cid_image/".$_POST['cid'];
  if($_FILES["pic"]["size"]>1024000*102400){
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
    echo "upload OK !! FILE:".$upfile."<br>";
	// move_uploaded_file($_FILES["pic"]["tmp_name"],"uploads/.$_FILES["pic"]["name"]);
	//echo $_FILES["pic"]["name"];
    //	 echo $_POST["cid"];
  }
}
?>
