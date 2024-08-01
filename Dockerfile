FROM python

ENV DB_HOST=127.0.0.1
ENV DB_USER=myuser
ENV DB_PASSWORD=mypassword

ADD . /opt/gateway_application_full
WORKDIR /opt/gateway_application_full

RUN pip install -r requirements.txt

EXPOSE 5000
EXPOSE 5001
EXPOSE 5002
CMD ["python", "gateway_service.py"]




