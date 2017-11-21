FROM python:3.6.3
RUN pip install pandas-datareader
RUN pip install scipy
RUN pip install boto3
COPY /src/queue_processor.py queue_processor.py
COPY /src/worker.py worker.py
CMD ["python", "queue_processor.py"]