# Serverless-Media-Upload-Hub-AWS-Lambda-with-S3-and-DynamoDB-
This project outlines a serverless media upload hub built using AWS Lambda, S3, and DynamoDB. It enables users to upload media files through a web interface, storing the files in S3 and their associated metadata in DynamoDB.

## Features

*   **Serverless Backend:** Utilizes AWS Lambda for efficient and scalable processing without managing servers.
*   **Object Storage:** Employs Amazon S3 for durable and highly available storage of media assets.
*   **Data Management:** Uses Amazon DynamoDB for flexible and fast storage of media metadata.
*   **User-Friendly Interface:** Provides a simple web form for media uploads.
## Project Architecture Diagram

## Project Walkthrough and Components

Here are the key aspects of the project, illustrated with screenshots:

### 1. Upload Interface

This image shows the web form used for uploading media, where users input a name, caption, and select a file.


### 2. IAM Role Permissions

Details of the IAM role permissions granted to the Lambda function, allowing it to interact with S3 and DynamoDB.


### 3. Lambda Function Code

A view of the Python code for the AWS Lambda function, which orchestrates the upload to S3 and data entry into DynamoDB.


### 4. Lambda Layer Configuration

The configuration for the `mylayer` Lambda layer, used for managing dependencies.


### 5. S3 Bucket Overview

The Amazon S3 bucket (`lamdawithdynadb`) where the media files are stored.


### 6. DynamoDB Table Entries

The `reels` DynamoDB table displaying the metadata for uploaded items, including `id`, `caption`, `file_url`, and `name`.


### 7. Successful Upload Confirmation

The confirmation message displayed on the web interface after a successful media upload, showing the stored details and file URL.


## High-Level Deployment Steps

To set up this project:

1.  Configure an S3 bucket for media storage.
2.  Set up a DynamoDB table for metadata.
3.  Create an IAM role with necessary permissions for Lambda, S3, and DynamoDB.
4.  Develop and deploy the AWS Lambda function.
5.  Optionally, create and attach a Lambda layer for dependencies.
6.  Integrate with API Gateway to expose the Lambda function via HTTP.
7.  Develop a simple frontend to interact with the API Gateway.


---
