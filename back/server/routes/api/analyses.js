const express = require("express");
const router = express.Router();
const Analysis = require("../../models/Analysis");
const Users = require("../../models/User");

// @route GET api/analyses/data
// @desc GET data analyses
// @access Private
router.post("/data", (req, res) => {
  Analysis.findOne({ user: req.user._id, analysis: req.body.analysis }).then(
    (analysis) => {
      res.json(analysis.data);
    }
  );
});

// @route GET api/analyses/list
// @desc List analyses
// @access Private
router.get("/list", (req, res) => {
  Analysis.find({ user: req.user._id }, "analysis").then((analyses) => {
    res.json(analyses);
  });
});

module.exports = router;
