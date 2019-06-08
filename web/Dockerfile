FROM tiangolo/uwsgi-nginx-flask:python3.7
RUN pip install prometheus_client
ADD website/ /app/website/
WORKDIR /app/website
CMD python ./main.py
