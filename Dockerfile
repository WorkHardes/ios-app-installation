FROM python:3.10-slim-buster

COPY poetry.lock pyproject.toml main.py /ios-apps /usr/src/sber-ios-install/

RUN apt-get update \
    && apt-get install -y curl perl g++ build-essential libusb-1.0-0-dev wget unzip build-essential git autoconf automake libtool-bin libplist-dev libusbmuxd-dev libssl-dev openssl pkg-config usbutils \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/libimobiledevice/libplist \
    && git clone https://github.com/libimobiledevice/libimobiledevice-glue \
    && git clone https://github.com/libimobiledevice/libusbmuxd \
    && git clone https://github.com/libimobiledevice/libimobiledevice \
    && git clone https://github.com/libimobiledevice/usbmuxd \
    && cd libplist && ./autogen.sh && make && make install && ldconfig \
    && cd ../libimobiledevice-glue && PKG_CONFIG_PATH=/usr/local/lib/pkgconfig ./autogen.sh --prefix=/usr && make && make install && ldconfig \
    && cd ../libusbmuxd && PKG_CONFIG_PATH=/usr/local/lib/pkgconfig ./autogen.sh && make && make install && ldconfig \
    && cd ../libimobiledevice && PKG_CONFIG_PATH=/usr/local/lib/pkgconfig ./autogen.sh --enable-debug && make && make install && ldconfig \
    && cd ../usbmuxd && PKG_CONFIG_PATH=/usr/local/lib/pkgconfig ./autogen.sh --prefix=/usr --sysconfdir=/etc --localstatedir=/var --runstatedir=/run && make && make install \
    && cd .. && rm -rf libplist libimobiledevice-glue libusbmuxd libimobiledevice usbmuxd

WORKDIR /usr/src/sber-ios-install/
RUN python3 -m pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install

CMD ["python3", "./main.py"]

VOLUME /dev/bus/usb
