#!/bin/bash

echo "%echo Generating a basic OpenPGP key
Key-Type: default
Subkey-Type: default
Name-Real: CI
Name-Comment: Temporary Key for CI
Name-Email: ci@localhost
Expire-Date: 0
%no-protection
%commit
%echo done" | gpg2 --batch --pinentry-mode loopback --gen-key
pass init "ci@localhost"
