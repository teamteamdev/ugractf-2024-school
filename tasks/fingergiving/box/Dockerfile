FROM ubuntu:22.04

RUN apt update && apt install sudo

RUN useradd -ms /bin/bash user
RUN echo "user ALL=(ALL) NOPASSWD: /usr/bin/apt install *" > /etc/sudoers.d/10-apt

COPY shell.sh /usr/local/bin/shell.sh
RUN chmod 777 /usr/local/bin/shell.sh

RUN touch /flag.txt
RUN chmod 600 /flag.txt

USER user
CMD ["/usr/local/bin/shell.sh"]
