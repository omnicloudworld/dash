#!/usr/bin/env bash

export DEBUG_API=0
hypercorn -w 1 --bind 0.0.0.0:8008 test/index:server
