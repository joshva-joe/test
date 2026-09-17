import boto3
import pandas as pd
from botocore.exceptions import ClientError

bucket = "opticpro"

df = pd.read_csv(r"C:\Sample\folders.csv")
s3 = boto3.client("s3", region_name="ap-south-1")

folders = df["Folder Name"].dropna().astype(str).str.strip()
folders = folders[folders != ""].drop_duplicates()

created, failed = [], []

for folder in folders:
    try:
        s3.put_object(Bucket=bucket, Key=f"{folder}/")
        created.append(folder)
        print(f"Created: {folder}")
    except ClientError as e:
        failed.append((folder, str(e)))
        print(f"❌ Failed: {folder} — {e}")

print(f"\n✅ Done. {len(created)} created, {len(failed)} failed.")