FROM public.ecr.aws/lambda/python:3.8
COPY . .
RUN pip3 install numpy
RUN pip3 install cython
RUN pip3 install pandas
RUN pip3 install scipy
RUN pip3 install joblib
RUN pip3 install threadpoolctl

RUN pip3 install -r requirements.txt
CMD [ "lambda_function.lambda_handler" ]