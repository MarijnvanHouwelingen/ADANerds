# Using python 3.10 slim image as the base image
FROM python:3.10.7-slim
# Defining working directory and copy the requirements file. We will run the commands inside this new directory
WORKDIR /usr/src/myapp
# Copy requirements.txt  to the working directory
COPY requirements.txt .
# Install required python packages
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for Google Cloud authentication
# ENV GOOGLE_APPLICATION_CREDENTIALS service-account-file.json

# Copy all Account bounded context files using the same structure
COPY . .
# Expose the port that our app runs in
EXPOSE 5000

# General Enviroment Variables
ENV DB_URL  bigquery://emerald-diagram-413020/accountdb
ENV GOOGLE_CLOUD_PROJECT_ID emerald-diagram-413020

ENV ACCOUNT_TOPIC_ID report_users
# Run our App
CMD ["python3","app.py"]