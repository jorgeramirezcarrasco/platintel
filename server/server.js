const express = require('express');
const app = express();
const path = require('path');
const router = express.Router();

router.get('/', function (req, res) {
    res.sendFile(path.join(__dirname + '/visualization/network/index.html'));
    //__dirname : It will resolve to your project folder.
});


//add the router
app.use('/network_styles', express.static(__dirname + '/visualization/network/css/'));
//Store all HTML files in view folder.
app.use('/network_scripts', express.static(__dirname + '/visualization/network/js/'));
//Store all JS and CSS in Scripts folder.

app.use('/', router);
app.listen(process.env.PORT || 3000);

console.log('Running at Port 3000');