# Install sber application on IOS

## Before app installation

### Download sber app and put it into ios-apps folder.

For example:

```bash
mkdir ios-apps
sudo apt update
sudo apt install curl
curl https://ipsw.guru/IPSW/%D0%A1%D0%B1%D0%B5%D1%80%D0%91%D0%B0%D0%BD%D0%BA%2012.15.0\[tg@iapps_ipa\].ipa -o ./ios-apps/sberbank.ipa
```

## How to start app

On debian-based linux distributions:

```bash
sudo apt update
sudo apt install usbmuxd make
make run-docker-container
```
