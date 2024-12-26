import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from flask import Flask, render_template, request

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import json
from flask import Flask, render_template, request
import plotly




app = Flask(__name__)

df = None

@app.route("/", methods=["GET", "POST"])
def index():
    global df
    graph_url = None
    table_html = None

    if request.method == "POST":
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"

        try:
            df = pd.read_csv(file)

            # Data cleaning (adapt as needed)
            '''df['size'] = pd.to_numeric(df['size'], errors='coerce')
            df['last_modified_date'] = pd.to_datetime(df['last_modified_date'], errors='coerce')
            file_path = '/home/studio-lab-user/sagemaker-studiolab-notebooks/AWS/csv/2024-09-28.csv'  # Replace with your file path if needed'''


            df['size'] = df['size'].fillna(0)
            for col in ['is_latest', 'is_delete_marker']:
                df[col] = df[col].astype(str).str.upper().replace({'NAN': 'FALSE'})




            # Aggregation
            grouped_df = df.groupby('storage_class').agg(
                total_size=('size', 'sum'),
                object_count=('key', 'count'),
                is_latest_count=('is_latest', lambda x: (x == 'TRUE').sum()),
                is_not_latest_count=('is_latest', lambda x: (x == 'FALSE').sum()),
                is_not_delete_count=('is_delete_marker', lambda x: (x == 'FALSE').sum())
            ).reset_index()
            grouped_df['total_size'] = grouped_df['total_size'] / 1000000000
            print (grouped_df)
            table_html = grouped_df.to_html(classes='table table-striped table-dark', index=False)




            # --- Create Plotly graph JSON ---
            fig = go.Figure()


            colors = ['#E64A19', '#512DA8', '#00796B', '#C2185B', '#F57C00'] # Material Design colors

            for metric, color in zip(['total_size', 'object_count', 'is_latest_count', 'is_not_latest_count', 'is_not_delete_count'], colors):
                yaxis = 'y1' if metric == 'total_size' else 'y2'
                fig.add_trace(go.Scatter(
                    x=grouped_df['storage_class'],
                    y=grouped_df[metric],
                    mode='lines+markers',
                    name=metric.replace("_", " ").title(),
                    yaxis=yaxis,
                    marker=dict(color=color, size=16),
                    line=dict(width=3)  # Thicker lines
                ))

            fig.update_layout(
                yaxis=dict(title="Size (GB)", titlefont=dict(color="white"), showgrid=False),
                yaxis2=dict(title="Counts", overlaying='y', side='right', titlefont=dict(color="white"), showgrid=False),
                xaxis_title="Storage Class",
                template='plotly_dark',  # Use dark mode template
                plot_bgcolor='#1E1E1E',  # Dark background color
                paper_bgcolor='#1E1E1E',  # Dark paper color
                font=dict(color='white'),    # Set font color to white
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),  # Horizontal legend at top
                margin=dict(l=70, r=70, t=50, b=50) # larger margins for better spacing
            )


            graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


        except Exception as e:
            return f"Error processing file: {str(e)}"

        return render_template('index.html', table=table_html, graph_json=graph_json)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
