from google.cloud import storage
import pandas as pd
import io
import datetime
import pytz
import streamlit as st

def download_csv_from_bucket(csv_file, bucket_name):
    """Downloads a CSV file from a Google Cloud Storage bucket and loads it into a DataFrame."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(csv_file)
    content = blob.download_as_string()
    df = pd.read_csv(io.BytesIO(content))
    return df

def add_data_to_csv(df, data):
    """Adds new data to a DataFrame and saves it to a CSV file."""
    df = pd.concat([df, pd.DataFrame(data, index=[0])], ignore_index=True)
    return df

def upload_csv_to_bucket(df, csv_file, bucket_name):
    """Saves a DataFrame to a CSV file and uploads it to a Google Cloud Storage bucket."""
    with io.StringIO() as csv_buffer:
        df.to_csv(csv_buffer, index=False)
        new_content = csv_buffer.getvalue().encode()

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(csv_file)
    blob.upload_from_string(new_content, content_type='text/csv')

def show_csv_in_streamlit(df):
    """Displays a DataFrame in Streamlit."""
    st.write(df)

if __name__ == "__main__":
    # Set the name of the CSV file in the bucket
    csv_file = 'fip_feedback.csv'
    # Set the name of the bucket in Google Cloud Storage
    bucket_name = 'taxo-pdfs'

    # Download the CSV file and load it into a DataFrame
    df = download_csv_from_bucket(csv_file, bucket_name)
    
    st.sidebar.write("Add Data:")
    user_name = st.sidebar.text_input('User Name:', key='user_name'),
    user_question = st.sidebar.text_input('Question:', key='question'),
    answer = st.sidebar.text_input('Answer:', key='answer'),
    feedback_text = st.sidebar.text_input('Feedback:', key='feedback_text'),
    source_text = st.sidebar.text_input('Source:', key='source_text'),
    improvement_suggestions = st.sidebar.text_input('Improvement Suggestions:', key='improvement_suggestions'), 
    missing_details = st.sidebar.text_input('Missing Details:', key='missing_details'),
    source_details = st.sidebar.text_input('Source Details:', key='source_details'),
    useful = st.sidebar.checkbox('Useful:', key='useful')

    if st.sidebar.button("Add Data"):
        mexico_tz = pytz.timezone('America/Mexico_City')
        current_datetime = datetime.datetime.now(mexico_tz)
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        new_data = {
            "user_name": user_name,
            "date": formatted_datetime,
            "question": user_question,
            "answer": answer,
            "feedback": feedback_text,
            "source": source_text,
            "improvement_suggestions": improvement_suggestions,
            "missing_details": missing_details,
            "source_details": source_details,
            "useful": useful    
        }

        # Add the new data to the DataFrame
        df = add_data_to_csv(df, new_data)

        # Upload the updated DataFrame to the CSV file in the bucket
        upload_csv_to_bucket(df, csv_file, bucket_name)

    df_invertido = df.iloc[::-1].reset_index(drop=True)

    # Show the updated DataFrame in Streamlit
    st.write("Updated CSV:")
    
    # Display rows with column name in bold and its value alongside, separating each value with a divider
    for index, row in df_invertido.iterrows():
        st.write("---")
        for column in df.columns:  # This loop now includes the "date" column
            st.write(f"**{column}:** {row[column]}")