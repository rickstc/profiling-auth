FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY configs/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY profiling-authentication/requirements.txt /code/
RUN pip install -r requirements.txt
ENTRYPOINT [ "/entrypoint.sh" ]