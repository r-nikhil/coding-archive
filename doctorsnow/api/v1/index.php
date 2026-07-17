<?php
session_cache_limiter(false);
//session_start();


session_start();
require '.././libs/Slim/Slim.php';
require '.././libs/rb.php';
\Slim\Slim::registerAutoloader();
// set up database connection
R::setup('mysql:host=localhost;dbname=doctornowv1','root','');
//R::freeze(true);
$app = new \Slim\Slim();
// User id from db - Global Variable
$user_id = NULL; // why do you need this ?

//Adding mailing functionality
// require_once '.././libs/Mandrill/Mandrill.php';
// $mandrill = new Mandrill('H11K_849FF05ZLgxBoeN9w');
// require_once '.././libs/Swiftmailer/swift_required.php';


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
$app->options('/(:x+)', function() use ($app) {
	//...return correct headers...
	//$app->response->setStatus(200);
	//$this->next->call();
});
//Handling CORS ends

include "doctor/login.php";
include "doctor/register.php";
include "doctor/createProfile.php";


include "patient/register.php";
include "patient/login.php";
include "patient/utils.php";
include "patient/appointment.php";

include "search/category.php";
include "search/city.php";
// include "search/name.php"


// include "mailers/signup.php";
include "vendor/autoload.php";

$app->get('/test', function() use ($app) {
	echo "working";

doctorWelcomeMail("Hemant", "maddyhemu@gmail.com");
});

// testing jwt
$app->get('/jwt', function() use ($app) {
	$key = "example_key";
	$token = array(
	    "iss" => "http://example.org",
	    "aud" => "http://example.com",
	    "iat" => 1356999524,
	    "nbf" => 1357000000
	);
	$jwt = JWT::encode($token, $key);
	echo $jwt;
	setcookie('identity', $jwt);
});
$app->get('/jwt1', function() use ($app) {
	$key = "example_key";
	$jws        = $_COOKIE['identity'];
	$decoded = JWT::decode($jws, $key, array('HS256'));
	print_r($decoded);


});






$app->run();

?>
