import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError
import time

s3 = boto3.client('s3')


bucket_name = 'project-storage00'


st.title('S3 Cloud Storage')


st.sidebar.header('Upload File')
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["jpg", "png", "txt", "pdf"])

if uploaded_file is not None:
    try:

        object_key = uploaded_file.name
        s3.upload_fileobj(uploaded_file, bucket_name, object_key)
        suc = st.sidebar.success(f'File uploaded to S3: {object_key}')
        time.sleep(2)
        suc.empty()      
     
        uploaded_file = None
  
    except NoCredentialsError:
        st.error("AWS credentials not available. Configure your credentials.")

a, b = st.columns(2)
a.subheader('S3 Bucket Contents')
if b.button("Refresh"):
    st.rerun()
st.text('-----------------------------------------------------------------------------------')


objects = s3.list_objects_v2(Bucket=bucket_name)

for obj in objects.get('Contents', []):
    col1, col2, col3 = st.columns([1, 1, 1])

    
    col1.write(obj['Key'])

    download_button = col2.button(f'Download {obj["Key"]}')
    if download_button:

        download_link = f'<a href="https://{bucket_name}.s3.amazonaws.com/{obj["Key"]}" download="{obj["Key"]}">Download {obj["Key"]}</a>'
        st.markdown(download_link, unsafe_allow_html=True)


    delete_button = col3.button(f'Delete {obj["Key"]}')
    if delete_button:
        s3.delete_object(Bucket=bucket_name, Key=obj["Key"])
        st.success(f'File deleted: {obj["Key"]}')
