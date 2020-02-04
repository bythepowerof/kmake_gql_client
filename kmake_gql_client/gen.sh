#!/bin/bash -x

python3 -m sgqlc.introspection \
     --exclude-deprecated \
     --exclude-description \
     http://localhost:8080/query \
     schema.json
sgqlc-codegen schema.json schema.py
