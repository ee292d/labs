
```bash
ulimit -l 200000
pip install --break-system-packages llama-cpp-python==0.1.77
sudo su
echo "*               soft   memlock        unlimited" >> /etc/security/limits.conf
echo "*               hard   memlock        unlimited" >> /etc/security/limits.conf
reboot
```