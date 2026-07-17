<?php


$app->post('/doctor/profile', function() use ($app, $connection)
{
  $request    = $app->request();
  $body       = $request->getBody();
  $input      = json_decode($body);
  $name       = $input->name;
  $email      = $input->email;
  $phone      = $input->phone;
  $city       = $input->city;
  $speciality = $input->speciality;
  $experience = $input->experience;

  if (!filter_var($email, FILTER_VALIDATE_EMAIL) === false) {
   // echo ("$email is a valid email address");
	//todo: email is unique else return json already registered
	
    $query = mysqli_query($connection, "INSERT INTO doc_profile (name, email, phone, city, speciality, experience)
    VALUES ('$namee','$email','$phone','$city','$speciality', '$experience')");
    if ($query) {
      echo json_encode("the doctor has been added");
    }
  }
  else {
    echo ("$email is not a valid email address");
  }

  $query = mysqli_query($connection, "select id from doc_profile where email ='$email'");
  $data = mysqli_fetch_array($query);
  $doctor_id=$data[0];
  echo json_encode($doctor_id);

  
  // lets copy a premade table here
  $sql=   "CREATE TABLE IF NOT EXISTS `.'timetable_'.$name.` (
  `id` int(20) NOT NULL,
  `patient_id` int(12) NOT NULL,
  `doctor_id` int(12) NOT NULL,
  `confirm` int(12) NOT NULL,
  `busy` int(12) NOT NULL,
  `appointment_id` int(12) NOT NULL,

  PRIMARY KEY (`id`)
  )";

  if (mysqli_query($connection,$sql))
  {
    echo "new doctor table created successfully";
  }
  else
  {
    echo "Error creating table: " . mysqli_error($con);
  }

$sql = "INSERT INTO `.$doctor_id+$name.` (date)
  SELECT
  DATE_ADD('2014-01-01', INTERVAL t.n DAY)
  FROM (
  SELECT
  a.N + b.N * 10 + c.N * 100 AS n
  FROM
  (SELECT 0 AS N UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) a
  ,(SELECT 0 AS N UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) b
  ,(SELECT 0 AS N UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7) c
  ORDER BY n
  ) t
  WHERE
  t.n <= TIMESTAMPDIFF(DAY, '2015-04-01', '2015-12-31')";


  if (mysqli_query($connection,$sql))
  {
    echo "table has been populated succesfully";



  }
  else
  {
    echo "Error creating table: " . mysqli_error($con);
  }










});
?>
