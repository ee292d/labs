# Lab 0: Set Up Your Raspberry Pi

This tutorial shows how to set up your laptop and Raspberry Pi 5 board to run
the rest of the machine learning labs in EE292D.

  - [Hardware Required](#hardware-required)
    - [Links to Buy](#links-to-buy)
    - [Other equipment](#other-equipment)
  - [Remote or Local Development?](#remote-or-local-development)
  - [Flash an SD Card](#flash-an-sd-card)
    - [Image](#image)
    - [Configure settings](#configure-settings)
    - [Check that the Pi boots](#check-that-the-pi-boots)
  - [Connect the Touch Display](#connect-the-touch-display)
    - [Connect the power wires](#connect-the-power-wires)
    - [Connect the data wires](#connect-the-data-wires)
    - [Mechanically attach the Pi to the display (optional)](#mechanically-attach-the-pi-to-the-display-optional)
    - [Power up the display](#power-up-the-display)
    - [Find your IP address](#find-your-ip-address)
  - [Install VS Code](#install-vs-code)
    - [Set up the Remote SSH extension](#set-up-the-remote-ssh-extension)
    - [Add your Pi as a host](#add-your-pi-as-a-host)
    - [Connect to to the Pi](#connect-to-to-the-pi)
    - [Troubleshoot connection issues](#troubleshoot-connection-issues)
    - [Download the code](#download-the-code)
  - [Next Steps](#next-steps)

## Hardware Required

You'll need the following pieces of equipment to complete this guide:

 - Raspberry Pi 5 8GB.
 - Raspberry Pi 27W USB-C Power Supply
 - Raspberry Pi Touchscreen 2
 - Blank Micro SD Card.
 - Micro SD Card Reader.
 - Laptop.

If you're a Stanford student on the course you will be provided with the 
equipment you need, but for anyone else following along, here are links to the
hardware I purchased. These are US resellers, but as long as you make sure 
you're buying the same hardware, versions bought from elsewhere should work
with no differences.

### Links to Buy

 - [Raspberry Pi 5 8GB at Adafruit](https://www.adafruit.com/product/5813)
 - [Official Raspberry Pi 27 Watt Power Supply](https://www.adafruit.com/product/5814). The Pi will still boot with the older 15 Watt power supply, but it may not be able to run all peripherals.
 - [Raspberry Pi Touch Display 2](https://www.adafruit.com/product/6079). Version 1 of the official touch display can be used in a pinch, but the connectors are a bit harder to set up.
 - [256 GB SanDisk MicroSD Card](https://www.amazon.com/dp/B082WNC4NK). I prefer name brands for reliability, and since we're doing a lot with data in this course, having at least 256GB is recommended.
  - [USB C SD Card Reader](https://www.amazon.com/dp/B09T5K56ZZ). If your laptop already has a built-in SD card reader, you won't need this.
  - Laptop. No links for this, since the tutorials should work with Windows, Mac, or Linux machines. I haven't tested with ChromeOS, and it's pretty locked-down by default, so I wouldn't go that route unless you're knowledgeable about ChromeBook modifications.

### Other equipment

If you want to screw the Pi to the touch display, you'll need a Phillips 
screwdriver with a very small head.

For [Lab 2](https://github.com/ee292d/labs/blob/main/lab2/README.md), you'll also need a camera and adaptor cable:

 - [Raspberry Pi Camera Module v2](https://www.raspberrypi.com/products/camera-module-v2/)
 - [Raspberry Pi Mini to Standard Camera Cable](https://www.raspberrypi.com/products/camera-cable/)

For [Lab 4](https://github.com/ee292d/labs/blob/main/lab4/README.md) you'll need a USB microphone and speakers or headphones.

## Remote or Local Development?

The easiest way to use a Raspberry Pi is to connect it to a full-size monitor, 
keyboard, and mouse. This lets you run a code editor directly on the desktop, 
configure the Wifi with a GUI, and execute commands in a terminal.

This does make the setup very hard to move around though, which isn't great 
when you need to bring it to class or deploy it in a production environment.
Real applications are also likely to be easier to debug if you can log in 
remotely without needing physical access to the device.

You can work through all of these labs using local access, the steps will be
be very similar, especially since VS Code can run on the Raspberry Pi desktop,
but I do recommend at least considering investing time setting up remote 
access. The rest of this lab walks you through the steps required to log into 
your Pi from a laptop. Some of it depends on the details of your own Wifi 
network so it can be a bit frustrating, but once you have it working it should
save you time in the end.

## Flash an SD Card

Raspberry Pis use an SD card as their default drive for storage and the
operating system. The first step to setting up your new board is to burn a new
card with an OS. I recommend picking a card with at least 32GB of space, and
preferably more if possible, since this is also where you'll put your working
files during development.

### Image

On your laptop, download the Raspberry Pi Imager tool for your operating system
from [raspberrypi.com/software/](https://www.raspberrypi.com/software/).

Insert an SD card into the laptop's reader.

Open the Imager tool.

<image src="doc_images/imager0.png" width="400px"/>

Select "Raspberry Pi 5", "Raspberry Pi OS (64-bit)", and the reader device.

<image src="doc_images/imager1.png" width="400px"/>

<image src="doc_images/imager2.png" width="400px"/>

<image src="doc_images/imager3.png" width="400px"/>

Press "Write" and choose "Edit Settings" on the dialog that appears.

### Configure settings

<image src="doc_images/imager4.png" width="400px"/>

On the default settings tab, choose a network name for your board (like 
*your name*-pi5, petes-pi5 in my case) and make a note of it, since it may be
helpful for connecting later. If you're doing this in a classroom with other 
people, you'll want to make sure the name is unique to your board, so you might
need to add your last name if someone else shares your first name, for example
pete-wardens-pi5.

<image src="doc_images/imager5.png" width="400px"/>

Enter your preferred user name and password, and make a note of these too.

Enter the name and password of your Wifi network (or prefill it from the 
keychain). If you are using a network like Stanford's that requires 
completing a browser-based login page, you can leave out this Wifi 
information, since we'll use the touchscreen to connect after booting.

<image src="doc_images/imager6.png" width="400px"/>

Then go to the services tab and enable SSH. You've got a choice about how you
want to connect to the board. Choosing password might be simpler, but if you 
run ssh-keygen then you can log in from the laptop without having to type
anything. If you want to log in from other devices you'll have to add their ssh
keys too at a later stage.

Choose "Yes" to apply the settings, and "Yes" again to erasing any existing
data on the card.

<image src="doc_images/imager7.png" width="400px"/>

Writing will take a few minutes. Once it's complete, take the card from the
reader and insert it into the Raspberry Pi. Make sure the SD card is inserted
so that its metal contacts are facing towards the board. The SD slot is on the
underside of the board.

<image src="doc_images/sdcard_inserted.jpg" width="400px"/>

### Check that the Pi boots

Plug the power supply into the wall, and then into the USB C plug on the 
Raspberry Pi. You should see a green LED near the USB C plug light up if it's
receiving power.

<image src="doc_images/power_led.jpg" width="400px"/>

If the LED doesn't come on at all, then you should check that your power supply
is plugged in, and then test it with another USB C device, like your phone, to
ensure it is actually supplying power.

If it settles into a steady blinking pattern that continues for a couple of
minutes, then the board is in an error state. Double check that the SD card is
firmly in the socket. If that doesn't fix it, then you can look at [this guide](https://forums.raspberrypi.com/viewtopic.php?t=58151#p1485558)
to the errors associated with each pattern, and other steps to help you
troubleshoot booting problems.

## Connect the Touch Display

Even if you have a Wifi network that doesn't require a browser-based login
process, having a touchscreen display attached makes debugging issues a lot
easier. The most important piece of information we'll need to set up remote
development is the IP address of the Pi on the local Wifi network. While
there are other ways to obtain it, the simplest is to make a note of it when
it's displayed as a notification on the desktop after booting the board.

Here's my step-by-step recipe, and the official docs have [a good guide on setting up the Touchscreen 2](https://www.raspberrypi.com/documentation/accessories/touch-display-2.html)
too.

Before you start, make sure the Pi is disconnected from its power supply. The
voltage should be too low to cause you any harm, but there's a chance something
could short-circuit and damage your board if you connect pins while the board
is running. Also touch something metal, like your laptop, to discharge any
static electricity.

### Connect the power wires

Unpack the touchcreen and you should find a red and a black wire that
joins two white plastic connectors.

<image src="doc_images/i2c_full_cable.jpg" width="400px"/>

This supplies power to the touchscreen from the Pi. First make sure that you
turn the smaller connector so that the metal contacts are facing towards you,
and away from the touchscreen.

<image src="doc_images/i2c_ts_end.jpg" width="400px"/>

Then insert the smaller connector into the pins on the back of the touchscreen,
that face one of the long sides of the display. The connector will only fit in
one orientation, so make sure that you do have the metal contacts facing away
from the touchscreen and towards you. You shouldn't need too much force to 
insert the connector, and once in it should feel snug, not loose.

<image src="doc_images/i2c_ts_inserted.jpg" width="400px"/>

Take the connector on the other end, and attach it to the long row of pins on
the Pi. The red wire should connect to the pin nearest the corner of the board,
on the outermost row, and the black wire should connect to the pin that's two
down, also on the outermost row. The small plastic ledge on the connector
should be turned away from the board. This connection should also require 
little force to insert, and feel snug and well-seated.

<image src="doc_images/i2c_pi_inserted.jpg" width="400px"/>

### Connect the data wires

So far we've supplied power to the display, but we also need it to receive
video input from the Pi, and any send touch information back in return. There's
a special cable included with the Touch Display for this, it's flat and orange,
with a swerve in the middle.

<image src="doc_images/ribbon_full_cable.jpg" width="400px"/>

The wider end goes into the touch screen. You will need to use your fingernails
to loosen the black plastic tab in the ribbon connector on the display first.
You only need to pull it out a small amount, so that it's loose but still in 
the socket. If you accidentally pull it completely out, don't worry, you can
always reinsert it.

Slide the wide end of the ribbon cable into the slot, with the gold contacts
facing you, away from the display. Once it's fully in, push the black tab back
into the socket. This should lock the cable in place, so it stays in place if
you give it a gentle tug. Pushing the tab back in can be very fiddly, and I
often feel like I need three hands to do it. You should hold the ribbon in
place while you simultaneously press down on both sides of the tab, I use my
thumbnails for this.

One of the most common reasons for the touch display to not work is a 
misalignment in the ribbon cable connectors on either end, so make sure that
the ribbon is well inserted, and perpendicular to the connector.

<image src="doc_images/ribbon_ts_inserted.jpg" width="400px"/>

Now we'll insert the narrower end of the ribbon cable into one of the Pi's
display ports. The Raspberry Pi 5 has two of these, and both should work, but
I tend to use the one nearest the Ethernet port on the board. They're white,
with black plastic tabs like the touch screen's ribbon port. As before, gently
pull the black tab out of your chosen display port. Once its loose, you should
be able to insert the ribbon cable, with the gold contacts facing towards the
USB and Ethernet port end of the board. When it's firmly and squarely in, 
wiggle the tab back into place so that the ribbon is locked. As before, take
extra care with this step, and check that it truly is square if you are having
problems getting the display to work.

<image src="doc_images/ribbon_pi_inserted.jpg" width="400px"/>

### Mechanically attach the Pi to the display (optional)

The Pi has four screwholes, one in each corner of the board, and the Touch
Display has four pillars that you can use to attach the Pi to the screen. This
is purely optional, it makes the board a little more awkward to handle, but I
do find that it helps me to avoid accidentally tugging out the cables. You
should have found some small black screws in the display packaging. You can use
these to attach the board.

<image src="doc_images/black_screws.jpg" width="400px"/>

I don't recommend attaching the board before you have connected the power and
data cables, since it can be tricky to access those ports on the display once 
the Pi is in place.

The easiest way I've found to start is by inserting a screw into one corner
of the board, pushing a small Phillips screwdriver into the screw's head to 
help hold it in place, and then moving the board and screwdriver together until
you can insert the screw into one of the pillars. Once you have one pillar
attached, it should be possible to rotate the board around it until the other
holes are in the right position, then place each screw on the end of your 
screwdriver and hold it in place as you transfer it to a hole.

### Power up the display

when you have all the cables in place you should reinsert the USB C power
supply. If everything is working correctly you should see a screen that says
"Welcome to the Raspberry Pi Desktop" appear after a few seconds.

<image src="doc_images/boot.jpg" width="400px"/>

If you have set your username, Wifi, and other details through the customize
settings dialog when you flashed your SD card, it will then boot directly into
the desktop. If not, you'll be guided through a step-by-step process to enter
all the required information when you first boot.

If you are on a Wifi network that requires a login page, you should be able to
trigger this by picking the network from the Wifi icon at the right of the top
menu bar that extends across the screen, and then opening your browser (the 
globe symbol on the left of the menu bar) and navigating to a page like 
google.com.

### Find your IP address

When you're connected to a Wifi network and boot up your board, the numerical 
IP address of your Pi will appear for a few seconds as a notification just 
below the Wifi icon in the menu bar. You'll need this information for remote
development.

<image src="doc_images/ip_notification.jpg" width="400px"/>

Don't worry if you don't write the IP address down before the notification
disappears, you can find it from the Wifi settings at any time. Tap on the
Wifi icon in the menu bar, choose "Advanced Options" at the bottom of that
menu, and then choose "Connection Information" in the submenu.

<image src="doc_images/connection_menu.jpg" width="400px"/>

That should bring up a window that includes a lot of information about your
network connection. The address you want is the IP Address below IPv4. In
this screenshot, that's 192.168.4.54.

<image src="doc_images/ip_connection_info.jpg" width="400px"/>

## Install VS Code

Go to [code.visualstudio.com/download](https://code.visualstudio.com/download)
and download the installer for your laptop's operating system. Follow the
instructions to install the application, and then open a new window.

Make sure the board is powered on and shows the desktop on the touch display,
and then with your laptop connected to the same Wifi network the Pi is
connected to, and then open VS Code.

### Set up the Remote SSH extension 

The Remote SSH extension in VS Code lets you easily edit files and run commands
on the Pi from your laptop. To configure this, open a new VS Code window and 
click on the Extensions icon in the left sidebar. Search for "Remote SSH" and
install the "Remote - SSH" extension from Microsoft.

<image src="doc_images/vscode1.png" width="400px"/>

### Add your Pi as a host

After it has installed, click the newly-added Remote Explorer icon on the
sidebar. When you mouse over the SSH heading, you should see a plus icon to the
right. 

<image src="doc_images/vscode5.png" width="400px"/>

Click on that, and type in the same address that you noted down from the 
earlier steps, and the username you picked when flashing the SD card. 

For example, if you picked the username `petewarden` and the IP address of the
board is 192.168.86.29, you would enter `ssh petewarden@192.168.86.29` into the
text field. 

<image src="doc_images/vscode6.png" width="400px"/>

You'll be asked if you want to update your SSH settings, and you should choose
the default location.

<image src="doc_images/vscode7.png" width="400px"/>

### Connect to to the Pi

Once you've completed adding your Pi as a host, you should see an option to 
connect to it.

<image src="doc_images/vscode8.png" width="400px"/>

When you select it you should see a new window appear. If you're using a 
password, you'll see a prompt to enter your password at the top. Once you're
logged in there should be a few progress messages such as "Downloading VS Code
Server". After they complete, you should see a small connection message in the
bottom left of the window that says `SSH: 192.168.86.29`, but with your Pi's IP
address.

<image src="doc_images/vscode10.png" width="400px"/>

### Troubleshoot connection issues

If you are seeing error messages, I recommend going through this checklist:

 - Make sure your laptop and Pi are on the same Wifi network.
 - Ensure that the SSH server that listens for connections is enabled on the 
Pi. This should have happened in the Advanced Settings dialog during the 
flashing process, but if you forgot to do it then, you can open up a terminal
on the Pi, run `sudo raspi-config`, select `Interfacing Options`, pick `SSH`,
and then choose "Yes" to turn it on.
 - Check to see if the IP address of the board has changed since you noted it
down. Some networks assign a new IP address every time the Pi reboots, so 
follow [the instructions above](#find-your-ip-address) to check it from the 
Wifi menu.

### Download the code

If that process worked, choose "Clone Git Repository..." from the options on
the start screen, and enter `https://github.com/ee292d/labs` when asked for the
URL. 

<image src="doc_images/vscode11.png" width="400px"/>

Choose your user's home folder as the destination (this will look like 
`/home/username` and should be the default choice). 

<image src="doc_images/vscode12.png" width="400px"/>

After it has downloaded, you'll be asked if you'd like to open the repository,
choose yes.

<image src="doc_images/vscode13.png" width="400px"/>

Then you'll be asked if you trust the authors of the repository, and you should
choose yes to enable all the VS Code features.

<image src="doc_images/vscode14.png" width="400px"/>

You should now be in a window that shows the contents of this repository in the
left-hand pane. If you choose "Terminal->New Terminal" from the menu you can
bring up a shell running on the board. You can now edit files and run commands
on the Pi directly from your laptop, which is often a lot easier than other
approaches to coding on the board.

## Next Steps

You should now have a fully-working Raspberry Pi 5 that you can program using
Visual Studio Code from your laptop. You're now ready to learn about all the
machine learning applications you can build on the system, using [the rest of the
labs](https://github.com/ee292d/labs).