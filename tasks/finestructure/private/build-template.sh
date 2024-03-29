#!/bin/bash

mkdir part1 part2


dd if=/dev/zero of=template.img bs=1048576 count=64

sfdisk template.img <<EOF
unit: sectors
start=2048, size=90112, type=83, bootable
type=7
EOF

lodevice=$(sudo losetup --partscan --show --find template.img)


sudo mkfs.ext4 -i 1024 -L boot -v ${lodevice}p1
sudo mount ${lodevice}p1 part1
sudo cp /boot/config-*-generic /boot/memtest86*x64.* /boot/System.map-*-generic part1
for i in 36 39; do
    sudo touch part1/vmlinuz-6.2.0-$i-generic
    sudo touch part1/initrd.img-6.2.0-$i-generic
done
sudo chmod o-rwx,g-rwx part1/v* part1/i*
sudo mkdir part1/{efi,grub}
sudo umount part1


sudo mkfs.ntfs -L data -s 512 -c 512 -U -v ${lodevice}p2
sudo mount ${lodevice}p2 part2 -o uid=$(id -u),gid=$(id -g)
for i in $(seq 0 7811); do
    head -c1024 /dev/urandom > part2/t-$(mktemp -u | tail -c9) && echo -n -e "Randomizing $i...\r" 1>&2
done
for i in $(ls part2 | head -n1600); do
    rm part2/$i
done
echo 1>&2

cat decr.py > part2/Moi\ rashifrovhik.py
for i in $(seq -w 00000 32767); do
    echo -n "<d$i>" >> part2/Zashifrovannye\ dannye.bin
    echo -n "<k$i>" >> part2/Klych\ shifrovania.bin
    echo -n -e "Putting data $i...\r" 1>&2
done
echo 1>&2
rm part2/t-*

sudo umount part2


sudo losetup -d $lodevice
rmdir part1 part2

sfdisk --delete template.img 2
