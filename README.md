# Starlink Engine Driver Application

This application is designed to manage and control Starlink engine systems using a Raspberry Pi. It integrates with relays to control engine operations and utilizes an MPU9250 sensor to handle the rotation mechanism's orientation. The system ensures precise alignment and control by monitoring and adjusting the orientation of the engines based on real-time data from the MPU9250 sensor.

## Configuring `eth0` Connection

1. Edit the `/etc/network/interfaces` file:
    ```bash
    sudo nano /etc/network/interfaces
    ```

2. Add the following configuration:
    ```bash
    auto eth0
    iface eth0 inet static
    address 192.168.161.42
    netmask 255.255.255.0
    gateway 192.168.1.1
    ```

3. Restart the networking service:
    ```bash
    sudo systemctl restart networking
    ```

## Run at Startup

Use `crontab` to run `launcher.sh` at startup:

1. Ensure `launcher.sh` has executable permissions:
    ```bash
    chmod +x /path/to/your/launcher.sh
    ```

2. Edit the crontab file using the following command:
    ```bash
    crontab -e
    ```

3. Add the following line to the crontab file:
    ```bash
    @reboot sh /path/to/your/launcher.sh >/home/user/logs/cronlog 2>&1
    ```


## Run watchdog

To set up a cron job to run `watchdog.sh` every minute:

1. Ensure `watchdog.sh` has executable permissions:
```bash
chmod +x /path/to/your/watchdog.sh
```

2. Edit the crontab file using the following command:
```bash
crontab -e
```

3. Add the following line to the crontab file:
```bash
* * * * * /path/to/your/watchdog.sh
```

## Disabling WiFi and Bluetooth

To disable WiFi and Bluetooth, you can edit the `/boot/firmware/config.txt` file or use `crontab` to apply the settings at startup.

1. Edit the `/boot/firmware/config.txt` file:
```bash
sudo nano /boot/firmware/config.txt
```

2. Add the following lines in the end of the file to disable WiFi and Bluetooth:
```bash
dtoverlay=disable-wifi
dtoverlay=disable-bt
```

3. Save the file and reboot your system:
```bash
sudo reboot
```
