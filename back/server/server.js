const express = require("express");
const app = express();
const mongoose = require("mongoose");
const bodyParser = require("body-parser");
const passport = require("passport");
const users = require("./routes/api/users");
const analyses = require("./routes/api/analyses");
const cors = require("cors");

var origin = process.env.ORIGIN;

app.use(cors({ credentials: true, origin: origin }));

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

const router = express.Router();
// Connection URL

var uri = process.env.MONGODB_URI;
mongoose
  .connect(uri, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log("MongoDB successfully connected"))
  .catch((err) => console.log(err));

// Passport middleware
app.use("/", router);
app.use(passport.initialize()); // Passport config
require("./config/passport")(passport); // Routes
app.use("/api/users", users);

app.use(
  "/api/analyses",
  passport.authenticate("jwt", { session: false }),
  analyses
);

app.listen(process.env.PORT || 8000);

console.log("Running at Port " + (process.env.PORT || 8000));
