<?php
$app->post('/patient/profile', function() use ($app, $connection)
{
  $request   = $app->request();
  $body      = $request->getBody();
  $input     = json_decode($body);
  $name      = $input->name;
  $allergies = $input->allergies;
  $age       = $input->age;
  $blood     = $input->blood;


  $query = mysqli_query($connection, "INSERT INTO profile_patient (name, issue, age, allergies, blood)
  VALUES ('$name','$issue','$age','$allergies','$blood')");
  if ($query) {
    echo json_encode("the issue has been added");
  }

});
?>
