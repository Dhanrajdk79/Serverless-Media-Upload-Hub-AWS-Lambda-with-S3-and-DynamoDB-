import boto3
import base64
import os
import uuid
from requests_toolbelt.multipart import decoder

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

BUCKET_NAME = os.environ.get("BUCKET_NAME", "majhidisablewali")
TABLE_NAME = os.environ.get("TABLE_NAME", "reels")
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method", "GET")

    # Serve HTML form
    if method == "GET":
        html_form = """
        <html>
        <head><title>Upload Form</title></head>
        <body>
            <h2>Upload File with Name & Caption</h2>
            <form action="" method="post" enctype="multipart/form-data">
                Name: <input type="text" name="name"><br><br>
                Caption: <input type="text" name="caption"><br><br>
                File: <input type="file" name="file"><br><br>
                <input type="submit" value="Upload">
            </form>
        </body>
        </html>
        """
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": html_form
        }

    # Handle POST request
    elif method == "POST":
        try:
            body = base64.b64decode(event["body"])
            content_type = event["headers"].get("content-type") or event["headers"].get("Content-Type")

            multipart_data = decoder.MultipartDecoder(body, content_type)

            name, caption, file_content, filename = None, None, None, None

            for part in multipart_data.parts:
                cd = part.headers[b'Content-Disposition'].decode()
                if 'name="name"' in cd:
                    name = part.text
                elif 'name="caption"' in cd:
                    caption = part.text
                elif 'name="file"' in cd:
                    file_content = part.content
                    if "filename=" in cd:
                        filename = cd.split("filename=")[1].strip('"')

            if not (name and caption and file_content):
                return {"statusCode": 400, "body": "Missing fields"}

            # Save file to S3
            unique_name = str(uuid.uuid4()) + "_" + (filename or "upload.bin")
            s3_key = f"uploads/{unique_name}"
            s3.put_object(Bucket=BUCKET_NAME, Key=s3_key, Body=file_content)

            file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_key}"

            # Save record in DynamoDB
            table.put_item(
                Item={
                    "id": str(uuid.uuid4()),
                    "name": name,
                    "caption": caption,
                    "file_url": file_url
                }
            )

            success_html = f"""
            <html>
            <body>
                <h2>Upload Successful!</h2>
                <p><b>Name:</b> {name}</p>
                <p><b>Caption:</b> {caption}</p>
                <p><b>File URL:</b> <a href="{file_url}" target="_blank">{file_url}</a></p>
            </body>
            </html>
            """
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "text/html"},
                "body": success_html
            }

        except Exception as e:
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "text/plain"},
                "body": f"Error: {str(e)}"
            }
