var express = require('express');
var app = express();
var bodyParser  = require('body-parser');
var mongoose = require('mongoose');
var connect = require('connect');
var port = 10900;

var db = mongoose.connection;
db.on('error', console.error);
db.once('open', function(){
    // CONNECTED TO MONGODB SERVER
    console.log("Connected to mongod server");
});

mongoose.connect('mongodb://127.0.0.1:27019/recipe');

// [CONFIGURE APP TO USE bodyParser]
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static(__dirname + '/public'));
app.use(connect.cookieParser());
app.use(connect.logger('dev'));
app.use(connect.bodyParser());
app.use(connect.json());
app.use(connect.urlencoded());

// [CONFIGURE SERVER PORT]


// [CONFIGURE ROUTER]
require('./controll.js')(app,db);

// [RUN SERVER]
var server = app.listen(port, function(){
 console.log("Express server has started on port " + port)
});
