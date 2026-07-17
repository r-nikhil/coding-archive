<?php


$app->get('/doctor/:id/appo', function() use ($app, $connection)
{
//http://stackoverflow.com/questions/25493942/mysql-how-to-generate-a-complete-calendar-from-an-interval
// use that link for future use. ITS awesome
  include "session.php";
  if(isset($login_session_user_patient) || isset($login_session_user_doctor) )
    {
$name = $login_session_user_doctor;
// pass from date and end date here.

$fromdate = date("Y-m-d");
$todate = date("Y-m-d",strtotime("+1 week"));

// we have $id
$result = mysqli_query($connection, "select * from  '.$name_$id.' where date BETWEEN '$fromdate' and '$todate'");
$data   = mysqli_fetch_array($result);
echo json_encode($data);

$app->response()->header('Content-Type', 'application/json');

// this will query the doctors table abd give you all appoinbtmentt id... there is no time specified there...we have to query the appointment table first.. some joins can be done here.
// call me when you see this.. i want some guidance to proceed here







  }
else
{
  echo " login first bitch";
}
});




























$app->post('/doctor/appointment', function() use ($app, $connection)
{
  $request      = $app->request();
  $body         = $request->getBody();
  $input        = json_decode($body);
  $patient_id   = $input->patient_id;
  $doctor_id    = $input->doctor_id;
  $time         = $input->time;
  $date         = $input->date;
  $details      = $input->details;
  $previous_med = $input->previous_med;
  $confirm      = $input->confirm;
  $chat_url     = $input->chat_url;



  $query = mysqli_query($connection, "INSERT INTO appointment (patient_id, doctor_id, time, date, details, previous_med, confirm, chat_url)
  VALUES ('$patient_id','$doctor_id','$time','$date','$details','$previous_med','$confirm', '$chat_url')");
  if ($query) {
    echo json_encode("the issue has been added");
  }
});

























?>
