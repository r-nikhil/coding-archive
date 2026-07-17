<?php
// load required files
require 'Slim/Slim.php';
require 'RedBean/rb.php';

// register Slim auto-loader
\Slim\Slim::registerAutoloader();

// set up database connection
R::setup('mysql:host=localhost;dbname=appdata','root','');
R::freeze(true); //prevent anymore changes to repo from redbeans

// initialize app

// initialize app
$app = new \Slim\Slim();

// handle GET requests for /articles
$app->get('/articles', function () use ($app) {
  try {
    // query database for articles
    $articles = R::find('articles');

    // check request content type
    // format and return response body in specified format
    $mediaType = $app->request()->getMediaType();
    if ($mediaType == 'application/xml') {
      $app->response()->header('Content-Type', 'application/xml');
      $xml = new SimpleXMLElement('<root/>');
      $result = R::exportAll($articles);
      foreach ($result as $r) {
        $item = $xml->addChild('item');
        $item->addChild('id', $r['id']);
        $item->addChild('title', $r['title']);
        $item->addChild('url', $r['url']);
        $item->addChild('date', $r['date']);
      }
      echo $xml->asXml();
    } else if (($mediaType == 'application/json')) {
      $app->response()->header('Content-Type', 'application/json');
      echo json_encode(R::exportAll($articles));
    }
  } catch (Exception $e) {
    $app->response()->status(400);
    $app->response()->header('X-Status-Reason', $e->getMessage());
  }
});

// run
$app->run();
