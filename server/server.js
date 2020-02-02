const express = require('express');
const app = express();
const path = require('path');
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
    res.sendFile(path.join(__dirname + '/visualization/network/index.html'));
    //__dirname : It will resolve to your project folder.
});

router.get('/data', function (req, res) {
    var collection = db_mongo.collection('analysis');
    var cursor = collection.find({ "user": "Test" })
    cursor.toArray(function (err, results) {
        if (err) {
            console.log(err);

        } else {
            res.send(results[0].data);
        }

    })
})

//add the router
app.use('/network_styles', express.static(__dirname + '/visualization/network/css/'));
//Store all HTML files in view folder.
app.use('/network_scripts', express.static(__dirname + '/visualization/network/js/'));
//Store all JS and CSS in Scripts folder.

app.use('/', router);
app.listen(process.env.PORT || 3000);

console.log('Running at Port 3000');