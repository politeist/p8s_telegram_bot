FROM alpine:latest
RUN apk add --no-cache gcc bash wget git \
      musl-dev py-pip python3 python3-dev \
    && rm -rf /var/cache/apk/*

RUN pip install --upgrade pip setuptools wheel
RUN mkdir /src
ADD . /src/
RUN pip install --upgrade pip \
        && pip install -r src/requirements.txt
ENV APP_DIR /src
EXPOSE 5000
EXPOSE 80
CMD ["python3.8", "src/main.py"]
