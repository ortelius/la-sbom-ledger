`use strict`

const { createLogger, format, transports }        = require('winston');
const { combine, printf, timestamp, splat, align} = format;
const fileSys = require('fs');
const Yaml    = require('js-yaml');

//Pull in configuration options - setup.yml
let config;
try {
  config = Yaml.load(fileSys.readFileSync('setup.yml'))
} catch (error) {
    //Dies hard this way.. This is a major issue we just fail outright on
    console.log(`Error in log.js: ${error}`)
    process.exit(-1);
}

//Setup the Logger
const logs = createLogger({
  level: config.logging.logLevel,
  transports: [
    new transports.File({
      filename: config.logging.logPath,
      maxsize: config.logging.maxSize,
      maxFiles: config.logging.maxFiles,
      colorize: true,
      format: combine(
        splat(),
        timestamp(),
        align(),
        printf((info) => {
          const { timestamp, level, message, ...args} = info;
          const ts = timestamp.slice(0, 19).replace('T', ' ');
          return `${ts} [${level}]: ${message} ${Object.keys(args).length ? JSON.stringify(args, null, 2) : ''}`;
        }),
      )
    }),
    new (transports.Console)({
      format: format.combine(
        format.colorize({
          all:true
        }),
        splat(),
        timestamp(),
        align(),
        printf((info) => {
          const { timestamp, level, message, ...args} = info;
          const ts = timestamp.slice(0, 19).replace('T', ' ');
          return `${ts} [${level}]: ${message} ${Object.keys(args).length ? JSON.stringify(args, null, 2) : ''}`;
        }),
      )
    })

  ],
  exitOnError: false, // do not exit on handled exceptions
});

module.exports = logs;