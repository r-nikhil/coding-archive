<?php

$app->post('/patient/makeappo', function() use ($app) {
	//tested using POSTMAN
	try {
		$request = $app->request();
		$body = $request->getBody();
		$input = json_decode($body);
		if ( isset($_SESSION['session_patient']) || 1)//have to remove 1
		{
			$article = R::dispense('appointments');
			$article->docid = (string)$input->docId;
			$article->docname = (string)$input->docName;
			$article->patid = (string)$input->patientId;
			$article->patname = (string)$input->patientName;
			$article->probdetails = (string)$input->patientDetails;
			$article->currentmeds = (string)$input->currentMeds;
			$article->time = "";
			$article->date = "";
			$article->connectlink = "https://appear.in/docdoc".(string)$input->docId."_".(string)$input->patientId;
			$id = R::store($article);
			$arr=array('status' => $app->response->getStatus(), 'message' => 'Done');
			$app->response()->header('Content-Type', 'application/json');
			$msg=json_encode($arr );
			$app->response->body($msg );
		}else {
			R::close();
			$arr=array('status' => $app->response->getStatus(), 'message' => 'Unauthorized');
			$app->response()->header('Content-Type', 'application/json');
			$msg=json_encode($arr );
			$app->response->body($msg );
		}
	}
	catch (Exception $e) {
		$arr=array('status' => $app->response->getStatus(), 'message' => ' '. $e->getMessage().' ');
		$app->response()->header('Content-Type', 'application/json');
		$msg=json_encode($arr );
		$app->response->body($msg );
	}
});

$app->get('/patient/getappo/:id', function() use ($app) {
	//tested using POSTMAN
	try {
		if ( isset( $_SESSION['session_patient']) || 1)//have to remove 1
		{
			$article = R::findAll('appointments', 'patid=?', array(1));
			// return JSON-encoded response body with query results
			$var_result=R::exportAll($article);
			$arr=array('status' => $app->response->getStatus(), 'message' => 'found','queryResult'=> $var_result );
			$app->response()->header('Content-Type', 'application/json');
			$msg=json_encode($arr);
			$app->response->body($msg );
		}
		else
		{
			$arr=array('status' => $app->response->getStatus(), 'message' => 'Unauthorized');
			$app->response()->header('Content-Type', 'application/json');
			$msg=json_encode($arr );
			$app->response->body($msg );
		}
	} catch (Exception $e) {
		$arr=array( 'status' => $app->response->getStatus() , 'message' => ' '. $e->getMessage().' ');
		$app->response()->header('Content-Type', 'application/json');
		$msg=json_encode($arr );
		$app->response->body($msg );
	}
});



$app->get('/doctor/getappo/:id', function($id) use ($app) {
	//tested using POSTMAN
	try {
		//$_SESSION['docId'] =11;
		if ( isset($_SESSION['session_doctor']) || 1)//have to remove 1
		{
			$article = R::findAll('appointments', 'docid=?', array($id));
			// return JSON-encoded response body with query results
			$var_result=R::exportAll($article);
			$arr=array( 'status' => $app->response->getStatus() , 'message' => 'found','queryResult'=> $var_result );
			$app->response()->header('Content-Type', 'application/json');
			$msg=json_encode($arr);
			$app->response->body($msg );
		}
		else
		{
			$arr=array('status' => $app->response->getStatus(), 'message' => 'Unauthorized', 'session' => $_SESSION);
			$app->response()->header('Content-Type', 'application/json');
			$msg=json_encode($arr );
			$app->response->body($msg );

		}
	} catch (Exception $e) {
		$arr=array('status' => $app->response->getStatus(), 'message' => ' '. $e->getMessage().' ');
		$app->response()->header('Content-Type', 'application/json');
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
	$app->response()->header('Content-Type', 'application/json');
	$msg=json_encode($arr );
	$app->response->body($msg );

	}else {
	R::close();
	}

}
catch (Exception $e) {
	$arr=array('status' => '400', 'message' => ' '. $e->getMessage().' ');
	$app->response()->header('Content-Type', 'application/json');
	$msg=json_encode($arr );
	$app->response->body($msg );

}
});

*/







?>
