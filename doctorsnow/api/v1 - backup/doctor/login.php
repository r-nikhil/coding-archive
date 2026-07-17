<?php


$app->post('/doctor/login', function() use ($app) {
  try {
    //getting json and decoding it
    $request = $app->request();
    $body = $request->getBody();
    $input = json_decode($body);

    $article = R::findOne('doctorregister', 'docemail=?', array((string)$input->email));

    if ($article) { // if found, return JSON response
      $pass_db = (string)$article->docpassword;
      $pass_request = (string)$input->password;
      if($pass_db === $pass_request)
      {
        $arr=array('status' => '201', 'message' => 'loggingIn', 'docId' => $article->id ); // store the id in front
        $app->response()->header('Content-Type', 'application/javascript');
        $msg=json_encode($arr );
        $app->response->body($msg );
        $session = $article->docemail;
        $session .= $article->doclname; // i concatenated email and last name and stored it in the session variable.
        $_SESSION['session_doctor'] = $session;
		 $_SESSION['docId'] = $article->id;
		 $_SESSION['docEmail'] = $article->docemail;
		 $_SESSION['docLname'] = $article->doclname;
		 

      }
      else
      {
        $arr=array('status' => '401', 'message' => 'wrongPassword');
        $app->response()->header('Content-Type', 'application/javascript');
        $msg=json_encode($arr );
        $app->response->body($msg );


      }

    }

    else {

      $arr=array('status' => '401', 'message' => 'emailNotRegistered');
      $app->response()->header('Content-Type', 'application/javascript');
      $msg=json_encode($arr );
      $app->response->body($msg );


    }
  } catch (ResourceNotFoundException $e) {
    // return 404 server error
    $app->response()->status(404);
  } catch (Exception $e) {
    $arr=array('status' => '400', 'message' => ' '. $e->getMessage().' ');
    $app->response()->header('Content-Type', 'application/javascript');
    $msg=json_encode($arr );
    $app->response->body($msg );
  }


});




$app->get('/doctor/profile/:id', function($id) use ($app) {
  try {
   

     
	 //getting json and decoding it
    $request = $app->request();
    $body = $request->getBody();
    $input = json_decode($body);

    $article = R::findAll('doctorsprofile', 'docid=?', array($id));
      // return JSON-encoded response body with query results
      $var_result=R::exportAll($article);
      $arr=array('status' => '200', 'message' => 'found','queryResult'=> $var_result );
      $app->response()->header('Content-Type', 'application/javascript');
      $msg=json_encode($arr);
      $app->response->body($msg );
    
  

  } catch (Exception $e) {
    $arr=array('status' => '400', 'message' => ' '. $e->getMessage().' ');
    $app->response()->header('Content-Type', 'application/javascript');
    $msg=json_encode($arr );
    $app->response->body($msg );
  }


});













?>
