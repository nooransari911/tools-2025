from dotenv import load_dotenv
import os, re


load_dotenv()

# BigQuery configuration
BQ_PROJECT = os.environ.get('BQ_PROJECT')  # Fetch from environment
BQ_DATASET = os.environ.get('BQ_DATASET')  # Fetch from environment


year = "aa"
requested_month = "aa"


SQL_LIST = [
    f"""
        SELECT DISTINCT CAST(SUBSTR(date, -2) AS INT64) AS oldest_year
        FROM `{BQ_PROJECT}.{BQ_DATASET}.transactions`
        ORDER BY oldest_year ASC
        LIMIT 1;
    """,

    """
        SELECT payee, SUM(withdrawal_amt) AS total_spent, SUM(deposit_amt) AS total_deposited
        FROM `{BQ_PROJECT}.{BQ_DATASET}.transactions`
        WHERE CAST(SUBSTR(date, 7, 2) AS INT64) = CAST(SUBSTR('<', 1, 2) AS INT64)
        GROUP BY payee
    """,

    """
        SELECT payee, SUM(withdrawal_amt) AS total_spent, SUM(deposit_amt) AS total_deposited
        FROM `{BQ_PROJECT}.{BQ_DATASET}.transactions`
        WHERE CAST(SUBSTR(date, 4, 2) AS INT64) = CAST(SUBSTR("<", 4, 2) AS INT64)
            AND CAST(SUBSTR(date, 7, 2) AS INT64) = CAST(SUBSTR("<", 1, 2) AS INT64)
        GROUP BY payee
    """
    ]




def return_sql (pyear=None, prequested_month=None):
    sq = SQL_LIST

    if pyear:
        sq [1] = re.sub (r'<', str (pyear), sq [1])
        sq [1] = re.sub (r"{BQ_PROJECT}.{BQ_DATASET}.transactions",
                f"{BQ_PROJECT}.{BQ_DATASET}.transactions",
                str (sq [1]))
        print (sq [1])


    elif prequested_month:

        if re.search (r"<", sq[2]):
            sq[2] = re.sub(r"({BQ_PROJECT}.{BQ_DATASET}.transactions)",
                           (f"{BQ_PROJECT}.{BQ_DATASET}.transactions"),
                           sq[2])

            sq [2] = re.sub (r'<', str (prequested_month), sq [2])


        else:
            replacements = [f"CAST(SUBSTR(\"{prequested_month}\", 4, 2) AS INT64)",
                            f"CAST(SUBSTR(\"{prequested_month}\", 1, 2) AS INT64)"
                            ]

            sq [2] = re.sub (r'CAST\(SUBSTR\("(\d{2}-\d{2})", \d{1}, \d{1}\) AS INT64\)',
                   lambda m, reps=replacements: reps.pop(0),
                   sq [2], 2)

            sq[2] = re.sub(r"({BQ_PROJECT}.{BQ_DATASET}.transactions)",
                           (f"{BQ_PROJECT}.{BQ_DATASET}.transactions"),
                           sq[2])

        print (sq [2])


    return sq