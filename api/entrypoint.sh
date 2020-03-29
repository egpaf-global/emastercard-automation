#!/bin/bash

rm -f /opt/emastercard/tmp/pids/server.pid

exec "$@"