<?php

$app->post('/patient/makeAppoitment', function() use ($app) {


  try {
    if ( isset($_SESSION['session_patient'])){
    //getting json and decoding it
    $request = $app->request();
    $body = $request->getBody();
    $input = json_decode($body);

    $article = R::dispense('appointments');
    $article->docid = (string)$input->doctorId;
    $article->docname = (string)$input->doctorName;
    $article->patid = (string)$input->patientId;
    $article->patname = (string)$input->patientName;
	$article->probdetails = (string)$input->problemDetails;
	$article->currentmeds = (string)$input->currentMeds;
	$article->time = "";
	$article->date = "";
	$article->connectlink = "";

    $id = R::store($article);

    //$app->response()->header('Content-Type', 'application/json');
    //$app->response()->set->contentType('application/json');

    $arr=array('status' => '200', 'message' => 'Done');
    $app->response()->header('Content-Type', 'application/javascript');
    $msg=json_encode($arr );
    $app->response->body($msg );

  }else {
    R::close();
	$arr=array('status' => '401', 'message' => 'Unauthorized');
    $app->response()->header('Content-Type', 'application/javascript');
    $msg=json_encode($arr );
    $app->response->body($msg );
  }

}
  catch (Exception $e) {
    $arr=array('status' => '400', 'message' => ' '. $e->getMessage().' ');
    $app->response()->header('Content-Type', 'application/javascript');
    $msg=json_encode($arr );
    $app->response->body($msg );

  }
});

$app->get('/patient/getappo', function() use ($app) {
  try {
   

     if ( isset( $_SESSION['session_patient'])){
	 //getting json and decoding it
    $request = $app->request();
    $body = $request->getBody();
    $input = json_decode($body);

    $article = R::findAll('appointments', 'patid=?', array($_SESSION['patId']));
      // return JSON-encoded response body with query results
      $var_result=R::exportAll($article);
      $arr=array('status' => 'true', 'message' => 'found','query_result'=> $var_result );
      $app->response()->header('Content-Type', 'application/javascript');
      $msg=json_encode($arr);
      $app->response->body($msg );
    }
    else
    {
     $arr=array('status' => '401', 'message' => 'Unauthorized');
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



$app->get('/doctor/getappo', function() use ($app) {
  try {
   

     if ( isset($_SESSION['session_doctor'])){
	 //getting json and decoding it
    $request = $app->request();
    $body = $request->getBody();
    $input = json_decode($body);

    $article = R::findAll('appointments', 'docid=?', array($_SESSION['docId']));
      // return JSON-encoded response body with query results
      $var_result=R::exportAll($article);
      $arr=array('status' => '200', 'message' => 'found','queryResult'=> $var_result );
      $app->response()->header('Content-Type', 'application/javascript');
      $msg=json_encode($arr);
      $app->response->body($msg );
    }
    else
    {
     $arr=array('status' => '401', 'message' => 'Unauthorized');
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



/* Commented out because we won't be using it for now
$app->post('/patient/deleteAppoitment/:id', function($id) use ($app) {


  try {
    if ( isset($_SESSION['session_patient'])){
      //getting json and decoding it
      $request = $app->request();
      $body = $request->getBody();
      $input = json_decode($body);
      // i am adduming you will be giving me doctorid and patientid
      // storing to DB
      $article = R::findOne('appointments', 'id=?', array((string)$id));

      R::trash( $article ); //for one bean


      //$app->response()->header('Content-Type', 'application/json');
      //$app->response()->set->contentType('application/json');

      $arr=array('status' => 'true', 'message' => 'appointment deleted');
      $app->response()->header('Content-Type', 'application/javascript');
      $msg=json_encode($arr );
      $app->response->body($msg );

    }else {
      R::close();
    }

  }
  catch (Exception $e) {
    $arr=array('status' => '400', 'message' => ' '. $e->getMessage().' ');
    $app->response()->header('Content-Type', 'application/javascript');
    $msg=json_encode($arr );
    $app->response->body($msg );

  }
});

*/







?>
