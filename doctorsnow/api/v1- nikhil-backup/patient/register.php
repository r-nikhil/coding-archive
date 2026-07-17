<?php

$app->post('/patient/register', function() use ($app) {
	try {
		$request = $app->request();
		$body = $request->getBody();
		$input = json_decode($body);
		
		$article = R::dispense('patientregister');
		$article->patfname = (string)$input->firstName;
		$article->patlname = (string)$input->lastName;
		$article->patmobile = (string)$input->mobile;
		$article->patemail = (string)$input->email;
		$article->patpassword = (string)$input->password;
		$article->patientname = (string)$input->firstName." ".(string)$input->lastName; 
		$id = R::store($article);

		//$app->response()->header('Content-Type', 'application/json');
		//$app->response()->set->contentType('application/json');
		
		$book = R::load( 'patientregister', $id );
		
		$arr=array('status' => $app->response->getStatus(), 'message' => 'Registered');
		$app->response()->header('Content-Type', 'application/javascript');
		$msg=json_encode($arr );
		$app->response->body($msg );

	}

	catch (Exception $e) {
		$arr=array('status' => $app->response->getStatus(), 'message' => ' '. $e->getMessage().' ');
		$app->response()->header('Content-Type', 'application/javascript');
		$msg=json_encode($arr );
		$app->response->body($msg );

	}


});

?>
