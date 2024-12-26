#!/bin/bash

echo "[$(date +'%Y-%m-%d %H:%M:%S')] - Script started"


# Variables
DATABASE_NAME="default"
OUTPUT_LOCATION="s3://aws-athena-query-results-677276075874-us-west-2"


QUERY_STRING="
    SELECT
        eventname AS \"Operation\",
        COUNT(*) AS \"Operation Count\"
    FROM
        cloudtrail_logs_aws_cloudtrail_logs_677276075874_s3_ansarimnfedorabackupuswest2
    WHERE
        from_iso8601_timestamp(eventtime) >= date_trunc('month', current_timestamp)
    GROUP BY
        eventname
    ORDER BY
        \"Operation Count\" DESC;"



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
    aws athena get-query-results --query-execution-id $QUERY_EXECUTION_ID | \
    jq -r '.ResultSet.Rows[] | [.Data[].VarCharValue] | @tsv' | \
    column -t -s $'\t' | \
    awk 'BEGIN { OFS="\t"; print "-------------------------------------" } { print $0; print "" } END { print "-------------------------------------" }'
    echo ""
    echo "Results fetched successfully."


else
    echo "Query failed or was cancelled."
    exit 1
fi
