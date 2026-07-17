@@ -11,32 +11,54 @@ R::setup('mysql:host=localhost;dbname=appdata','root','');
R::freeze(true); //prevent anymore changes to repo from redbeans

// initialize app
$app = new \Slim\Slim();
class ResourceNotFoundException extends Exception {}

  // handle GET requests for /articles/:id
  $app->get('/articles/:id', function ($id) use ($app) {    
    try {
      // query database for single article
      $article = R::findOne('articles', 'id=?', array($id));

      if ($article) {
        // if found, return JSON response
        $app->response()->header('Content-Type', 'application/json');
        echo json_encode(R::exportAll($article));
      } else {
        // else throw exception
        throw new ResourceNotFoundException();
      }
    } catch (ResourceNotFoundException $e) {
      // return 404 server error
      $app->response()->status(404);
    } catch (Exception $e) {
      $app->response()->status(400);
      $app->response()->header('X-Status-Reason', $e->getMessage());
    }
  });

  // run
  $app->run();