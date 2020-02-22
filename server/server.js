const express = require('express');
const app = express();
const session = require('express-session');
const bodyParser = require('body-parser');
const path = require('path');
const bcrypt = require('bcryptjs');

app.use(session({
    secret: 'secret',
    resave: true,
    saveUninitialized: true
}));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

const router = express.Router();
const mongodb = require('mongodb')


// Connection URL

var uri = process.env.MONGODB_URI;
var db_name = process.env.MONGODB_NAME
var db_mongo;

mongodb.MongoClient.connect(uri, { 'useUnifiedTopology': true }, function (err, db) {
    db_mongo = db.db(db_name)
});

router.get('/', function (req, res) {
    res.sendFile(path.join(__dirname + '/login/login.html'));
    //__dirname : It will resolve to your project folder.
});

router.post('/auth', function (req, res) {
    var username = req.body.username;
    var password = req.body.password;
    if (username && password) {
        var collection = db_mongo.collection('users');

        var cursor = collection.find({ "username": username })
        cursor.toArray(function (err, results) {
            if (results.length > 0) {
                if (bcrypt.compareSync(password, results[0]['password'])) {
                    req.session.loggedin = true;
                    req.session.username = username;
                    res.redirect('/network');
                } else {
                    res.send('Incorrect Username and/or Password!');
                }
            } else {
                res.send('Incorrect Username and/or Password!');
            }
            res.end();
        });
    } else {
        res.send('Please enter Username and Password!');
        res.end();
    }
});
/*
router.post('/register', function (req, res, next) {
    var username = req.body.username;
    var password = req.body.password;

    bcrypt.hash(password, 12)
        .then(function (hashedPassword) {
            console.log(hashedPassword)
        })
        .then(function () {
            res.send();
        })
        .catch(function (error) {
            console.log("Error saving user: ");
            console.log(error);
            next();
        });
});
*/
router.get('/network', function (req, res) {
    if (req.session.loggedin) {
        res.sendFile(path.join(__dirname + '/visualization/network/index.html'));
        //__dirname : It will resolve to your project folder.
    } else {
        res.redirect('/');
    }

});

router.get('/data', function (req, res) {
    if (req.session.loggedin) {
        var collection = db_mongo.collection('analysis');
        var cursor = collection.find({ "user": "Test" })
        cursor.toArray(function (err, results) {
            if (err) {
                console.log(err);

            } else {
                res.send(results[0].data);
            }

        })
    } else {
        res.redirect('/');
    }

})

//add the router
app.use('/network_styles', express.static(__dirname + '/visualization/network/css/'));
//Store all HTML files in view folder.
app.use('/network_scripts', express.static(__dirname + '/visualization/network/js/'));
//Store all JS and CSS in Scripts folder.

app.use('/', router);
app.listen(process.env.PORT || 3000);

console.log('Running at Port 3000');