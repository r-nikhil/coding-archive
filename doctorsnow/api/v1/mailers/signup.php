<?php



function doctorWelcomeMail($name, $email){
$subject = 'Welcome to DoctorsNow!';
$from = array('hello@doctorsnow.in' =>'Doctors Now');
$to = array(
 $email  => $name
);

$text = "Hello, Welcome to DoctorsNow";
$html = "Hello ".$name.", <br/> Welcome to  <strong>DoctorsNow</strong>";

$transport = Swift_SmtpTransport::newInstance('smtp.mandrillapp.com', 587);
$transport->setUsername('unizen01@gmail.com');
$transport->setPassword('H11K_849FF05ZLgxBoeN9w');
$swift = Swift_Mailer::newInstance($transport);

$message = new Swift_Message($subject);
$message->setFrom($from);
$message->setBody($html, 'text/html');
$message->setTo($to);
$message->addPart($text, 'text/plain');

if ($recipients = $swift->send($message, $failures))
{
 echo 'Message successfully sent!';
} else {
 echo "There was an error:\n";
 print_r($failures);
}

}

?>