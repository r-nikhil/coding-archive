<?php
$app->get('/doctor/profile', function() use ($app, $connection)
{
  include('session.php');
  $body   = $app->request->getBody();
  $result = json_decode($body);


  $result = mysqli_query($connection, "select * from profile_doctor where username='$login_session_user_doctor'");
  $data   = mysqli_fetch_array($result);

  echo json_encode($data);

  $app->response()->header('Content-Type', 'application/json');
});
?>