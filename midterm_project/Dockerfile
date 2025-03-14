FROM python:3.12

COPY requirments.txt /code/requirments.txt

RUN pip3 install -r /code/requirments.txt

COPY iss_tracker.py /code/iss_tracker.py

COPY test_iss_tracker.py /code/test_iss_tracker.py

RUN chmod +rx /code/iss_tracker.py 

EXPOSE 5000

ENV PATH="/code:$PATH"

CMD ["iss_tracker.py"]