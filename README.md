# Install sber application on IOS

## Before app installation

### 1. Install jailbreak on IOS device with Checkra1n package.

- Firstly tap in bash:

```bash
wget -O - https://assets.checkra.in/debian/archive.key | gpg --dearmor | sudo tee /usr/share/keyrings/checkra1n.gpg >/dev/null
echo 'deb [signed-by=/usr/share/keyrings/checkra1n.gpg] https://assets.checkra.in/debian /' | sudo tee /etc/apt/sources.list.d/checkra1n.list
sudo apt-get update
sudo apt install checkra1n
```

- Find Checkra1n app in application launcher and start it.
- Activate in [ Options ]: [x] Allow untested iOS/iPadOS/tvOS versions; [x] Skip A11 BPR check.
- Tap [ Start ] and follow the instructions to jailbreak the device.

### 2. Download sber app and put it into ios-apps folder.

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
sudo apt install usbmuxd
sudo usbmuxd &> /dev/null &
make run-docker-container
```
