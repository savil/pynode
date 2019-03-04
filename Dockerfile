# instructions https://github.com/docker-library/docs/blob/master/python/README.md

FROM python:3.7.2

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

CMD [ "python", "./your-daemon-script.py" ]
