<?php
$app->get('/patient/profile', function() use ($app, $connection)
{
  require "session.php";

  $body   = $app->request->getBody();
  $result = json_decode($body);

  $result = mysqli_query($connection, "select * from profile_patient where name='$login_session_user_patient'");
  $data   = mysqli_fetch_array($result);

  echo json_encode($data);

  $app->response()->header('Content-Type', 'application/json');


});
?>
