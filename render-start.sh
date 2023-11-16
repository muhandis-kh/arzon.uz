#!/usr/bin/env bash
# exit on error
set -o errexit

#Chrome
STORAGE_DIR=/opt/render/project/.render

if [[ ! -d $STORAGE_DIR/chrome ]]; then
  echo "...Downloading Chrome"
  mkdir -p $STORAGE_DIR/chrome
  cd $STORAGE_DIR/chrome
  wget -P ./ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  dpkg -x ./google-chrome-stable_current_amd64.deb $STORAGE_DIR/chrome
  rm ./google-chrome-stable_current_amd64.deb
  cd $HOME/project/src # Make sure we return to where we were
else
  echo "...Using Chrome from cache"
fi

Xvfb :1 -screen 0 1024x768x24 &
export DISPLAY=:1
#requirements
gunicorn core.wsgi:app -t 1800 --keep-alive 1800 