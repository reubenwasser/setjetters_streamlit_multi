# SetJetter Streamlit Application

## How to Run

1. Clone the repository:
```
$ git clone git@github.com:upraneelnihar/streamlit-multiapps
$ cd streamlit-multiapps
```

2. Install dependencies:
```
$ pip install -r requirements.txt
```

3. Save databse credentials:
You should put your database credentials and OpenCage API for geocoder api in the Streamlit Secrets in: `.streamlit/secrets.toml` as follows:
```
# .streamlit/secrets.toml

[mysql]
host = "DB HOST"
database = "DB"
user = "USER"
password = "PW"

[opencage]
api_key = "TOKEN HERE"
```


4. Start the application:
```
streamlit run app.py
```
