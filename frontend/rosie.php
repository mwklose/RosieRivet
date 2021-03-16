<?php
$source = $_FILES["upfile"]["tmp_name"];
$destination = $_FILES["upfile"]["name"];
move_uploaded_file($source, $destination);
echo "OK";
