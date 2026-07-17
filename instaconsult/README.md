# instaconsult

Can't reveal stuff<br>
<h1>Work in Progress</h1><br>

To Anurag and Chetan: Send Rest Requests to "172.17.19.41/instaconsult/Slim/index.php/{param}". It will be available most of the time.



Hemant :: {Check the dump file to get an idea of the schema. All the logic and everything resides in Slim/index.php
 So the first login request will be like http://www.example.com/Slim/index.php/login.<br>

 Maybe open a new branch and start committing code to that branch(front end code)<br>

 Use a chrome plugin to send rest api requests<br>

 Also some browsers dont support put and delete requests apparently. http://docs.slimframework.com/#Routing<br>

 Please refer that on how to make those requests<br>
 }

Finished API Endpoints.<br>
1)/login_client. Send username and password.   (Uses PHP Sessions) POST request<br>
2)/profile_client. Simply send a get request.. I will display the data for the correct user who has logged in. If not logged in he will be redirected to /login. You have to change frontend also accordingly.<br>
<h1>Project Retreival<---------------------> </h1>
3)/open_project. GET Give project details of all the open projects available.<br>
4)/open_project/ids. GET Give project id there, I will retrieve project details.<br>
5)/closed_project. GET Give project details of all the open projects available.<br>
6)/closed_project/ids. GET Give project id there, I will retrieve project details.<br>
7)/accepted_project. GET Give project details of all the open projects available.<br>
8)/accepted_project/ids. GET Give project id there, I will retrieve project details.<br>
9)/deadline_project. GET Give project details of all the open projects available.<br>
10)/deadline_project/ids. GET Give project id there, I will retrieve project details.<br>
<--------------------------------------------------------------------------------------------->


11)/create_profile_client. PUT. See schema/code for all the details you have to give in json.<br>
12)/create_profile_expert. PUT. See schema/code for all the details you have to give in json.<br>
13)/profile_client:idq. GET. See schema/code for all the details you have to give in json. This is for one client accessing other client's profile.<br>
14)/profile_expert:idq. GET. See schema/code for all the details you have to give in json. This is for one client accessing other expert's profile.<br


15)/login_expert. Send username and password.   (Uses PHP Sessions) POST request<br>
16)/profile_expert. Simply send a get request.. I will display the data for the correct user who has logged in. If not logged in he will be redirected to /login. You have to change frontend also accordingly.<br>

<h1>BIDS</h1>

17)/add_bid. POST request. Check the code for values you have to send.<br>
18)/view_bid:id. Get request. Here the id is project id. The frontend has to keep track of which project the user is searching for.<br>
<h1>Comments</h1>
19)/add_comment. POST request. Check the code for details<br>
20)/delete_comment. PUT request. Check the code.<br>







The code quality now is very poor since being a novice I am experimenting with various methods. I dont want to waste time on write beautiful/easy to read code as of now.Once atleast a few modules are neatly working, I will organise stuff into libs, use redbeans, make functions. Please bear with this for sometime. Any doubt in the code, please PM me.
<br><br>

<h2>TODO: </h2>
Every 5 api I write, I will refactor and organise a little so that it doesnt get out of hand<br>
Make a middleware function or include some file for auth at every endpoint<br>
Add try and catch at every endpoint for error management(Also generate specific error also at some point{ask hemant})<br>
Read on slim webhooks and try to use this(later stage)<br>
Write a proper documentation for the api endpoints at later stage for the front end person<br>
Add messages. Tweak comments. Make sure you added CRUD for all tables<br>
