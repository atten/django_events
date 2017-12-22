#!/usr/bin/env bash

docker build \
    -t docker.force.fm/msa/events:latest \
    -t docker.force.fm/msa/events:1.1.2 \
    .
