# Просто установи это: Write-up

Запускаем программу, она пытается проверить путь `/usr/install_it` и говорит,
что не нашла там файл. Попробуем его установить так, как она предлагает. При
повторном запуске первая проверка уже проходит, но начинает падать на второй,
уже с другим путем.

Полезно также проверить, что будет, если подложить вместо `/usr/install_it`
какой-то другой файл. Запустим программу — в ответ нам скажут `failed validate
installation`. Обмануть не получилось.

Посмотрим, что делает программа, запустив ее через `strace`:

> _В настоящем выводе нет номеров в квадратных скобках в начале строк; они
добавлены вручную для того, чтобы сослаться на них в дальнейшем тексте._

```
[ ] execve("./install_it", ["./install_it"], 0x7ffec2671a90 /* 75 vars */) = 0
[ ] arch_prctl(ARCH_SET_FS, 0x40ab98)       = 0
[ ] set_tid_address(0x40acd0)               = 3291902
[1] open("./install_it", O_RDONLY|O_LARGEFILE) = 3
[2] read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\2\0>\0\1\0\0\0\217\22@\0\0\0\0\0"..., 64) = 64
[3] lseek(3, 37592, SEEK_SET)               = 37592
[ ] brk(NULL)                               = 0x1b3b000
[ ] brk(0x1b3d000)                          = 0x1b3d000
[ ] mmap(0x1b3b000, 4096, PROT_NONE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x1b3b000
[ ] mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f0dede5d000
[4] read(3, "\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"..., 1024) = 1024
[ ] mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f0dede5c000
[5] lseek(3, 37441, SEEK_SET)               = 37441
[6] read(3, "\0.shstrtab\0.note.gnu.property\0.n"..., 147) = 147
[7] lseek(3, 4112, SEEK_SET)                = 4112
[ ] mmap(NULL, 24576, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f0dede56000
[8] read(3, "\17\v\17\v\17\vS\211\373\350\364\r\0\0\350\360\r\0\0001\300\350PZ\0\0\211\337\350\220R\0"..., 23251) = 23251
[ ] munmap(0x7f0dede5c000, 4096)            = 0
[ ] munmap(0x7f0dede5d000, 4096)            = 0
[9] close(3)                                = 0
[ ] mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f0dede5d000
[ ] ioctl(1, TIOCGWINSZ, 0x7fff4203d118)    = -1 ENOTTY (Inappropriate ioctl for device)
[ ] writev(1, [{iov_base="checking path `/usr/install_it`,"..., iov_len=48}, {iov_base="...\n", iov_len=4}], 2checking path `/usr/install_it`, hash = eeb0fce2...
[ ] ) = 52
[1] open("/usr/install_it", O_RDONLY|O_LARGEFILE) = 3
[2] read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\2\0>\0\1\0\0\0\217\22@\0\0\0\0\0"..., 64) = 64
[3] lseek(3, 37592, SEEK_SET)               = 37592
[ ] mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f0dede5c000
[4] read(3, "\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"..., 1024) = 1024
[5] lseek(3, 37441, SEEK_SET)               = 37441
[6] read(3, "\0.shstrtab\0.note.gnu.property\0.n"..., 147) = 147
[7] lseek(3, 4112, SEEK_SET)                = 4112
[ ] munmap(0x7f0dede56000, 24576)           = 0
[ ] mmap(NULL, 24576, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f0dede56000
[8] read(3, "\17\v\17\v\17\vS\211\373\350\364\r\0\0\350\360\r\0\0001\300\350PZ\0\0\211\337\350\220R\0"..., 23251) = 23251
[ ] munmap(0x7f0dede5c000, 4096)            = 0
[9] close(3)                                = 0
[1] open("/usr/installit", O_RDONLY|O_LARGEFILE) = -1 ENOENT (No such file or directory)
[ ] writev(2, [{iov_base="failed find installation at `/us"..., iov_len=79}, {iov_base=NULL, iov_len=0}], 2failed find installation at `/usr/installit`, error: No such file or directory
[ ] ) = 79
[ ] writev(2, [{iov_base="tip: you can install by `cp ./in"..., iov_len=57}, {iov_base=NULL, iov_len=0}], 2tip: you can install by `cp ./install_it /usr/installit`
[ ] ) = 57
[ ] writev(1, [{iov_base="checking path `/usr/installit`, "..., iov_len=51}, {iov_base=NULL, iov_len=0}], 2checking path `/usr/installit`, hash = 690d84cf...
[ ] ) = 51
[ ] exit_group(2)                           = ?
[ ] +++ exited with 2 +++
```

Видим, что в программе есть какой-то цикл, который выполняет вызовы 1–9, но
каждый раз для разного пути. Если мы сможем как-то отдавать программе один и тот
же файл, то она будет считать, что все уже установлено.

Существует много способов этого добиться.

* Манипуляции с файловой системой:
* * Запустить программу в `chroot`, ловить сообщения об ошибках, добавлять недостающий файл и перезапускать заново.
* * Не создавать настоящие файлы, а написать свою файловую систему. Используя `fuse`, можно подсовывать программе по любому пути что угодно. Можно посмотреть [пример простейшей виртуальной файловой системы](https://github.com/libfuse/python-fuse/blob/master/example/hello.py).
* Манипуляции с системными вызовами:
* * Запатчить программу так, чтобы она вместо системных вызовов вызывала какой-нибудь наш собственный код.
* * Перехватывать системные вызовы в отладчике.
* * Переопределить поведение системных вызовов с помощью `strace --inject`.

Рассмотрим подробнее последний из путей — самый быстрый и простой.

Системные вызовы делают вот что:
1. Открываем файл и получаем дескриптор `3`
2. Читаем заголовок ELF-файла
3. Делаем seek на таблицу секций (это можно понять, сравнив адрес прыжка 37592 с
   адресом секций, который можно получить, к примеру, через `readelf -h`)
4. Читаем таблицу секций
5. Прыгаем на таблицу строк (опять же, сравниваем адрес с `readelf -S`)
6. Читаем строки
7. Прыгаем на секцию `.text` (снова сравниваем аргумент с адресами секций)
8. Читаем `.text`
9. Закрываем файл

При этом все пункты с [2] по [9] выполняются над файловым дескриптором, который
вернул вызов `open` в пункте [1].

Мы же хотим, чтобы `open` ничего не делал, а все остальные вызовы возвращали то,
что нам нужно. К счастью, в `strace` есть механизм `inject`, который
позволяет сделать то, что мы хотим.

При этом нам не обязательно подменять все вызовы, достаточно только подменять
файловый дескриптор и результат вызова [2]. А потом программа будет делать `seek`
на нужные места в файле и читать нужные данные.

Выпишем аргументы для `strace`.

1. `--inject=open:retval=3:when=2+` — так `open` всегда будет возвращать 3
2. `--inject=close:retval=0` — так `close` будет ничего не делать и возвращать 0
   (этим мы добьёмся, чтобы читался один и тот же файл)
3. `--inject=read:poke_exit=@arg2=...заголовок...:when=1+4` —
   так вызов [2] всегда будет возвращать правильный ELF-заголовок

Первый вызов `open` отработает без изменений — он откроет файл, который мы
дальше будем переиспользовать.

Значение для заголовка — это первые 64 байта нашего файла.

```bash
$ head -c64 install_it | xxd -p -c0
7f454c4602010100000000000000000002003e00010000008f124000000000004000000000000000d89200000000000000000000400038000900400010000f00
```

Запустим получившуюся команду:
```
$ strace \
   --inject=open:retval=3:when=2+ \
   --inject=close:retval=0 \
   --inject=read:poke_exit=@arg2=7f454c4602010100000000000000000002003e00010000008f124000000000004000000000000000d89200000000000000000000400038000900400010000f00:when=1+4 \
   -o /dev/null \
   ./install_it

