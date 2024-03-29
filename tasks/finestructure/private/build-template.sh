#!/bin/bash

mkdir /tmp/part1 /tmp/part2


dd if=/dev/zero of=template.img bs=1048576 count=64

sfdisk template.img <<EOF
unit: sectors
start=2048, size=90112, type=83, bootable
start=94188, type=7
EOF

lodevice=$(sudo losetup --partscan --show --find template.img)


sudo mkfs.ext4 -i 1024 -L boot -v ${lodevice}p1
sudo mount ${lodevice}p1 /tmp/part1
sudo cp /boot/config-*-generic /boot/memtest86*x64.* /boot/System.map-*-generic /tmp/part1
for i in 36 39; do
    sudo touch /tmp/part1/vmlinuz-6.2.0-$i-generic
    sudo touch /tmp/part1/initrd.img-6.2.0-$i-generic
done
sudo chmod o-rwx,g-rwx /tmp/part1/v* /tmp/part1/i*
sudo mkdir /tmp/part1/{efi,grub}
sudo umount /tmp/part1


sudo mkfs.ntfs -L data -s 512 -c 512 -U -v ${lodevice}p2
sudo mount ${lodevice}p2 /tmp/part2 -o uid=$(id -u),gid=$(id -g)
for i in $(seq 0 7366); do
    head -c1024 /dev/urandom > /tmp/part2/A-$(mktemp -u | tail -c9) && echo -n -e "Randomizing $i...\r" 1>&2
done
for i in $(ls /tmp/part2 | head -n1100); do
    rm /tmp/part2/$i
done
echo 1>&2

cat decr.py > /tmp/part2/Moi\ rashifrovhik.py
for i in $(seq -w 00000 65535); do
    echo -n "<d$i>" >> /tmp/part2/Zashifrovannye\ dannye.bin
    echo -n "<k$i>" >> /tmp/part2/Klych\ shifrovania.bin
    echo -n -e "Putting data $i...\r" 1>&2
done
echo 1>&2
rm /tmp/part2/A-*

sudo umount /tmp/part2


sudo losetup -d $lodevice
rmdir /tmp/part1 /tmp/part2

sfdisk --delete template.img 2
