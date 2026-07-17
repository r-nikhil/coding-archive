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
				$article->doccity = (string)$input->city;
				$article->docexpyears = (string)$input->numOfYears;
				$article->docinterests = (string)$input->interests;
				$article->docwriteup = (string)$input->writeup;
				$article->doccharges = (string)$input->charges;
				$article->doclocality = (string)$input->locality;
				$article->docavailability = (string)$input->availablity;
				$article->docservices = (string)$input->services;
				$article->docclinicname = (string)$input->clinicname;
				$article->docclinicaddress = (string)$input->clinicaddress;

				$input->experience = explode(":", $input->experience);
				foreach ($input->experience as $exp)
				{
				$experience =R::dispense('doctorexperience');
  				$experience->docid = $article->docid;
				$experience->desc = $exp;
				//$article->docexperience[] = $experience;
				$id = R::store($experience);
				}

				$input->education = explode(":", $input->education);
				foreach ($input->education as $edu)
				{
				$education =R::dispense('doctoreducation');
  				$education->docid = $article->docid;
				$education->desc = $edu;
				//$article->doceducation[] = $education;
				$id = R::store($education);
				}

				$input->memberships = explode(":", $input->memberships);
				foreach ($input->memberships as $mem) {
				$memberships =R::dispense('doctormemberships');
  				$memberships->docid = $article->docid;
				$memberships->desc = $mem;
				//$article->docmemberships[] = $memberships;
				$id = R::store($memberships);
				}

				$input->certifications = explode(":", $input->certifications);
				foreach ($input->certifications as $cer) {
						$certifications =R::dispense('doctorcertifications');
  				$certifications->docid = $article->docid;
				$certifications->desc = $cer;
				//$article->doccertifications[] = $certifications	;
				$id = R::store($certifications);
				}

				$input->awards = explode(":", $input->awards);
				foreach ($input->awards as $awa) {
				$awards =R::dispense('doctorawards');
  				$awards->docid = $article->docid;
				$awards->desc = $awa;
				//$article->docawards[] = $awards;
				$id = R::store($awards);
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

$app->post('/doctor/addphoto', function() use ($app) {

// frontend person. set formenctype to multipart/form-data
try{







	$target_dir = "uploads/";
	$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
	$uploadOk = 1;
	$imageFileType = pathinfo($target_file,PATHINFO_EXTENSION);
	// Check if image file is a actual image or fake image

	if(isset($_POST["submit"])) {
	    $check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
	    if($check !== false) {
	        echo "File is an image - " . $check["mime"] . ".";
	        $uploadOk = 1;
	    } else {
	        echo "File is not an image.";
	        $uploadOk = 0;
	    }
	}
	// Check if file already exists
	if (file_exists($target_file)) {
	    echo "Sorry, file already exists.";
	    $uploadOk = 0;
	}
	// Check file size
	if ($_FILES["fileToUpload"]["size"] > 500000) {
	    echo "Sorry, your file is too large.";
	    $uploadOk = 0;
	}
	// Allow certain file formats
	if($imageFileType != "jpg" && $imageFileType != "png" && $imageFileType != "jpeg"
	&& $imageFileType != "gif" ) {
	    echo "Sorry, only JPG, JPEG, PNG & GIF files are allowed.";
	    $uploadOk = 0;
	}
	// Check if $uploadOk is set to 0 by an error
	if ($uploadOk == 0) {
	    echo "Sorry, your file was not uploaded.";
	// if everything is ok, try to upload file
	} else {
	    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
	        echo "The file ". basename( $_FILES["fileToUpload"]["name"]). " has been uploaded.";
	    } else {
	        echo "Sorry, there was an error uploading your file.";
	    }
	}
	$request = $app->request();
	$body = $request->getBody();
	$input = json_decode($body);
	if ( isset($_SESSION['session_doctor']) || 1){
		$article = R::findOne('doctorsprofile', 'id=?', array((string)$input->id));
		// storing to DB
		if ($article) {
			$article->doc_image_id= $_FILES["fileToUpload"]["name"];

		}

		}
}
	catch (Exception $e) {
		$arr=array('status' => $app->response->getStatus(), 'message' => ' '. $e->getMessage().' ');
		$app->response()->header('Content-Type', 'application/json');
		$msg=json_encode($arr );
		$app->response->body($msg );
}

});

// in case you want to retrieve the photo

$app->get('/doctor/addphoto', function() use ($app) {
try{
	$request = $app->request();
	$body = $request->getBody();
	$input = json_decode($body);
	if ( isset($_SESSION['session_doctor']) || 1){
		$article = R::findOne('doctorsprofile', 'id=?', array((string)$input->id));
		// storing to DB
		if ($article) {

		$name=	$article->doc_image_id;
		// embed this in the front end
		// ""<img src="http://localhost/face/images/<?=$images[0]->filename
			}

}


}	catch (Exception $e) {
		$arr=array('status' => $app->response->getStatus(), 'message' => ' '. $e->getMessage().' ');
		$app->response()->header('Content-Type', 'application/json');
		$msg=json_encode($arr );
		$app->response->body($msg );
}





});




?>
