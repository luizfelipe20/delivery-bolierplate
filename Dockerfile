# FROM python:3
# ENV PYTHONUNBUFFERED=1
# RUN mkdir /code
# WORKDIR /code
# COPY requirements.txt /code/
# RUN pip install -r requirements.txt
# COPY . /code/
# EXPOSE 80

FROM python:3
ENV PYTHONUNBUFFERED=1
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 80
CMD sh /usr/src/utils/run.sh