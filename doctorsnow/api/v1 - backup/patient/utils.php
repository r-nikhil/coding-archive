<?php

//this file will contain small functions which can be required by frontend for getting some data, not for actions

$app->get('/patient/getid', function() use ($app) {
  try {
   
	if (isset($_SESSION['patId']))
	{
	$arr=array('status' => '200', 'message' => 'Sending id','query_result'=> $_SESSION['patId'], );
    $app->response()->header('Content-Type', 'application/javascript');
    $msg=json_encode($arr );
    $app->response->body($msg );
	   
	}
	else
	{
	$arr=array('status' => '401', 'message' => 'Unauthorized');
    $app->response()->header('Content-Type', 'application/javascript');
    $msg=json_encode($arr );
    $app->response->body($msg );
	}
    

  }

  catch (Exception $e) {
    $arr=array('status' => '400', 'message' => ' '. $e->getMessage().' ');
    $app->response()->header('Content-Type', 'application/javascript');
    $msg=json_encode($arr );
    $app->response->body($msg );

  }
 
});

$app->get('/patient/getName', function() use ($app) {
  try {
   
	if (isset($_SESSION['patName']))
	{
	$arr=array('status' => '200', 'message' => 'Sending id', 'query_result' => $_SESSION['patName'] );
    $app->response()->header('Content-Type', 'application/javascript');
    $msg=json_encode($arr );
    $app->response->body($msg );
	   
	}
	else
	{
	$arr=array('status' => '401', 'message' => 'Unauthorized');
    $app->response()->header('Content-Type', 'application/javascript');
    $msg=json_encode($arr );
    $app->response->body($msg );
	}
    

  }

  catch (Exception $e) {
    $arr=array('status' => '400', 'message' => ' '. $e->getMessage().' ');
    $app->response()->header('Content-Type', 'application/javascript');
    $msg=json_encode($arr );
    $app->response->body($msg );

  }
 
});







?>

























