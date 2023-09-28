#!/bin/bash

sudo apt-get update
sudo apt-get install -y pass
curl -fsSL https://github.com/docker/docker-credential-helpers/releases/download/v0.8.0/docker-credential-pass-v0.8.0.linux-amd64 -o docker-credential-pass
chmod +x docker-credential-pass
mv docker-credential-pass /usr/local/bin/
