FROM public.ecr.aws/lambda/python:3.8
COPY . .
RUN pip3 install numpy==1.21.6
RUN pip3 install cython
RUN pip3 install pandas==1.3.5
RUN pip3 install scipy==1.7.3
RUN pip3 install joblib==1.2.0
RUN pip3 install threadpoolctl
RUN pip3 install -r requirements.txt
CMD [ "lambda_function.lambda_handler" ]