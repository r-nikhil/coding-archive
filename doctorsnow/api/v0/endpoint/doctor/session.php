<?php
// session_start();

$connection = mysqli_connect("localhost", "root", "", "doctornow");

$login_doctor = $_SESSION['login_doctor'];

$result=mysqli_query($connection, "select username from login_patient where username= '$login_doctor'");

$row = mysqli_fetch_assoc($result);

$login_session_user_doctor  = $row['username'];// this extra time reassigning and search happens for safety


//
// if(!isset($login_session_user_patient) || !isset($login_session_user_doctor) )
// {
//   mysqli_close($connection); // Closing Connection
//   // header('Location: index.php'); // This has to be changed. Come back to this at the end
// }

?>
