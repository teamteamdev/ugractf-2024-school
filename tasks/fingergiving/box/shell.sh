#!/bin/bash
run-parts /etc/update-motd.d
exec bash -i -l
