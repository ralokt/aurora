const path = require('path');
const merge = require('webpack-merge');
const validate = require('webpack-validator');
const parts = require('./lib/parts')

const PATHS = {
  app: path.join(__dirname, 'app'),
  build: path.join(__dirname, '../js')
};

const common = {
  entry: {
    app: PATHS.app
  },
  output: {
    path: PATHS.build,
    filename: 'feedback.js'
  },
  plugins: [
  ]
};

var config;

switch(process.env.npm_lifecycle_event) {
  case 'build':
    config = merge(
      common,
      parts.minify(),
      parts.setupCSS(PATHS.app)
    );
    break;
  default:
    config = merge(
      common,
      parts.setupCSS(PATHS.app)
    );
}

module.exports = validate(config);