#!/bin/bash

#Run in development environment

execFile="../web-server-egeo/serverDev.py"
export FLASK_APP=$execFile
export FLASK_ENV=development
python3 $execFile
