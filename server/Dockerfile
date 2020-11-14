FROM python:3
ADD . /server
WORKDIR /code
COPY . .
#COPY requirements.txt /
RUN pip install -r requirements.txt
EXPOSE 5000
EXPOSE 5678
CMD python server.py