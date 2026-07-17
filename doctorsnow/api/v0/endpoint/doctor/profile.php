<?php

$app->get('/doctor/profile', function() use ($app, $connection)
{
  include('session.php');
  $body   = $app->request->getBody();
  $result = json_decode($body);


  $result = mysqli_query($connection, "select * from doc_profile where username='$login_session_user_doctor'");
  $data   = mysqli_fetch_array($result);

  echo json_encode($data);

  $app->response()->header('Content-Type', 'application/json');
});

$app->post('/doctor/profile/:id', function() use ($app, $connection){
  if(isset($login_session_user_patient) || isset($login_session_user_doctor))
  {

    $result = mysqli_query($connection, "select * from profile_doctor where id='$id'");
    $data   = mysqli_fetch_array($result);

    echo json_encode($data);

    $app->response()->header('Content-Type', 'application/json');

  }
  else
  {
    echo json_encode("login first and then try to access all the doctors");

  }

});



?>
