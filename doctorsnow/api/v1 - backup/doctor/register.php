<?php
$app->post('/doctor/register', function() use ($app) {
  try {
    //getting json and decoding it
    $request = $app->request();
    $body = $request->getBody();	
    $input = json_decode($body);
	

    // storing to DB
    $article = R::dispense('doctorregister');
    $article->docfname = (string)$input->firstName;
    $article->doclname = (string)$input->lastName;
    $article->docmobile = (string)$input->mobile;
    $article->docemail = (string)$input->email;
    $article->docpassword = (string)$input->password;
    $id = R::store($article);

    // we are also storing those fields in docs profile
/*
    $article = R::dispense('doctorsprofile');
    $article->docfname = (string)$input->firstName;
    $article->doclname = (string)$input->lastName;
    $article->docname = (string)$input->firstName." ".(string)$input->lastName  ; // this column is for search
    $article->docmobile = (string)$input->mobile;
    $article->docemail = (string)$input->email;
    $id = R::store($article);
*/

    //$app->response()->header('Content-Type', 'application/json');
    //$app->response()->set->contentType('application/json');

    $arr=array('status' => '200', 'message' => 'Registered');
    $app->response()->header('Content-Type', 'application/javascript');
    $msg=json_encode($arr );
    $app->response->body($msg );

  }

  catch (Exception $e) {
    $arr=array('status' => '400', 'message' => ' '. $e->getMessage().' ');
    $app->response()->header('Content-Type', 'application/javascript');
    $msg=json_encode($arr );
    $app->response->body($msg );

  }


});
?>
