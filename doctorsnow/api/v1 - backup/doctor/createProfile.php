<?php
$app->post('/doctors/updateProfile', function() use ($app) {

  try {
    //getting json and decoding it
    $request = $app->request();
    $body = $request->getBody();
    $input = json_decode($body);
if ( isset($_SESSION['session_doctor'])){
    $article = R::findOne('doctorsprofile', 'id=?', array((string)$input->docId));
    // storing to DB


    if ($article) { // if found, return JSON response


      $article->docspecial = (string)$input->speciality;
      $article->docaddress = (string)$input->address;
      $article->docpincode = (string)$input->pincode;
      $article->doccharges = (string)$input->charges;
      $article->docdegrees = (string)$input->degrees;
      $article->doccollege = (string)$input->college;
      $article->docexp = (string)$input->experience;
      $article->docexpyears = (string)$input->numofYears;
      $article->docwriteup = (string)$input->writeup;
      $article->doccity = (string)$input->city;
      $article->docmember = (string)$input->memberships;
      $article->doctime = (string)$input->docTime;
      $article->docclinic = (string)$input->clinicName;
      $id = R::store($article);

      //making and storing doc time table here
      $time = (string)$input->docTime;
      $time_arr=explode(',',$time);

      //we need like this date time patient case meds busy confirmed


      $begin = new DateTime( '2010-05-01' );
      $end = new DateTime( '2010-05-10' );

      $interval = DateInterval::createFromDateString('1 day');
      $period = new DatePeriod($begin, $interval, $end);

      foreach ( $period as $dt )
      { echo $dt->format( "l Y-m-d H:i:s\n" );

        foreach ($time_arr as $item) {
          $article = R::dispense('doctime_'.(string)$input->doc_id);
          $article->docspecial = (string)$input->speciality;
          $article->docadd = (string)$input->address;
          $article->docpin = (string)$input->pincode;
          $article->doccharges = (string)$input->charges;

          echo "$item\n";
        }

      }



      $arr=array('status' => '201', 'message' => 'saved');
      $app->response()->header('Content-Type', 'application/javascript');
      $msg=json_encode($arr );
      $app->response->body($msg );





    }

    else {

      $arr=array('status' => '404', 'message' => 'IdNotFound');
      $app->response()->header('Content-Type', 'application/javascript');
      $msg=json_encode($arr );
      $app->response->body($msg );


    }
} else {
	$arr=array('status' => '401', 'message' => 'Unauthorized');
    $app->response()->header('Content-Type', 'application/javascript');
    $msg=json_encode($arr );
    $app->response->body($msg );

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

?>
