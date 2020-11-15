FROM python:3.7
RUN apt-get update
RUN apt-get install -y redis-server
#ADD . /backend
COPY backend /backend
WORKDIR /backend
RUN pip install -r requirements.txt
# This should be done using gunicorn
ENTRYPOINT ["python"]
CMD ["app.py"]
