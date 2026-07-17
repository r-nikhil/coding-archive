<?

require ('oauth.php');
function require_auth()
{

  global $dbmain;
  $valid=false;
  $method = $_SERVER['REQUEST_METHOD'];
  $uri = 'http://'.$_SERVER['SERVER_NAME'].$_SERVER['REQUEST_URI'];
  if (array_key_exists('oauth_consumer_key',$_REQUEST))
  {
    ////////////
    // get secret
    $sql="select consumer_secret,uid from `w_user` where consumer_key='" . $dbmain->real_escape_string($_REQUEST['oauth_consumer_key']) ."'";
    //die($sql);
    $result = $dbmain->query($sql);
    $data = $result->fetch_object();
    if(!is_null($data))
    {
      if (array_key_exists('oauth_signature',$_REQUEST))
      {

        $key = $_REQUEST['oauth_consumer_key'];
        $secret = $data->consumer_secret;
        $consumer = new OAuthConsumer($key, $secret);
        $sig_method = new OAuthSignatureMethod_HMAC_SHA1;

        $sig = $_REQUEST['oauth_signature'];
        $req = new OAuthRequest($method, $uri);
        $valid = $sig_method->check_signature( $req, $consumer, null, $sig );
      }
    }

  }
  if(!$valid){
    header('HTTP/1.1 401 Unauthorized', true, 401);
    die('HTTP/1.1 401 Unauthorized');
  }
  else
  {
    return $data->uid;
  }

}
?>
