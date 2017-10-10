<?php
$domain= 'baidu.com';
$url='http://vote.bi-xenon.cn/checkicp.php?dm='.$domain;
$contents = file_get_contents($url);
preg_match_all("|<tr><td>状态码：</td><td>(.*)</td></tr><tr><td>查询结果|U", $contents, $out,PREG_PATTERN_ORDER);
echo $out;//$out即为是否备案的代码了，2000为已备案，其他的内容就等你就举一反三了~
?>
