<?php
$app->post('/patient/login', function() use ($app) {
	try {
		$request = $app->request();
		$body = $request->getBody();
		$input = json_decode($body);
		//getting json and decoding it
		$article = R::findOne('patientregister', 'patemail=?', array((string)$input->email));
		$request = $app->request();
		$body = $request->getBody();
		$input = json_decode($body);
		if ($article) { // if found, return JSON response
			$pass_db = (string)$article->patpassword;
			$pass_request = (string)$input->password;
			if($pass_db === $pass_request)
			{	$result=array('patientId' => $article->id, 'patientName' => $article->patfname);
				$arr=array('status' => '200', 'message' => 'loggedIn','queryResult' => $result); // store the id in front
				$app->response()->header('Content-Type', 'application/json');
				$msg=json_encode($arr );
				$app->response->body($msg );
				$_SESSION['patEmail'] = $article->patemail;
				$_SESSION['patId'] = $article->id;
				$_SESSION['patName'] = $article->patlname; // patient name because we will be sending it to frontend if they want to use
				$_SESSION['session_patient'] = $article->id; // patient name because we will be sending it to frontend if they want to use
				
			}
			else
			{
				$arr=array('status' => $app->response->getStatus(), 'message' => 'wrongPassword');
				$app->response()->header('Content-Type', 'application/json');
				$msg=json_encode($arr );
				$app->response->body($msg );

			}

		}
		else {
			$arr=array('status' => $app->response->getStatus(), 'message' => 'emailNotRegistered');
			$app->response()->header('Content-Type', 'application/json');
			$msg=json_encode($arr );
			$app->response->body($msg );

		}
	} catch (ResourceNotFoundException $e) {
		// return 404 server error
		$app->response()->status(404);
	}
	catch (Exception $e) {
		$arr=array('status' => $app->response->getStatus(), 'message' => ' '. $e->getMessage().' ');
		$app->response()->header('Content-Type', 'application/json');
		$msg=json_encode($arr );
		$app->response->body($msg );
	}


});
?>
