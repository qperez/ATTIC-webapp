FROM python:3.9-buster

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONPATH=/buticc_microservice
ENV PRODUCTIONMODE=YES

# Install dependencies:
COPY requirements.txt /buticc_microservice/requirements.txt
COPY web_app_buticc /buticc_microservice/web_app_buticc/
RUN pip install -r /buticc_microservice/requirements.txt

# RUN ls -la /web_app_buticc/*

#EXPOSE 5000
CMD ["python","/buticc_microservice/web_app_buticc/app/controller.py"]
