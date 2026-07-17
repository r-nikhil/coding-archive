<?php
$app->get('/search/category/:category', function($category) use ($app) {
  try {
       $article = R::find('doctorsprofile', 'doctype=?', array($category));

    if ($article){
      // return JSON-encoded response body with query results
      $var_result=R::exportAll($article);
      $arr=array('status' => '200', 'message' => 'found','queryResult'=> $var_result );
      $app->response()->header('Content-Type', 'application/javascript');

      $msg=json_encode($arr);
      $app->response->body($msg );
    }
    else
    {
      $arr=array('status' => '200', 'message' => 'noResults');
      $app->response()->header('Content-Type', 'application/javascript');
      $msg=json_encode($arr );
      $app->response->body($msg );

    }




  } catch (Exception $e) {
    $arr=array('status' => '400', 'message' => ' '. $e->getMessage().' ');
    $app->response()->header('Content-Type', 'application/javascript');
    $msg=json_encode($arr );
    $app->response->body($msg );
  }



});
?>
