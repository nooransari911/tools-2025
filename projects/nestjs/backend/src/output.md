<h1>API Response Report</h1>
<h1>URL: http://localhost:3000/jet/post_user_profile?id=45&phone=fg&name=my&dept=sales</h1>
<h2>Status Code: 400</h2>
<pre>{
    "standard_exc_body": {
        "status": 400,
        "status_string": "Invalidation Failed",
        "timestamp": "2025-01-19T18:22:53.723Z",
        "message": [
            "phone must be an integer number"
        ],
        "requested_resource": "/jet/post_user_profile?id=45&phone=fg&name=my&dept=sales"
    }
}</pre>
<h1>URL: http://localhost:3000/jet/post_user_profile?id=45&phone=fg&name=my</h1>
<h2>Status Code: 400</h2>
<pre>{
    "standard_exc_body": {
        "status": 400,
        "status_string": "Invalidation Failed",
        "timestamp": "2025-01-19T18:22:53.728Z",
        "message": [
            "phone must be an integer number",
            "dept should not be empty",
            "dept must be a string"
        ],
        "requested_resource": "/jet/post_user_profile?id=45&phone=fg&name=my"
    }
}</pre>
<h1>URL: http://localhost:3000/jet/post_user_profile?id=45&phone=85&name=my&dept=sales</h1>
<h2>Status Code: 200</h2>
<pre>{
    "id": "45",
    "phone": "85",
    "name": "my",
    "dept": "sales"
}</pre>
<h1>URL: http://localhost:3000/jet/nz</h1>
<h2>Status Code: 418</h2>
<pre>{
    "standard_exc_body": {
        "status": 418,
        "status_string": "I'm a Teapot;",
        "timestamp": "2025-01-19T18:22:53.745Z",
        "message": "This is my message for a 418/I'm a teapot status code",
        "requested_resource": "/jet/nz"
    }
}</pre>
<h1>URL: http://localhost:3000/jet/viet</h1>
<h2>Status Code: 403</h2>
<pre>{
    "standard_exc_body": {
        "status": 403,
        "status_string": "Forbidden Request;",
        "timestamp": "2025-01-19T18:22:53.754Z",
        "message": "This is my message for a 403/forbidden status code",
        "requested_resource": "/jet/viet"
    }
}</pre>
<h1>URL: http://localhost:3000/jet/france</h1>
<h2>Status Code: 200</h2>
<pre>[
    {
        "country": "france",
        "block": "NATO",
        "name": "rafale",
        "manufacturer": "dassault",
        "gen": "4.5",
        "role": "multirole",
        "mtow": "24"
    }
]</pre>
<h1>URL: http://localhost:3000/jet/china</h1>
<h2>Status Code: 200</h2>
<pre>[
    {
        "country": "china",
        "block": "SCO",
        "name": "J20",
        "manufacturer": "chengdu",
        "gen": "5",
        "role": "air superiority",
        "mtow": "35"
    },
    {
        "country": "china",
        "block": "SCO",
        "name": "J15",
        "manufacturer": "shenyang",
        "gen": "4.5",
        "role": "air superiority",
        "mtow": "30"
    }
]</pre>
