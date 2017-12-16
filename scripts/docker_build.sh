#!/usr/bin/env bash

docker build \
    -t msa_events:latest \
    -t msa_events:1.1.2 \
    -t docker.force.fm/msa/msa_events:latest \
    -t docker.force.fm/msa/msa_events:1.1.2 \
    .
