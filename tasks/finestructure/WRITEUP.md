# Выбор из двух вариантов: Write-up

Дан сжатый файл образа небольшого диска.

```bash
$ file harddisk.img
harddisk.img: DOS/MBR boot sector; partition 1 : ID=0x83, active, start-CHS (0x0,32,33), end-CHS (0x5,187,54), startsector 2048, 90112 sectors
```

Размер файла — 64 МБ, при этом в нём есть только один раздел, и его размер существенно меньше (44 МБ, что можно увидеть, например, утилитой `fdisk`):

```bash
$ fdisk harddisk.img

...
Command (m for help): p
Disk harddisk.img: 64 MiB, 67108864 bytes, 131072 sectors
...

Device        Boot Start   End Sectors Size Id Type
harddisk.img1 *     2048 92159   90112  44M 83 Linux

Command (m for help):
```

Судя по описанию задания, Инга Сергеевна устанавливала операционную систему или проводила какие-то ещё манипуляции с разделами диска, выбирала для удаления один из двух разделов — и ошиблась.

Удаление раздела зачастую просто удаляет запись о нём в таблице разделов, однако ничего не делает с данными — так что все характерные признаки файловой системы остаются на месте.

Просканировать образ на предмет таких файловых систем позволит утилита [testdisk](https://www.cgsecurity.org/wiki/TestDisk). Она же позволит пересоздать утраченную запись в таблице разделов:

![Использование testdisk](writeup/testdisk.gif)

Теперь этой файловой системой можно пользоваться как ни в чём не бывало. Чтобы получить возможность монтировать файловые системы непосредственно из образа, выполним команду `losetup`:

```bash
$ sudo losetup --partscan --show --find harddisk.img
/dev/loop1
```

Образовались файлы устройств — например, они могут называться `/dev/loop1p1` и `/dev/loop1p2`. Их можно монтировать как обычно:

```bash
$ sudo mount /dev/loop1p2 /mnt
```

```bash
$ ls /mnt
'Klych shifrovania.bin'  'Moi rashifrovhik.py'  'Zashifrovannye dannye.bin'
```

Можно запустить скрипт-расшифровщик — в нём придётся лишь поправить имена файлов, ведь у нас нет диска `D:`.

Полученный bmp-файл можно открыть и посмотреть:

![Изображение](writeup/image.png)

Флаг: **ugra_always_double_double_check_7eey49jgtebn**
