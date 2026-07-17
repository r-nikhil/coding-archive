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
			$approved = $article->approved;
			//echo $approved;
			if($approved == 1)
			{
			if($pass_db === $pass_request)
			{	
				//$result = array('docId' => $article->id, 'fname' => $article->docfname, );
				//$arr=array('status' => '201', 'message' => 'loggingIn', 'doctorId' => $article->id, 'doctorName' => $article->docfname ); // store the id in front
				
				$article1 = R::findAll('doctorsprofile', 'id=?', array($article->id));
				// return JSON-encoded response body with query results
				$var_result=R::exportAll($article1);
				
				$experience = R::findAll('doctorexperience', 'docid=?', array($article->docid));
				$var_result[0]['docexperience'] = R::exportAll($experience);
				$education = R::findAll('doctoreducation', 'docid=?', array($article->docid));
				$var_result[0]['doceducation'] = R::exportAll($education);
				$memberships = R::findAll('doctormemberships', 'docid=?', array($article->docid));
				$var_result[0]['docmemberships'] = R::exportAll($memberships);
				$certifications = R::findAll('doctorcertifications', 'docid=?', array($article->docid));
				$var_result[0]['doccertifications'] = R::exportAll($certifications);
				$awards= R::findAll('doctorawards', 'docid=?', array($article->docid));
				$var_result[0]['docawards'] = R::exportAll($awards);
				
				$session = $article->docemail;
				$session .= $article->doclname; // i concatenated email and last name and stored it in the session variable.
				$_SESSION['session_doctor'] = $session;
				$_SESSION['docId'] = $article->id;
				$_SESSION['docEmail'] = $article->docemail;
				$_SESSION['docLname'] = $article->doclname;
				//echo $_SESSION;
				
				$arr=array('status' => $app->response->getStatus(), 'message' => 'loggedIn','queryResult'=> $var_result[0], 'session'=> $_SESSION );
				
				$app->response()->header('Content-Type', 'application/json');
				$msg=json_encode($arr );
				$app->response->body($msg );
				

			}
			else
			{
				$arr=array('status' => $app->response->getStatus(), 'message' => 'wrongPassword');
				$app->response()->header('Content-Type', 'application/json');
				$msg=json_encode($arr );
				$app->response->body($msg );
			}
			}
			else
				{
				$arr=array('status' => $app->response->getStatus(), 'message' => 'notApproved');
				$app->response()->header('Content-Type', 'application/json');
				$msg=json_encode($arr );
				$app->response->body($msg );
			}

		}
		else {
			$arr=array('status' =>$app->response->getStatus(), 'message' => 'emailNotRegistered');
			$app->response()->header('Content-Type', 'application/json');
			$msg=json_encode($arr );
			$app->response->body($msg );
		}
	} catch (ResourceNotFoundException $e) {
		// return 404 server error
		$app->response()->status(404);
	} catch (Exception $e) {
		$arr=array('status' => $app->response->getStatus(), 'message' => ' '. $e->getMessage().' ');
		$app->response()->header('Content-Type', 'application/json');
		$msg=json_encode($arr );
		$app->response->body($msg );
	}
});

$app->get('/doctor/profile/:id', function($id) use ($app) {
	try {
		$article = R::findOne('doctorsprofile', 'id=?', array($id));
		// return JSON-encoded response body with query results
		$var_result=R::exportAll($article);
		
		
		$experience = R::findAll('doctorexperience', 'docid=?', array($article->docid));
		$var_result[0]['docexperience'] = R::exportAll($experience);
		$education = R::findAll('doctoreducation', 'docid=?', array($article->docid));
		$var_result[0]['doceducation'] = R::exportAll($education);
		$memberships = R::findAll('doctormemberships', 'docid=?', array($article->docid));
		$var_result[0]['docmemberships'] = R::exportAll($memberships);
		$certifications = R::findAll('doctorcertifications', 'docid=?', array($article->docid));
		$var_result[0]['doccertifications'] = R::exportAll($certifications);
		$awards= R::findAll('doctorawards', 'docid=?', array($article->docid));
		$var_result[0]['docawards'] = R::exportAll($awards);
		
		$arr=array('status' => $app->response->getStatus(), 'message' => 'found','queryResult'=> $var_result[0] );
		$app->response->headers->set('Content-Type', 'application/json');
		$msg=json_encode($arr);
		$app->response->setBody($msg );

	} catch (Exception $e) {
		$arr=array('status' => $app->response->getStatus(), 'message' => ' '. $e->getMessage().' ');
		//$app->response()->header('Content-Type', 'application/json');
		$app->response->headers->set('Content-Type', 'application/json');
		$msg=json_encode($arr );
		$app->response->setBody($msg );
	}
});

$app->get('/doctor/gettype', function() use ($app) {
	try {
		$cat = array();	
		//$cat[0]=array( "id" => 0 , "title" => "Other", "image" => "test.jpg" );	
		$cat[1]=array( "id" => 1 , "title" => "Cardiologist", "image" => "test.jpg" );					
		$cat[2]=array( "id" => 2 , "title" => "Physician", "image" => "test.jpg"  );					
		$cat[3]=array( "id" => 3 , "title" => "Gynaecologist", "image" => "test.jpg"  );					
		$cat[4]=array( "id" => 4 , "title" => "Dietitian/Nutritionist", "image" => "test.jpg"  );					
		$cat[5]=array( "id" => 5 , "title" => "Sexologist", "image" => "test.jpg"  );					
		$cat[6]=array( "id" => 6 , "title" => "Dermatologist", "image" => "test.jpg"  );					
		$cat[7]=array( "id" => 7 , "title" => "Psychiatrist", "image" => "test.jpg"  );					
		
		$arr=array('status' => '200', 'message' => 'found','queryResult'=> $cat );
		$app->response->headers->set('Content-Type', 'application/json');
		$msg=json_encode($arr);
		$app->response->setBody($msg );

		} catch (Exception $e) {
		$arr=array('status' =>$app->response->getStatus(), 'message' => ' '. $e->getMessage().' ');
		$app->response->headers->set('Content-Type', 'application/json');
		$msg=json_encode($arr );
		$app->response->setBody($msg );
	}  
});

//testing function to be removed
$app->post('/doctors', function() use ($app) {
	try {
		$arr=array('status' => $app->response->getStatus(), 'message' => 'found' );
		//$app->response()->header('Content-Type', 'application/json');
		$app->response->headers->set('Content-Type', 'application/json');
		$msg=json_encode($arr);
		$app->response->setBody($msg );
	} catch (Exception $e) {
		$arr=array('status' => '400', 'message' => ' '. $e->getMessage().' ');
		$app->response->headers->set('Content-Type', 'application/json');
		$msg=json_encode($arr );
		$app->response->setBody($msg );
	}  
});










?>
