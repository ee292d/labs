# Lab 1: Deploy a person detector on RPI

## Requirements

 - Raspberry Pi 5 8GB.
 - Raspberry Pi Camera
 - USB keyboard and mouse.
 - HDMI display.
 - Blank SD card.
 - SD card reader.
 - Laptop.
 - Visual Studio Code application.

## Set up your Raspberry Pi

#### Flash an SD Card

On your laptop, download the Rapsberry Pi Imager tool for your operating system from [raspberrypi.com/software/](https://www.raspberrypi.com/software/).

Insert an SD card into the laptop's reader.

Open the Imager tool.

Select "Raspberry Pi 5", "Raspberry Pi OS (64-bit)", and the reader device.

Press "Write" and choose "Edit Settings".

Choose a network name for your board (like <your name>pi5) and make a note of it, since it can be helpful for connecting later.

Enter your preferred user name and password, and make a note of these too.

Enter the name and password of your Wifi network (or prefill it from the keychain).

Go to the services tab and enable SSH.

Choosing password might be simpler, but if you run ssh-keygen then you can log 
in from the laptop without having to type anything. If you want to log in from
other devices you'll have to add their ssh keys too at a later stage.

Choose "Yes" to apply the settings.

Writing will take a few minutes. Once it's complete, take the card from the reader and insert it into the Raspberry Pi. Make sure SD card is inserted so that its metal contacts are facing towards the board.

Plug the power supply into the wall, and then into the USB C plug on the 
Raspberry Pi. You should see a green LED near the USB C plug light up if it's
receiving power.

#### Install VS Code

Go to [code.visualstudio.com/download](https://code.visualstudio.com/download)
and download the installer for your laptop's operating system. Follow the
instructions to install the application, and then open a new window.

#### Remote login through SSH

Give the board a few minutes to boot, and then with your laptop connected to
the same Wifi network you entered into the Imager for the SD card, open a
terminal window in VS Code. You can do this by going to the main menu and
choosing "Terminal->New Terminal".

To make sure you can connect, type the following in the terminal, with the
name you gave to your Pi replacing 'petes-pi5', and the username you picked
instead of `petewarden` in the command:

```bash
ssh petewarden@petes-pi5.local
```

You should see a message like:

```bash
The authenticity of host 'petes-pi5.local (192.168.86.29)' can't be established.
```

This is normal for the first time you try to connect to a new host with SSH,
and you should reply 'yes' to the prompt.

If you chose to use a password, you should enter it when prompted, otherwise if you picked `ssh-keygen` during the SD card flashing, you'll be logged in automatically.

If all this is successful, you should see logs and a prompt, like this:

```bash
Linux petes-pi5 6.6.20+rpt-rpi-2712 #1 SMP PREEMPT Debian 1:6.6.20-1+rpt1 (2024-03-07) aarch64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sun Mar 24 12:21:33 2024 from 192.168.86.28
petewarden@petes-pi5:~ $ 
```

#### Troubleshooting Login Issues

Logging in remotely is one of the steps that's most likely to cause problems,
because there are so many variables that affect the process, from your laptop's
operating system, to the Wifi equipment, to the board itself. Here are some
techniques that can help fix common errors.

##### Finding the Address of the Board

If you've plugged in your board, have seen the green LED light up, and have 
waited five minutes, but the `ssh` command either hangs or reports an error,
your laptop may be having trouble finding the board on the Wifi network.

To get a better understanding of what's happening, try the following command,
with `petes-pi5` replaced by the name you gave your board.

```bash
ping petes-pi5.local
```

If the board is at that network address you should see a stream of messages
like these:

```bash
PING petes-pi5.local (192.168.86.29): 56 data bytes
64 bytes from 192.168.86.29: icmp_seq=0 ttl=64 time=16.664 ms
64 bytes from 192.168.86.29: icmp_seq=1 ttl=64 time=29.753 ms
```

If this works then the network address isn't the issue, there must be a problem
with the ssh password or certificate.

If you see this message however, it means the board isn't at the address you
used:

```bash
ping: cannot resolve petes-pi5.local: Unknown host
```

If you do see this, and you have double-checked that you got the name of your
board correct and you're on the right Wifi network, you can try finding its
numerical IP address instead. To do this you first need to find the local
numerical address of your laptop. If you're on MacOS or Linux, here's a command
that should give you what you need:

```bash
ifconfig | grep 192.168
```

This should give something like this as its result:

```bash
        inet 192.168.86.28 netmask 0xffffff00 broadcast 192.168.86.255
```

As a next step, we're going to use the `nmap` network mapping tool to find all
the devices on the same network that have an open port ready to receive SSH
commands. The port number for ssh is 22, so you run the scan like this 
(replacing `192.168.86` with the first three numbers you found in your laptop's
IP address).

```bash
nmap -p 22 --open 192.168.86.0/24
```

This searches through all the numerical addresses on your local network, 
looking for any with open SSH ports. If the board is on the network, you should
see something like this as the output:

```bash
Starting Nmap 7.94 ( https://nmap.org ) at 2024-03-24 12:52 PDT
Nmap scan report for petes-pi5.lan (192.168.86.29)
Host is up (0.015s latency).

PORT   STATE SERVICE
22/tcp open  ssh

Nmap done: 256 IP addresses (9 hosts up) scanned in 18.11 seconds
```

There might be more than one address in the logs, and it might not report the
name of the device. You can try substituting any numerical IP addresses you've found into the ssh command, like this:

```bash
ssh petewarden@192.168.86.29
```

If any of them allow you to log in, then it's likely you've found the right
address, and you should note it down to use instead of the text address in
future commands.

#### Connect the Display and Keyboard



#### Connect the Camera to the Pi


#### Power up the Pi

#### Connect to Wifi

### Install VS Code on your Laptop

#### Download the App

#### Find the IP address of your Pi

#### Create a Remote Connection

#### Download this Repository

### Run an Image Labeling Model

#### Install TFLite

```bash
python3 -m pip install tflite-runtime
```

#### Make sure TFLite is Working

```bash
cd labs/lab1
python3 label_image.py
```
