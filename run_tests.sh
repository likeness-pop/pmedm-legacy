#!/bin/bash

pytest pmedm_legacy \
    -r a \
    --verbose \
    --color yes \
    --numprocesses logical \
    --dist loadgroup \
    --doctest-modules \
    --cov pmedm_legacy \
    --cov-report term-missing
