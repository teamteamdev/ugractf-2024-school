#!/usr/bin/env bash

cd app
zip -r ../public/knocker.zip epkp poetry.lock pyproject.toml
cd -
