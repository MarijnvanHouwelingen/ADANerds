# Using python 3.10 slim image as the base image
FROM python:3.10.7-slim
# Defining working directory and copy the requirements file. We will run the commands inside this new directory
WORKDIR /usr/src/myapp
# Copy requirements.txt  to the working directory
COPY requirements.txt .
# Install required python packages
RUN pip install --no-cache-dir -r requirements.txt
# Copy the service account key file into the container
COPY my-service-account.json .
# Set the environment variable for Google Cloud authentication
ENV GOOGLE_APPLICATION_CREDENTIALS service-account-file.json
# Copy FAAS files into the FAAS directory
COPY FAAS /usr/src/myapp/FAAS/
# Copy all RestfulAPI files using the same structure
COPY . /usr/src/myapp/Restful-API/
# Expose the port that our app runs in
EXPOSE 5000

# General Enviroment Variables
ENV DB_URL  sqlite:///datalodge.db
ENV GOOGLE_CLOUD_PROJECT_ID emerald-diagram-413020
ENV GOOGLE_CLOUD_BUCKET_NAME picture_ass2

# Listing topic ID
ENV LISTING_TOPIC_ID create/update_listing
ENV LISTING_SUBSCRIPTION_ID listing-service-subscription

# booking,refund,status topic ID
ENV BOOKING_TOPIC_ID booking_refund
ENV REFUND_SUBSCRIPTION_ID refund-service-subscription
ENV REFUND_STATUS_TOPIC_ID refund_status
# Run our App
CMD ["python3","/usr/src/myapp/Restful-API/app.py"]