const mongoose = require("mongoose");
const Schema = mongoose.Schema; // Create Schema
const AnalysisSchema = new Schema({
  user: {
    type: String,
    required: true,
  },
  analysis: {
    type: String,
    required: true,
  },
  data: {
    type: Array,
    required: true,
  },
});
module.exports = Analysis = mongoose.model("analyses", AnalysisSchema);
