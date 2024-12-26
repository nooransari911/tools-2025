{
    "widgets": [
        {
            "height": 8,
            "width": 9,
            "y": 0,
            "x": 0,
            "type": "metric",
            "properties": {
                "metrics": [
                    [ "AWS/S3", "BucketSizeBytes", "BucketName", "ansarimn-public-s3", "StorageType", "StandardStorage", { "region": "us-west-2", "label": "Total Standard Storage Bytes" } ],
                    [ ".", "NumberOfObjects", ".", ".", ".", "AllStorageTypes", { "region": "us-west-2", "label": "Total Number Of Objects" } ]
                ],
                "sparkline": true,
                "view": "singleValue",
                "region": "us-west-2",
                "start": "-PT672H",
                "end": "P0D",
                "period": 86400,
                "stat": "Sum"
            }
        },
        {
            "height": 7,
            "width": 15,
            "y": 8,
            "x": 9,
            "type": "metric",
            "properties": {
                "metrics": [
                    [ { "expression": "SUM(METRICS())", "label": "Total GET LIST HEAD", "id": "e1" } ],
                    [ "AWS/S3", "GetRequests", "BucketName", "ansarimn-public-s3", "FilterId", "full-bucket", { "id": "m1" } ],
                    [ ".", "ListRequests", ".", ".", ".", ".", { "id": "m2" } ],
                    [ ".", "HeadRequests", ".", ".", ".", ".", { "id": "m3" } ]
                ],
                "sparkline": true,
                "view": "singleValue",
                "region": "us-west-2",
                "stat": "Sum",
                "period": 2592000,
                "start": "-PT672H",
                "end": "P0D",
                "title": "Total GET LIST HEAD"
            }
        },
        {
            "height": 7,
            "width": 9,
            "y": 8,
            "x": 0,
            "type": "metric",
            "properties": {
                "metrics": [
                    [ { "expression": "SUM(METRICS())", "label": "Total PUT POST", "id": "e1" } ],
                    [ "AWS/S3", "PutRequests", "BucketName", "ansarimn-public-s3", "FilterId", "full-bucket", { "id": "m1" } ],
                    [ ".", "DeleteRequests", ".", ".", ".", ".", { "id": "m2" } ]
                ],
                "sparkline": true,
                "view": "singleValue",
                "region": "us-west-2",
                "stat": "Sum",
                "period": 2592000,
                "start": "-PT672H",
                "end": "P0D",
                "title": "Total PUT POST"
            }
        },
        {
            "height": 8,
            "width": 15,
            "y": 0,
            "x": 9,
            "type": "metric",
            "properties": {
                "metrics": [
                    [ { "expression": "METRICS()/1000000", "label": "Bytes MB", "id": "e1" } ],
                    [ "AWS/S3", "BytesDownloaded", "BucketName", "ansarimn-public-s3", "FilterId", "full-bucket", { "region": "us-west-2", "label": "Downloaded", "id": "m2", "visible": false } ],
                    [ ".", "BytesUploaded", ".", ".", ".", ".", { "region": "us-west-2", "label": "Uploaded", "id": "m3", "visible": false } ]
                ],
                "sparkline": true,
                "view": "gauge",
                "region": "us-west-2",
                "stat": "Sum",
                "period": 2592000,
                "start": "-PT672H",
                "end": "P0D",
                "title": "Total REQ, Bytes upload/download",
                "yAxis": {
                    "left": {
                        "min": 0,
                        "max": 2
                    }
                }
            }
        }
    ]
}
