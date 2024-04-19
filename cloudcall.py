import os
import shutil
import subprocess
import re

# Define local file paths
download_path = "/home/ec2-user"
extract_path = "/home/ec2-user/cloudcall"

# AWS S3 configurations
s3_bucket_name = 'carrerdoc-cloudcall'

# Read file URLs from a text file
#file_urls_path = "/home/ec2-user/file_urls.txt"
file_urls_path = "/home/ec2-user/file_urls_cloudcall.txt"

with open(file_urls_path, 'r') as file:
    file_urls = file.readlines()

# Loop through each file URL
for file_url in file_urls:
    file_url = file_url.strip()  # Remove leading/trailing whitespace or newline characters

    if not os.path.exists(extract_path):
        os.mkdir(extract_path)
    pattern = r'\d{4}_\w{3}'
    match = re.search(pattern, file_url)
    matched_date = match.group()
    extract_path2 = f"{extract_path}/{matched_date}"
    if not os.path.exists(extract_path2):
        os.mkdir(extract_path2)

    # Download the file using wget
    subprocess.run(["wget", file_url, "-P", download_path, "-O", f"{download_path}/{matched_date}.zip"])

    # Extract the downloaded file using unzip command
    zip_file = f"{download_path}/{matched_date}.zip"
    print(f"unzip {zip_file} -d {extract_path2}")
    subprocess.run(["unzip", "-P", "MQihUB[m{sInS83Hpr#y", zip_file, "-d", extract_path2])

    # Get the name of the zip file without the extension
    zip_file_name = os.path.splitext(os.path.basename(file_url))[0]

    print(f"aws s3 cp {extract_path2} s3://{s3_bucket_name}/{matched_date} --recursive")
    subprocess.run(["aws", "s3", "cp", extract_path2, f"s3://{s3_bucket_name}/{matched_date}", "--recursive"])

    # Upload the extracted files to S3 in their own directory
#    for root, dirs, files in os.walk(extract_path):
#        for file in files:
#            local_path = os.path.join(root, file)
#            s3_key = os.path.relpath(local_path, extract_path)
#            s3_directory = os.path.join(zip_file_name, os.path.dirname(s3_key))
#            s3_object_key = os.path.join(zip_file_name, s3_key)


    print(f"Files from '{zip_file}' uploaded to S3 successfully.")

    # Clean up extracted files
    shutil.rmtree(extract_path2)
    os.remove(zip_file)

print("All files uploaded to S3 and cleaned up.")