...
checking path `/log/flag.txt/log/flag.txtVa+(sQ=/var/flag.txt]f \&/G`, hash = 98bbc0f4...
checking path `/log/flag.txt/log/flag.txtVa+(sQ=/log/install_itdE@@l`, hash = 9885b8f2...
checking path `/log/flag.txt/log/flag.txtVa+(sQ=/log/installitWlN-u%`, hash = d3811c7a...
checking path `/log/flag.txt/log/flag.txtVa+(sQ=/log/not_a_flag'f3=f`, hash = e73aaedf...
checking path `/log/flag.txt/log/flag.txtVa+(sQ=/log/setup.exe]MtZ7-`, hash = a37365ab...
checking path `/log/flag.txt/log/flag.txtVa+(sQ=/log/bashm/]uz|,6p<#`, hash = 8f4f65cb...
checking path `/log/flag.txt/log/flag.txtVa+(sQ=/log/cd#]TUA^"PN9[]|`, hash = 974c2070...
checking path `/log/flag.txt/log/flag.txtVa+(sQ=/log/localB#s&Rj1h_i`, hash = 3adcf57b...
checking path `/log/flag.txt/log/flag.txtVa+(sQ=/log/flag.txt?jj-cfC`, hash = 4f19b7de...
Flag was installed. Flag value is `ugra_y0u_1nstall3d_it_d06bca7f`
```

Флаг: **ugra_y0u_1nstall3d_it_d06bca7f**
