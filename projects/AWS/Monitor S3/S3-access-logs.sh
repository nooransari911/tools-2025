#!/bin/bash

# Variables
DATABASE_NAME="default"
OUTPUT_LOCATION="s3://aws-athena-query-results-677276075874-us-west-2"


QUERY_STRING="
    SELECT
        at_timezone(from_iso8601_timestamp(eventtime), 'Asia/Kolkata') AS \"Time\",
        eventname AS \"Operation\",
        CASE
            WHEN useridentity.arn LIKE '%user/%' THEN CONCAT('user/', regexp_extract(useridentity.arn, 'user/(.*)', 1))
            WHEN useridentity.arn LIKE '%role/%' THEN CONCAT('role/', regexp_extract(useridentity.arn, 'role/(.*)', 1))
            WHEN useridentity.type = 'Root' THEN 'root'
            ELSE 'unknown'
        END AS \"User\",
        regexp_extract(arn_bucket, 'arn:aws:s3:::(.*)', 1) AS \"Bucket Name\",
        CASE
            WHEN json_extract_scalar(REQJSON, '$.prefix') IS NOT NULL
                THEN json_extract_scalar(REQJSON, '$.prefix')
        ELSE 'N/A'
        END AS \"Prefix\"
    FROM
        cloudtrail_logs_aws_cloudtrail_logs_677276075874_s3_ansarimnfedorabackupuswest2,
        LATERAL (
            SELECT
                resources[2].arn AS arn_bucket,
                json_parse(requestparameters) AS REQJSON
        )
    ORDER BY eventtime DESC
    LIMIT 10;"

# Start Query Execution
QUERY_EXECUTION_ID=$(aws athena start-query-execution \
    --query-string "$QUERY_STRING" \
    --result-configuration "OutputLocation=$OUTPUT_LOCATION" \
    --query-execution-context "Database=$DATABASE_NAME" \
    --output text --query 'QueryExecutionId')

echo "Query Execution ID: $QUERY_EXECUTION_ID"

# Check Query Execution Status
STATUS="RUNNING"
while [ "$STATUS" == "RUNNING" ] || [ "$STATUS" == "QUEUED" ]; do
    STATUS=$(aws athena get-query-execution --query-execution-id $QUERY_EXECUTION_ID \
        --output text --query 'QueryExecution.Status.State')
    echo "Query Status: $STATUS"
    sleep 5
done

# Check if the query succeeded
if [ "$STATUS" == "SUCCEEDED" ]; then
    echo "Query succeeded. Fetching results..."

    # Get the results and pretty-print them
    aws athena get-query-results --query-execution-id $QUERY_EXECUTION_ID | \
    jq -r '.ResultSet.Rows[] | [.Data[].VarCharValue] | @tsv' | \
    column -t -s $'\t' | \
    awk 'BEGIN { OFS="\t"; print "-------------------------------------" } { print $0; print "" } END { print "-------------------------------------" }'


    echo "Results fetched and formatted successfully."
else
    echo "Query failed or was cancelled."
    exit 1
fi
