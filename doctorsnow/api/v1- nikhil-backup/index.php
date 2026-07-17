<?php
session_cache_limiter(false);
//session_start();


session_start();
require 'Slim/Slim.php';
require 'rb.php';
// require '.././libs/Slim/Middleware/StrongAuth.php';
use \Slim\Middleware\StrongAuth;
// use the middelware above
// foreach (glob("auth/*.php") as $filename)
// {
//     include $filename;
// }
// the above thing includes everything at once.
\Slim\Slim::registerAutoloader();
// set up database connection
R::setup('mysql:host=localhost;dbname=doctornowv1','root','');
//R::freeze(true);
$app = new \Slim\Slim();

// User id from db - Global Variable
$user_id = NULL; // why do you need this ?

//$app->contentType('application/json');
//$app->response->headers->set('Access-Control-Allow-Origin', '*');
//TODO: make a config file for dev, staging and production
//FOR handling CORS
// Access-Control headers are received during OPTIONS requests
header("Access-Control-Allow-Origin: *");
if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {

	if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_METHOD']))
	header("Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS");

	if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']))
	header("Access-Control-Allow-Headers: {$_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']}");
}
// instead of mapping:
// $app->options('/(:x+)', function() use ($app) {
// 	//...return correct headers...
// 	//$app->response->setStatus(200);
// 	//$this->next->call();
// });
//Handling CORS ends
// I commented it out because it doesnt make any sense to me.
include "doctor/login.php";
include "doctor/register.php";
include "doctor/createProfile.php";
include "doctor/sessionHandler.php"
include "doctor/passwordhash.php"


include "patient/register.php";
include "patient/login.php";
include "patient/utils.php";
include "patient/appointment.php";

include "search/category.php";
include "search/city.php";
// include "search/name.php"

// echoResponse seems to work well with angularjs. Check this sample out

$app->get('/session', function() {
    $db = new sessionHandler();
    $session = $db->getSession();
    $response["email"] = $session['email'];
    $response["name"] = $session['name'];
    echoResponse(200, $session);
});
$app->get('/logout', function() {
    $db = new sessionHandler();
    $session = $db->destroySession();
    $response["status"] = "info";
    $response["message"] = "Logged out successfully";
    echoResponse(200, $response);
});

$app->get('/test', function() use ($app) {
	echo "working";
});

$app->run();

?>
