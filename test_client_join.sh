#!/bin/bash

# Get current working directory
PROJECT_DIR="$(pwd)"

# Start multiple clients automatically with JOIN commands
for i in {1..10}
do
  osascript -e "tell application \"Terminal\" to do script \"echo 'JOIN User$i' | python3 '$PROJECT_DIR/client.py' localhost 8001\""
  sleep 1
done

# Start the 11th client (OverflowUser)
osascript -e "tell application \"Terminal\" to do script \"echo 'JOIN OverflowUser' | python3 '$PROJECT_DIR/client.py' localhost 8001\""
