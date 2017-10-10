<?
$uptypes=array(
    'image/jpg', 
    'image/jpeg',
    'image/png',
    'image/pjpeg',
    'image/gif',
    'image/bmp',
    'image/x-png'
);
?>
<html>
<head>
<title>IMAGESUPLOAD</title>
</head>
<script language="javascript">
    function checkfile(){
        var ofile = document.getElementById('upfile').value;
        if(ofile == ""){
            window.alert("请选择上传文件");
            return false;
        }    
        return true;
    }    
</script>
<body>
<form enctype="multipart/form-data" method="post" name="upform" onSubmit="return checkfile();">
上传文件1:    <input name="upfile[]" id="upfile" type="file"><br /> 
上传文件2:    <input name="upfile[]" type="file" /><br />
上传文件3:    <input name="upfile[]" type="file" /><br />
上传文件4:    <input name="upfile[]" type="file" /><br />
上传文件5:    <input name="upfile[]" type="file" /><br />
<input type="submit" value="上传"><br>
<font color="red" size="2pt">允许上传的文件类型为:<?=implode(',',$uptypes);?></font>
</form>
</body>
</html>

<?php
if($_SERVER['REQUEST_METHOD'] == 'POST'){
 $count=count($_FILES['upfile']['name']);

 $max_size_upfile='2097152';
 $cid =$_GET[cid];
 $upload_dir = "cid_image/$cid";
   // echo $cid;
   
for($i=0;$i<$count;$i++){
        if(empty($_FILES['upfile']['tmp_name'][$i])){
        continue;
        }
        if($_FILES['upfile']['size'][$i]>$max_size_upfile){
            echo $_FILES['upfile']['name'][$i].'文件大小超过最大！';
            continue;
        }
    //    if(!in_array($_FILES['upfile']['type'][$i],$uptypes)){
     //       echo '只能上传图片类型!';
     //       continue;
      //  }
        if($_FILES['upfile']['error'][$i]!=UPLOAD_ERR_OK){
            echo $_FILES['upfile']['name'][$i].'文件上传不成功!';
            continue;
        }
      if(!file_exists($upload_dir)){
            mkdir($upload_dir);
        }
  
    $upfile=$upload_dir.'/'.$_FILES['upfile']['name'][$i];
     $fname = $_FILES['upfile']['tmp_name'][$i];
    $image_info = getimagesize($fname);
    
    if(file_exists($upfile)){
        $upfile=$upload_dir.'/'.rand(0,100).$_FILES['upfile']['name'][$i];
        }
    move_uploaded_file($_FILES['upfile']['tmp_name'][$i],$upfile);
    
  //  echo $_FILES['upfile']['name'][$i].'上传成功<br />';
      $str_file=$upload_dir.'/'.$_FILES['upfile']['name'][$i];
      echo "<font color='red'>已经成功上传文件,文件名为:</font> <font color='blue'>".$upfile."<br>";
    echo "宽度:".$image_info[0];
    echo "长度:".$image_info[1];
    echo "<br> 大小:".$_FILES['upfile']['size'][$i]."bytes<br></font>";
echo "图片预览:<br>";
     
    echo "<img src=\"".$upfile."\">";
    echo "<br>";
    }
}
?>


