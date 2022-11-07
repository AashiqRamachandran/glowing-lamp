FROM public.ecr.aws/lambda/python:3.7
COPY . .
RUN pip3 install numpy==1.21.6
RUN pip3 install cython
RUN pip3 install pandas==1.3.5
RUN pip3 install scipy==1.7.3
RUN pip3 install joblib==1.2.0
RUN pip3 install threadpoolctl
RUN pip3 install -r requirements.txt
RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader stopwords
RUN python3 -m nltk.downloader wordnet
CMD [ "lambda_function.lambda_handler" ]