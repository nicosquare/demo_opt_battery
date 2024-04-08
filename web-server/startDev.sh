#!/bin/bash

#Run in development environment

execFile="../web-server/serverDev.py"
export FLASK_APP=$execFile
export FLASK_DEBUG=True
python3 $execFile
