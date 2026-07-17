<?php
ini_set("SMTP","ssl://smtp.gmail.com");
ini_set("smtp_port","465");
$headers = 'MIME-Version: 1.0' . '\r\n';
$headers .= 'Content-type: text/html; charset=iso-8859-1' . '\r\n';
$headers .= 'From: {myEmail}' . '\r\n';
mail("{rnikhil275@gmail.com}","test subject","test body",$headers);
?>