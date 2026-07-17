@@ -11,49 +11,35 @@ R::setup('mysql:host=localhost;dbname=appdata','root','');
R::freeze(true); //prevent anymore changes to repo from redbeans

// initialize app
<?php
// do initial application and database setup

// initialize app
$app = new \Slim\Slim();

// route middleware for simple API authentication
function authenticate(\Slim\Route $route) {
  $app = \Slim\Slim::getInstance();
  $uid = $app->getEncryptedCookie('uid');
  $key = $app->getEncryptedCookie('key');
  if (validateUserKey($uid, $key) === false) {
    $app->halt(401);
  }
}

function validateUserKey($uid, $key) {
  // insert your (hopefully more complex) validation routine here
  if ($uid == 'demo' && $key == 'demo') {
    return true;
  } else {
    return false;
  }
}

// handle GET requests for /articles
$app->get('/articles', 'authenticate', function () use ($app) {
  // query database for all articles
  $articles = R::find('articles');

  // send response header for JSON content type
  $app->response()->header('Content-Type', 'application/json');

  // return JSON-encoded response body with query results
  echo json_encode(R::exportAll($articles));
});

// generates a temporary API key using cookies
// call this first to gain access to protected API methods
$app->get('/demo', function () use ($app) {
    $app->setEncryptedCookie('uid', 'demo', '5 minutes');
    $app->setEncryptedCookie('key', 'demo', '5 minutes');
      } catch (Exception $e) {
    $app->response()->status(400);
    $app->response()->header('X-Status-Reason', $e->getMessage());