## Installing CentOS Stream on the Firebox M4600

### Bootstrapping

I haven't found a way to configure the boot device of the Firebox, and by default it boots from the internal CFast flash card.
To get installation media booted, I removed the CFast card, attached it to my computer by an adapter, and installed the Grub bootloader to the card, using the following steps.

1. Erase the partition table with `dd`
2. Create a new partition with `fdisk`
3. Write a new ext4 filesystem with `mkfs.ext4`
4. Mount the filesystem with `mount`
5. Install the grub bootloader with `grub-install`
6. Install a config file that enables the serial console

~~~
# dd if=/dev/zero of=/dev/sdX count=1
1+0 records in
1+0 records out
512 bytes copied, 0.00607499 s, 84.3 kB/s
# fdisk /dev/sda

Welcome to fdisk (util-linux 2.41).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Device does not contain a recognized partition table.
Created a new DOS (MBR) disklabel with disk identifier 0x9da1a380.

Command (m for help): n
Partition type
   p   primary (0 primary, 0 extended, 4 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (1-4, default 1): 1
First sector (2048-4194303, default 2048): 2048
Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-4194303, default 4194303): +1G

Created a new partition 1 of type 'Linux' and of size 1 GiB.

Command (m for help): w
The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.

# mkfs.ext4 /dev/sda1
mke2fs 1.47.2 (1-Jan-2025)
Creating filesystem with 262144 4k blocks and 65536 inodes
Filesystem UUID: 7d4f6118-4ebf-4e90-99b3-74f86863529c
Superblock backups stored on blocks: 
	32768, 98304, 163840, 229376

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (8192 blocks): done
Writing superblocks and filesystem accounting information: done

# mkdir mnt
# mount /dev/sda1 mnt
# grub-install --target=i386-pc --boot-directory=/root/mnt /dev/sdX
Installing for i386-pc platform.
Installation finished. No error reported.
~~~

The Firebox will boot from this, and present a grub console over the serial port.
Once the machine is booted to a grub console, chainloading a flashdrive is easy.

~~~
grub> set root='hd1,msdos1'
grub> chainloader +1
grub> boot
~~~

### Custom CentOS Installer

To create a CentOS installer that would work over the serial port of the Firebox, I replaced the ISOLINUX bootloader configuration file with a modified version that put the bootloader in serial console mode, and added a parameter to the text installer menu entry that started the linux kernel in serial console mode.

~~~
# xorriso -indev CentOS-Stream-9-20250922.0-x86_64-boot.iso -outdev CentOS-Serial.iso -compliance no_emul_toc -map ./isolinux.cfg isolinux/isolinux.cfg -boot_image any replay
xorriso 1.5.6 : RockRidge filesystem manipulator, libburnia project.

xorriso : NOTE : Loading ISO image tree from LBA 0
xorriso : UPDATE :      30 nodes read in 1 seconds
xorriso : NOTE : Detected El-Torito boot information which currently is set to be discarded
Drive current: -indev 'CentOS-Stream-9-20250922.0-x86_64-boot.iso'
Media current: stdio file, overwriteable
Media status : is written , is appendable
Boot record  : El Torito , MBR isohybrid cyl-align-on GPT
Media summary: 1 session, 678608 data blocks, 1325m data,  346g free
Volume id    : 'CentOS-Stream-9-BaseOS-x86_64'
Drive current: -outdev 'CentOS-Serial.iso'
Media current: stdio file, overwriteable
Media status : is blank
Media summary: 0 sessions, 0 data blocks, 0 data,  346g free
xorriso : UPDATE :       1 files added in 1 seconds
Added to ISO image: file '/isolinux/isolinux.cfg'='/home/rob/Downloads/isolinux.cfg'
xorriso : WARNING : -volid text does not comply to ISO 9660 / ECMA 119 rules
xorriso : NOTE : Replayed 21 boot related commands
xorriso : NOTE : Copying to System Area: 32768 bytes from file '--interval:imported_iso:0s-15s:zero_mbrpt,zero_gpt:CentOS-Stream-9-20250922.0-x86_64-boot.iso'
libisofs: NOTE : Aligned image size to cylinder size by 10 blocks
xorriso : UPDATE : Writing:      37216s    5.5%   fifo  98%  buf  50%
xorriso : UPDATE : Writing:     385024s   56.8%   fifo 100%  buf  50%  642.5xD 
ISO image produced: 677944 sectors
Written to medium : 678094 sectors at LBA 0
Writing to 'CentOS-Serial.iso' completed successfully.

# dd if=CentOS-Serial.iso of=/dev/sdX bs=4M
331+1 records in
331+1 records out
1388736512 bytes (1.4 GB, 1.3 GiB) copied, 0.109243 s, 12.7 GB/s
~~~

Changes to `isolinux.cfg`

~~~
# diff /media/rob/CentOS-Stream-9-BaseOS-x86_64/isolinux/isolinux.cfg isolinux.cfg 
8a9
> serial 0 115200
91c92
<   append initrd=initrd.img inst.stage2=hd:LABEL=CentOS-Stream-9-BaseOS-x86_64 inst.text quiet
---
>   append initrd=initrd.img inst.stage2=hd:LABEL=CentOS-Stream-9-BaseOS-x86_64 inst.text quiet console=ttyS0,115200
~~~