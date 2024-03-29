#!/bin/bash

echo "exec bash -i -l" > /usr/local/bin/shell.sh

exec env -u KYZYLBORDA_SECRET_flag bash --rcfile <(echo run-parts /etc/update-motd.d) -i -l
