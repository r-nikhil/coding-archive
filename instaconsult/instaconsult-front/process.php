<?php
include "connection.php";

$email= $_POST["email"];
$sql = "INSERT INTO email (email_id) VALUES ('$email')";
//
// if(!isset($email) || trim($email) == '')
// {
//   echo "You did not fill anything";
// }
// else{

if (!filter_var($email, FILTER_VALIDATE_EMAIL) === false) {

  if (mysqli_query($connection, $sql)) {
    echo "Your email has been added to the database";
  } else {
    echo "Error: " . $sql . "<br>" . mysqli_error($conn);
  }

} else {
  echo("Enter a valid Email Address");
}



// }
mysqli_close($connection);

?>
