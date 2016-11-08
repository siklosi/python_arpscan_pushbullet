# python_arpscan_pushbullet
Python local network scanner with pushbullet notification on new device

Script logs all new devices in "known" file in scripts path and sends pushbullet notification when new device is detected. "known" file lines should begin with mac address. Delimited with space after mac address can be any text used as description. Script can be added to cron and reports when new device is conected to local network.
