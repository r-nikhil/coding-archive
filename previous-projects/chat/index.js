var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var mysql      = require('mysql');
var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  password : '',
  database : 'chat'
});
var a="no";

app.get('/', function(req, res){
  res.sendfile('index.html');
  console.log(req.connection.remoteAddress);
});

io.on('connection', function(socket){
	socket.on('username', function(un){
	console.log("Username: "+un);
	connection.query('select username,password from info where username="'+un+'"', function(err,result) {
	if(result==false){
		console.log("Username doesn't exist");
		socket.emit('wru');}
	else{
		console.log("Existing username");
		a = result[0].password;
		socket.emit('pwd');}
	});
    //socket.emit('pwd');
  });
  socket.on('password', function(pd){
	console.log("Password: "+pd);
	if(pd === a)
		console.log("right password");
	else{
		console.log("wrong password");
		socket.emit('wrp');}
  });
});

http.listen(3000, function(){
  console.log('listening on *:3000');
});