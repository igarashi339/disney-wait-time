#!/bin/bash
heroku logout
source .env

expect -c "
  log_user 0
  set timeout 3
  spawn heroku login --interactive
  expect \"Email: \"
  send $HEROKU_EMAIL
  send \"\r\"
  expect \"Password: \"
  sleep 2
  send \"${HEROKU_PASSWORD}\"
  sleep 2
  send \"\r\"
  interact
"