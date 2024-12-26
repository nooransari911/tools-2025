"""Routes:
/          homepage; generate viz for a year/month
/up        upload files to GCS bucket;
/update    process latest statement and update database;
/24-08     for Aug `24;
/year/24   for year `24
/test      to automatic test routes
"""
import time

import openpyxl
from google.cloud import storage
from google.cloud import bigquery
import datetime
import pandas as pd
import plotly.express as px
from flask import Flask, render_template, redirect, url_for, request, Response
import os, json, io, requests
from dotenv import load_dotenv

from SQL_queries import *

load_dotenv()

app = Flask(__name__)

# BigQuery configuration
BQ_PROJECT = os.environ.get('BQ_PROJECT')  # Fetch from environment
BQ_DATASET = os.environ.get('BQ_DATASET')  # Fetch from environment

# Google Cloud Storage configuration
GCS_BUCKET = os.environ.get('GCS_BUCKET')  # Fetch from environment

# Function to process the latest statement from GCS
def process_latest_statement():
    """Cloud Function triggered by a file upload to GCS."""

    # 1. Get the latest .xlsx file from GCS
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET)
    blobs = bucket.list_blobs()
    latest_file = None
    latest_timestamp = datetime.datetime.min
    for blob in blobs:
        if blob.name.endswith('.xlsx'):
            month_str, year_str = blob.name[:-5].split('-')
            month_num = datetime.datetime.strptime(month_str, '%b').month
            timestamp = datetime.datetime(int(year_str), month_num, 1)
            if timestamp > latest_timestamp:
                latest_timestamp = timestamp
                latest_file = blob

    if latest_file is None:
        print("No .xlsx files found in the bucket.")
        return

    # 2. Download the latest file
    latest_file.download_to_filename('statement.xlsx')

    # 3. Process statement data
    workbook = openpyxl.load_workbook('statement.xlsx')
    sheet = workbook.active

    # Identify relevant columns
    date_column = None
    payee_column = None
    withdrawal_column = None
    deposit_column = None
    for i, col in enumerate(sheet[1]):  # Check header row
        if col.value == 'Date':
            date_column = i
        elif col.value == 'Narration':
            payee_column = i
        elif col.value == 'Withdrawal Amt.':
            withdrawal_column = i
        elif col.value == 'Deposit Amt.':
            deposit_column = i

    if any(col is None for col in [date_column, payee_column, withdrawal_column, deposit_column]):
        print("Could not find all required columns: Date, Narration, Withdrawal Amt., Deposit Amt.")
        return

    transactions = []
    for row in sheet.iter_rows(values_only=True):
        # Skip header row
        if row[0] is None:
            continue

        payee = row[payee_column]
        if "UPI-" in payee:
            payee = payee.replace("UPI-", "")
        payee = payee[:20]  # Limit to 20 characters

        transaction = {
            "date": row[date_column],
            "payee": row[payee_column][:20],
            "withdrawal_amt": row[withdrawal_column],
            "deposit_amt": row[deposit_column],
        }
        transactions.append(transaction)

    transactions = transactions[1:]
    transactions_json = json.dumps(transactions, indent=4)
    print(f"{transactions_json}\n\n\n\n")


    # 4. Save data to BigQuery
    client = bigquery.Client(project=BQ_PROJECT)  # Default credentials should be used

    # Create the dataset if it doesn't exist
    dataset_ref = client.dataset(BQ_DATASET)
    client.create_dataset(dataset_ref, exists_ok=True)  # Create if doesn't exist

    # Create the table if it doesn't exist
    table_ref = dataset_ref.table('transactions')

    # Define schema for the table
    schema = [
        bigquery.SchemaField("date", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("payee", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("withdrawal_amt", bigquery.enums.SqlTypeNames.FLOAT),
        bigquery.SchemaField("deposit_amt", bigquery.enums.SqlTypeNames.FLOAT),
    ]

    table = bigquery.Table(table_ref, schema=schema)
    # Create the table using the defined schema
    #table = client.create_table(table, exists_ok=True)  # Use client.create_table() directly


    errors = client.insert_rows_json (table_ref, transactions)
    if errors == []:
        print("Data loaded successfully")
    else:
        print(f"Errors: {errors}")


"""query viz = f
            SELECT payee, SUM(withdrawal_amt) AS total_spent, SUM(deposit_amt) AS total_deposited
            FROM `{BQ_PROJECT}.{BQ_DATASET}.transactions`
            WHERE CAST(SUBSTR(date, 4, 2) AS INT64) = CAST(SUBSTR("{month}", 4, 2) AS INT64)
                AND CAST(SUBSTR(date, 7, 2) AS INT64) = CAST(SUBSTR("{month}", 1, 2) AS INT64)
            GROUP BY payee
        """


def viz_data (query):
    """# Query BigQuery for the requested month's data
    client = bigquery.Client(project=BQ_PROJECT)

    query_job = client.query_and_wait(query)
    results = query_job

    data = [dict(row) for row in results]
    df = pd.DataFrame(data)
    # print (f"\n\nDf is:\n{df.to_string()}")"""


    client = bigquery.Client(project=BQ_PROJECT)

    query_job = client.query_and_wait(query)
    results = query_job


    # Check if the query returned any rows
    if results.total_rows == 0:
        requested_month = query.split("WHERE")[1].strip()  # Extract the month from the query
        error_message = f"No data found for {requested_month}"
        return render_template('index.html', error=error_message)


    else:
        data = [dict(row) for row in results]
        df = pd.DataFrame(data)

        df_spending = df.sort_values(by='total_spent', ascending=False)
        df_deposits = df.sort_values(by='total_deposited', ascending=False)
        df_spending = df_spending.dropna(subset=['total_spent'])  # Drop rows with null in total_spent
        df_deposits = df_deposits.dropna(subset=['total_deposited'])  # Drop rows with null in total_deposited

        FIG_WIDTH = 1000
        FIG_HEIGHT = 700
        """# Create pie chart for spending
        fig_pie_spending = px.pie(
            df_spending,
            names='payee',
            values='total_spent',
            title=f"Spending Breakdown"
        )
        fig_pie_spending.update_layout(width=FIG_WIDTH, height=FIG_HEIGHT)
        # Create bar chart (you can use either df_spending or df_deposits)
        fig_bar = px.bar(df_spending, x="payee", y="total_spent", title=f"Spending by Payee")
        fig_bar.update_layout(width=FIG_WIDTH, height=FIG_HEIGHT)
        fig_bar.update_xaxes(tickangle=45)

        # Convert charts to HTML
        pie_chart_spending = fig_pie_spending.to_html(full_html=False)
        bar_chart = fig_bar.to_html(full_html=False)

        #Generate spending and deposits table
        df_spending = df_spending.drop('total_deposited', axis=1)
        df_deposits = df_deposits.drop('total_spent', axis=1)
        df_sp_html = df_spending.to_html(classes='table table-striped', index=False)
        df_de_html = df_deposits.to_html(classes='table table-striped', index=False)"""

        # Create pie chart for spending
        pie_chart_spending = px.pie(
            df_spending,
            names='payee',
            values='total_spent',
            title=f"Spending Breakdown",
            color_discrete_sequence=px.colors.qualitative.Prism  # Use a colorblind-friendly palette
        )
        pie_chart_spending.update_layout(
            width=FIG_WIDTH,
            height=FIG_HEIGHT,
            template='plotly_dark',  # Use dark mode template
            font=dict(family='Source Code Pro', size=14, color='#f0f0f0'),  # Update font
            title=dict(font=dict(size=18, color='#00ffff'))  # Increase title font size
        )

        # Create bar chart
        bar_chart = px.bar(
            df_spending,
            x="payee",
            y="total_spent",
            title=f"Spending by Payee",
            color_discrete_sequence=px.colors.qualitative.Prism  # Use a colorblind-friendly palette
        )
        bar_chart.update_layout(
            width=FIG_WIDTH,
            height=FIG_HEIGHT,
            template='plotly_dark',  # Use dark mode template
            font=dict(family='Source Code Pro', size=14, color='#f0f0f0'),  # Update font
            title=dict(font=dict(size=18, color='#00ffff')),  # Increase title font size
            xaxis_tickangle=45
        )

        # Generate spending and deposits table
        df_spending = df_spending.drop('total_deposited', axis=1)
        df_deposits = df_deposits.drop('total_spent', axis=1)

        # Convert charts to HTML
        pie_chart_spending = pie_chart_spending.to_html(full_html=False)
        bar_chart = bar_chart.to_html(full_html=False)

        # Create the HTML for the tables with inline styling for text color
        df_sp_html = df_spending.to_html(
            classes='table table-striped',
            index=False,
        ).replace(
            '<style type="text/css">',
            '<style type="text/css"> .table th, .table td { color: #eee !important; } '  # More specific selectors
        )
        df_de_html = df_deposits.to_html(
            classes='table table-striped',
            index=False,
        ).replace(
            '<style type="text/css">',
            '<style type="text/css"> .table th, .table td { color: #eee !important; } '  # More specific selectors
        )

        return render_template('index.html',
                               pie_chart_spending=pie_chart_spending, bar_chart=bar_chart,
                               df_sp_html=df_sp_html, df_de_html=df_de_html)

















# Function to generate visualizations for the current month
@app.route('/latest')
def visualize_current_month():
    # Get the current month
    current_month = datetime.datetime.now().strftime('%Y-%m')
    current_month = current_month [2:]
    #print(current_month)
    query = f"""
                SELECT payee, SUM(withdrawal_amt) AS total_spent, SUM(deposit_amt) AS total_deposited
                FROM `{BQ_PROJECT}.{BQ_DATASET}.transactions`
                WHERE CAST(SUBSTR(date, 4, 2) AS INT64) = CAST(SUBSTR("{current_month}", 4, 2) AS INT64)
                    AND CAST(SUBSTR(date, 7, 2) AS INT64) = CAST(SUBSTR("{current_month}", 1, 2) AS INT64)
                GROUP BY payee
            """
    return viz_data(return_sql(prequested_month=current_month)[2])


# Function to generate visualizations for a specific month
@app.route('/<year>-<month>')
def visualize_specific_month(year, month):
    requested_month = f"{year}-{month}"
    #print(requested_month)
    #print(return_sql(prequested_month=requested_month)[2])
    return viz_data(return_sql(prequested_month=requested_month)[2])




@app.route('/year/<year>')
def visualize_year(year):
    return viz_data(return_sql(pyear=year)[1])




@app.route('/', methods=["GET"])
def select_data_get():
    client = bigquery.Client(project=BQ_PROJECT)
    oldest_year = client.query_and_wait(SQL_LIST [0])
    oldest_year = "".join (["20", str (next(oldest_year)["oldest_year"])])


    current_year = datetime.datetime.now().year
    years = list(range(int (oldest_year), current_year + 1)) # Generate a list of years
    months = list(range(1, 13))
    return render_template('select.html', years=years, months=months)


@app.route ("/", methods=["POST"])
def select_year_post ():
    selected_option = request.form.get('option')
    selected_year = int(request.form.get('year'))
    #print(selected_year)
    if selected_option == 'month':
        selected_month = int(request.form.get('month'))
        return redirect(url_for("visualize_specific_month",
                                year=str(selected_year)[-2:], month=f"{selected_month:02}"))

    elif selected_option == 'year':
        return redirect(url_for("visualize_year",
                                year=str(selected_year)[-2:]))
    else:
        return "Invalid selection."



@app.route ("/update")
def process ():
    process_latest_statement()
    return ("<h1>Done</h1>")



@app.route('/up', methods=['GET'])
def upload_form():
    """Renders the file upload form."""
    return render_template('upload.html')

@app.route('/up', methods=['POST'])
def upload_file():
    """Handles file upload and redirection."""
    storage_client = storage.Client()
    bucket = storage_client.bucket (GCS_BUCKET)


    # Get the uploaded file and desired filename
    file = request.files['file']
    new_filename = request.form['new_filename']

    if file and new_filename:
        try:
            # Upload the file to GCS with the new name
            blob = bucket.blob(new_filename)
            # Overwrite the existing file
            blob.upload_from_string(file.read(), content_type=file.content_type)
            return f'<h1>File {file.filename} uploaded to {GCS_BUCKET} as {new_filename}</h1>'

        except Exception as e:
            return f'Error uploading file: {str(e)}', 500
    else:
        return 'No file or filename provided', 400



@app.route ("/GCS-text")
def in_memory_download_text ():
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET)
    blobs = bucket.list_blobs()

    blobs = bucket.list_blobs()
    latest_file = max(blobs, key=lambda blob: blob.updated)

    blob_stream = io.BytesIO()
    latest_file.download_to_file(blob_stream)
    blob_stream.seek(0)

    text_content = blob_stream.read().decode('utf-8')
    #print(text_content)

    return (f"<h1>Content is:</h1>\n\n{text_content}")



@app.route ("/GCS-image")
def in_memory_download_image ():
    #Takes ~4.5 seconds to 5 second to show 1080p 450 kB proxdr image


    time_start = time.time_ns()
    IMAGE_BUCKET = "gcloud_image_intelligence"
    storage_client = storage.Client()
    bucket = storage_client.bucket(IMAGE_BUCKET)


    #select latest file:
    #blobs = bucket.list_blobs()
    #latest_file = max(blobs, key=lambda blob: blob.updated)
    blob = bucket.blob ("proxdr.jpg")
    blob_stream = io.BytesIO()

    content_type = blob.content_type
    blob.download_to_file(blob_stream)
    blob_stream.seek(0)
    time_end = time.time_ns()
    time_elapsed = (time_end - time_start) / (10**9)
    print (f"\nTime elapsed: {time_elapsed} s")
    return Response (blob_stream.getvalue(), mimetype=blob.content_type, headers={'Content-Disposition': 'inline'})




@app.route ("/GCS-url")
def gcs_image_url_direct ():
    #Takes ~0.03 to ~0.08 seconds for 450kB proxdr image
    time_start = time.time_ns()
    IMAGE_BUCKET = "gcloud_image_intelligence"
    storage_client = storage.Client()
    bucket = storage_client.bucket(IMAGE_BUCKET)
    blob = bucket.blob("proxdr.jpg")

    signed_url = blob.generate_signed_url(version="v4",
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta (minutes=15),
        # Allow GET requests using this URL.
        method="GET",
    )

    time_end = time.time_ns()
    time_elapsed = (time_end - time_start) / (10 ** 9)
    #print(f"\nTime elapsed: {time_elapsed} s")
    return redirect(signed_url)




@app.route('/test', methods=['POST'])
def test_route_post_request():
    target_route = request.form.get('target_route')
    app_url = 'http://127.0.0.1:5000'  # Base URL of your Flask app

    if request.form.get('no_of_hits') != '':
        num_requests = int(request.form.get('no_of_hits'))
    else:
        num_requests = 2

    for i in range(num_requests):
        start_time = time.time_ns()  # Start timing
        full_url = app_url + "/" + target_route
        try:
            response = requests.get(full_url)
            end_time = time.time_ns()  # End timing
            request_time = (end_time - start_time) / (10**9)
            print(f"Request {i + 1}: Status code - {response.status_code}, Time: {request_time:.4f} seconds")  # Print results
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    return "<h1>Requests sent!</h1>"  # Send a simple message back to the browser

@app.route('/test', methods=['GET'])
def test_route_get_request():
    return render_template('test.html')









if __name__ == '__main__':
    #Run the Flask app for visualizations
    app.run(debug=True)
