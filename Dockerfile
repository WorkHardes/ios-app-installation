FROM python:3.10-slim-buster

COPY poetry.lock pyproject.toml main.py sberbank.ipa /usr/src/sber-ios-install/

# Install app dependencies
WORKDIR /usr/src/sber-ios-install/

RUN python3 -m pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

VOLUME /dev/bus/usb

CMD ["python3", "./main.py"]
