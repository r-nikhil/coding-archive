@@ -8,22 +8,35 @@ require 'RedBean/rb.php';

// set up database connection
R::setup('mysql:host=localhost;dbname=appdata','root','');
R::freeze(true);


// initialize app
$app = new \Slim\Slim();
// handle GET requests for /articles
$app->get('/articles', function () use ($app) {
  // query database for all articles
  $articles = R::find('articles');
    // send response header for JSON content type
  $app->response()->header('Content-Type', 'application/json');

   // return JSON-encoded response body with query results
  echo json_encode(R::exportAll($articles));
});
// run
$app->run();