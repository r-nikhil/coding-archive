<?php
class sessionHandler {
  public function getSession(){
      if (!isset($_SESSION)) {
          session_start();
      }
      $sess = array();
      if(isset($_SESSION['session_doctor']))
      {

          $sess["id"]      =  $_SESSION['docId']
          $sess["email"]    =  $_SESSION['docEmail']
          $sess["name"]     =  $_SESSION['docLname']
      }
      else
      {
          $sess["id"] = '';
          $sess["name"] = 'Guest';
          $sess["email"] = '';
      }
      return $sess;
  }
  public function destroySession(){
      if (!isset($_SESSION)) {
      session_start();
      }
      if(isSet($_SESSION['session_doctor']))
      {
          unset($_SESSION['docId']);
          unset($_SESSION['docLname']);
          unset($_SESSION['docEmail']);
          $info='info';
          if(isSet($_COOKIE[$info]))
          {
              setcookie ($info, '', time() - $cookie_time);
          }
          $msg="Logged Out Successfully...";
      }
      else
      {
          $msg = "Not logged in...";
      }
      return $msg;
  }

  }

?>
