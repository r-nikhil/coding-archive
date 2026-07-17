<?php
require 'Slim/Slim.php';
//require 'RedBean/rb.php';
\Slim\Slim::registerAutoloader();
session_cache_limiter(false);
session_start();
$connection = mysqli_connect("localhost", "root", "", "doctornow");
// include 'db.php';

$app = new \Slim\Slim(); // pass an associative array to this if you want to configure the settings


// you wanted the id of doctor/patient while logging in. But I am giving you everything when you log in and redirtect to profile_doctor. Will that do ?

include "endpoint/patient/login.php";
include "endpoint/patient/profile.php";
include "endpoint/patient/signup.php";

include "endpoint/doctor/login.php";
include "endpoint/doctor/profile.php";
include "endpoint/doctor/signup.php";





$app->run();
?>
