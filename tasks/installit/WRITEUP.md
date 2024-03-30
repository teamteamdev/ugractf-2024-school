# Просто установи это: Write-up

Запускаем программу, она пытается проверить путь `/usr/install_it` и говорит,
что не нашла там файл. Попробуем его установить так, как она предлагает. При
повторном запуске первая проверка уже проходит, но начинает падать на второй,
уже с другим путем.

Попробуем второй путь: попробуем подложить вместо `/usr/install_it` какой-то
другой файл и запустим программу. В ответ нам скажут `failed validate
installation`. Обмануть не получилось.

Посмотрим, что делает эта программа, запустив ее под `strace`:

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

> В квадратных скобочках обозначены номера для ссылок из текста, в настоящем
выводе их нет.

Видим, что в программе есть какой-то цикл, который выполняет вызовы 1-9, но
каждый раз для разного пути. Если мы сможем как-то отдавать программе один и тот
же файл, то она будет считать, что все уже установлено.

Есть несколько способов это сделать: запустить программу в VFS, пропатчить ее,
перехватывать системные вызовы в дебаггере и подменять аргумент или
воспользоваться `strace --inject`. Пойдем по самому простому пути ---
последнему.

Пройдем по системным вызовам:
1. Открываем файл и получаем дескриптор 3
2. Читаем заголовок ELF файла
3. Делаем seek на таблицу секций (это можно понять сравнив адрес прыжка с
  адресом секций, который можно получить, к примеру, через `readelf -h`)
4. Читаем таблицу секций
5. Прыгаем на таблицу строк (`readelf -S` и сравниваем адресы)
6. Читаем строки
7. Прыгаем на секцию `.text` (сравнивая аргумент с адресами секций)
8. Читаем `.text`
9. Закрываем файл

При этом все пункты с 2 по 9 выполняются над файловым дескриптором, который
вернул вызов `open` в пункте 1.

Мы же хотим, чтобы `open` ничего не делал, а все остальные вызовы возвращали то,
что нам нужно. И оказывается в `strace` есть механизм `inject`, который
позволяет сделать то, что мы хотим.

При этом нам не обязательно подменять все вызовы, достаточно только подменять FD
и 2 пункт. А потом программа будет делать seek на нужные места в файле и
читать нужные данные.

Команда по частям:
1. `--inject=open:retval=3:when=2+` --- `open` всегда будет возвращать три
2. `--inject=close:retval=0` --- `close` в noop без ошибок (чтобы читать один и
  тот же файл)
3. `--inject=read:poke_exit=@arg2=<header>:when=1+4` --- пункт 2 всегда будет
  возвращать правильный ELF заголовок.

Мы оставили без изменений первый вызов `open`, чтобы открыть файл, который мы
дальше будем переиспользовать.

Чтобы получить значение заголовка воспользуемся небольшим однострочником:
```python
>>> ''.join(f'{v:02x}' for v in open('install_it', 'rb').read(64))
'7f454c4602010100000000000000000002003e00010000008f124000000000004000000000000000d89200000000000000000000400038000900400010000f00'
```

Запустим эту команду:
```
# strace \
   --inject=open:retval=3:when=2+ \
   --inject=close:retval=0 \
   --inject=read:poke_exit=@arg2=7f454c4602010100000000000000000002003e00010000008f124000000000004000000000000000d89200000000000000000000400038000900400010000f00:when=1+4 \
   -o /dev/null \
   ./install_it
...more lines...
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
