```
{
    "widgets": [
        {
            "height": 13,
            "width": 12,
            "y": 0,
            "x": 0,
            "type": "metric",
            "properties": {
                "metrics": [
                    [ "AWS/S3", "BucketSizeBytes", "BucketName", "ansarimn-fedora-backup-us-west-2", "StorageType", "GlacierStorage", { "region": "us-west-2", "label": "Total Glacier Storage" } ],
                    [ "...", "StandardStorage", { "region": "us-west-2", "label": "Total Standard Storage" } ],
                    [ "...", "StandardIAStorage", { "region": "us-west-2", "label": "Total Standard IA Storage" } ],
                    [ ".", "NumberOfObjects", ".", ".", ".", "AllStorageTypes", { "region": "us-west-2", "label": "Total Number Of Objects" } ]
                ],
                "sparkline": true,
                "view": "singleValue",
                "stacked": true,
                "region": "us-west-2",
                "start": "-PT336H",
                "title": "storage overview",
                "period": 86400,
                "end": "P0D",
                "stat": "Average"
            }
        },
        {
            "height": 7,
            "width": 12,
            "y": 13,
            "x": 0,
            "type": "metric",
            "properties": {
                "metrics": [
                    [ { "expression": "SUM(METRICS())", "label": "Total GET LIST HEAD", "id": "e1", "stat": "Sum", "period": 2592000 } ],
                    [ "AWS/S3", "HeadRequests", "BucketName", "ansarimn-fedora-backup-us-west-2", "FilterId", "full-bucket-requests", { "id": "m1" } ],
                    [ ".", "ListRequests", ".", ".", ".", ".", { "id": "m2" } ]
                ],
                "sparkline": true,
                "view": "singleValue",
                "region": "us-west-2",
                "stat": "Sum",
                "period": 2592000,
                "title": "Total GET LIST HEAD",
                "start": "-PT672H",
                "end": "P0D"
            }
        },
        {
            "height": 13,
            "width": 12,
            "y": 0,
            "x": 12,
            "type": "metric",
            "properties": {
                "metrics": [
                    [ { "expression": "METRICS()/1000000000", "label": "Bytes GB", "id": "e1" } ],
                    [ "AWS/S3", "BytesDownloaded", "BucketName", "ansarimn-fedora-backup-us-west-2", "FilterId", "full-bucket-requests", { "region": "us-west-2", "id": "m1", "visible": false, "label": "Downloaded" } ],
                    [ ".", "BytesUploaded", ".", ".", ".", ".", { "region": "us-west-2", "id": "m2", "visible": false, "label": "Uploaded" } ]
                ],
                "sparkline": true,
                "view": "gauge",
                "title": "Total REQ, Bytes upload/download",
                "region": "us-west-2",
                "start": "-PT1344H",
                "end": "P0D",
                "period": 2592000,
                "stat": "Sum",
                "yAxis": {
                    "left": {
                        "min": 0,
                        "max": 0.8
                    }
                }
            }
        },
        {
            "height": 7,
            "width": 12,
            "y": 13,
            "x": 12,
            "type": "metric",
            "properties": {
                "metrics": [
                    [ "AWS/S3", "PostRequests", "BucketName", "ansarimn-fedora-backup-us-west-2", "FilterId", "full-bucket-requests", { "region": "us-west-2", "label": "Post Requests" } ],
                    [ ".", "PutRequests", ".", ".", ".", ".", { "region": "us-west-2", "label": "Put Requests" } ]
                ],
                "sparkline": true,
                "view": "singleValue",
                "region": "us-west-2",
                "start": "-PT672H",
                "end": "P0D",
                "title": "Total PUT POST",
                "period": 2592000,
                "stat": "Sum"
            }
        }
    ]
}

```
