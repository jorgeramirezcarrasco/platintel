const express = require("express");
const router = express.Router();
const Analysis = require("../../models/Analysis");
const Users = require("../../models/User");

// @route GET api/analysis/data
// @desc GET data analysis
// @access Private
router.get("/data", (req, res) => {
  Analysis.findOne({ user: req.user._id }).then((analysis) => {
    res.json(analysis.data);
  });
});

// @route GET api/analysis/list
// @desc List analysis
// @access Private
router.get("/list", (req, res) => {
  Analysis.find({ user: req.user._id }, "analysis").then((analyses) => {
    res.json(analyses);
  });
});

module.exports = router;
