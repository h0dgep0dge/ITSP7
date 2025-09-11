# Installing

## Installing Debian on the Firebox M4600

The Firebox boots from an internal memory card, my first step was to install GRUB2 to the memory card, and configure it to use the serial console.
With GRUB2 booted, it's easy enough to chainload a USB installation media, but the tricky part is getting the installation media to use the serial console.
To achieve this for Debian I used the Live Build system to create a customer image, with the correct settings to make the bootloader and kernel use the serial console.