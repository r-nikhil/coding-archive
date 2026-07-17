<?php
$app->post('/doctor/updateProfile', function() use ($app) {

	try {
		//getting json and decoding it
		$request = $app->request();
		$body = $request->getBody();
		$input = json_decode($body);
		if ( isset($_SESSION['session_doctor']) || 1){
			$article = R::findOne('doctorsprofile', 'id=?', array((string)$input->id));
			// storing to DB
			if ($article) { // if found, return JSON response
				//$article->docspecial = (string)$input->speciality;
				if(isset($input->city))
				$article->doccity = (string)$input->city;
				if(isset($input->numOfYears))
				$article->docexpyears = (string)$input->numOfYears;
				if(isset($input->interests))
				$article->docinterests = (string)$input->interests;
				if(isset($input->writeup))
				$article->docwriteup = (string)$input->writeup;
				if(isset($input->charges))
				$article->doccharges = (string)$input->charges;
				if(isset($input->locality))
				$article->doclocality = (string)$input->locality;
				if(isset($input->availablity))
				$article->docavailability = (string)$input->availablity;
				if(isset($input->services))
				$article->docservices = (string)$input->services;
				if(isset($input->clinicname))
				$article->docclinicname = (string)$input->clinicname;
				if(isset($input->clinicaddress))
				$article->docclinicaddress = (string)$input->clinicaddress;
				
				//$input->experience = explode(":", $input->experience);
				foreach ($input->experience as $exp) 
				{
				if($exp->id === NULL )	
				{		
				$experience =R::dispense('doctorexperience');
  				$experience->docid = $article->docid;	
				$experience->desc = $exp->desc;
				//$article->docexperience[] = $experience;	
				$id = R::store($experience);
				}
				else
				{
				$experience = R::findOne('doctorexperience', 'id=?', array((string)$exp->id));
				$experience->desc = $exp->desc;				
				$id = R::store($experience);	
				}

				}	
	
				//$input->education = explode(":", $input->education);
				foreach ($input->education as $edu) 
				{
				if($edu->id === NULL )	
				{	
				$education =R::dispense('doctoreducation');
  				$education->docid = $article->docid;	
				$education->desc = $edu->desc;
				//$article->doceducation[] = $education;	
				$id = R::store($education);
				}
				else
				{
				$education = R::findOne('doctoreducation', 'id=?', array((string)$edu->id));
				$education->desc = $edu->desc;				
				$id = R::store($education);	
				}

				}
				
				//$input->memberships = explode(":", $input->memberships);
				foreach ($input->memberships as $mem) {
				if($mem->id === NULL )	
				{		
				$memberships =R::dispense('doctormemberships');
  				$memberships->docid = $article->docid;	
				$memberships->desc = $mem->desc;
				//$article->docmemberships[] = $memberships;	
				$id = R::store($memberships);
				}
				else
				{
				$memberships = R::findOne('doctormemberships', 'id=?', array((string)$mem->id));
				$memberships->desc = $mem->desc;				
				$id = R::store($memberships);	
				}

				}				
				
				//$input->certifications = explode(":", $input->certifications);
				foreach ($input->certifications as $cer) {
				if($cer->id === NULL )	
				{
				$certifications =R::dispense('doctorcertifications');
  				$certifications->docid = $article->docid;	
				$certifications->desc = $cer->desc;
				//$article->doccertifications[] = $certifications	;
				$id = R::store($certifications);
				}
				else
				{
				$certifications = R::findOne('doctorcertifications', 'id=?', array((string)$cer->id));
				$certifications->desc = $cer->desc;				
				$id = R::store($certifications);	
				}

				}	
				
				//$input->awards = explode(":", $input->awards);
				foreach ($input->awards as $awa) {
				if($awa->id === NULL )	
				{
				$awards =R::dispense('doctorawards');
  				$awards->docid = $article->docid;	
				$awards->desc = $awa->desc;
				//$article->docawards[] = $awards;
				$id = R::store($awards);
				}
				else
				{
				$awards = R::findOne('doctorawards', 'id=?', array((string)$awa->id));
				$awards->desc = $awa->desc;				
				$id = R::store($awards);	
				}

				}		
				
				$id = R::store($article);
				
				$arr=array('status' => $app->response->getStatus(), 'message' => 'saved');
				$app->response()->header('Content-Type', 'application/json');
				$msg=json_encode($arr );
				$app->response->body($msg );
			}
			
			
			
			
			
		} else {
			$arr=array('status' => $app->response->getStatus(), 'message' => 'Unauthorized');
			$app->response()->header('Content-Type', 'application/json');
			$msg=json_encode($arr );
			$app->response->body($msg );
			R::close();
		}
	}
	catch (Exception $e) {
		$arr=array('status' => $app->response->getStatus(), 'message' => ' '. $e->getMessage().' ');
		$app->response()->header('Content-Type', 'application/json');
		$msg=json_encode($arr );
		$app->response->body($msg );
	}
});





?>
