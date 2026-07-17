<?php

/// this is the search api. I think we can even access this using chrome
// have to look in specifications

$app->get('/doctor/search/category/:id', function() use ($app, $connection)
{

  $request   = $app->request();
  $body      = $request->getBody();
  $input     = json_decode($body);
  $doctor_id = $input->doctor_id;
  $tablename= "category"+$id;


  $result = mysqli_query($connection, "select * from '.$tablename.' where doctor_id='$doctor_id'");
  $data   = mysqli_fetch_array($result);

  echo json_encode($data);

});


$app->get('/doctor/search/name/:name', function() use ($app, $connection)
{

  $request   = $app->request();
  $body      = $request->getBody();
  $input     = json_decode($body);


  $result = mysqli_query($connection, "select * from doc_profile where full_name='$name'");
  $data   = mysqli_fetch_array($result);

  echo json_encode($data);

});
$app->get('/doctor/search/city/:city', function() use ($app, $connection)
{

  $request   = $app->request();
  $body      = $request->getBody();
  $input     = json_decode($body);


  $result = mysqli_query($connection, "select * from doc_profile where city='$city'");
  $data   = mysqli_fetch_array($result);

  echo json_encode($data);

});


?>
