#!/bin/bash

PORT=3000
PORT_DB=8000
DB=./data/new-user.json
CURL_CMD="curl -X GET http://localhost:$PORT/users/check?id=0"  # <--- CHANGE THIS!

run_block() {
  json-server --port $PORT_DB $DB &
  PID=$!
  sleep 1
  $CURL_CMD
  kill -TERM $PID 2>/dev/null
  wait $PID 2>/dev/null
}

run_block
echo ""
read -p "Press Enter to run the second time..."
echo ""
run_block
echo ""
echo "Done"
