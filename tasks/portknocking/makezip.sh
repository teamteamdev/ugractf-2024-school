#!/usr/bin/env bash

cd app
rm ../public/knocker.zip || true
zip -r ../public/knocker.zip epkp poetry.lock pyproject.toml
cd -
