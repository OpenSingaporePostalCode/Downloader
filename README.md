# SGP Postal Code Database

Collecting postal code to address mapping from OneMap

## Run

    python3 -m venv venv
    . venv/bin/activate.fish
    pip install -r requirements.txt
    # please populate the env with MONGODB_USER, MONGODB_PASSWORD, MONGODB_HOST, MONGODB_NAME to the data store
    python run.py

## Data License and TOS

The use of the data is governed by [OneMap's Open Data License and API Terms of Service](https://www.onemap.gov.sg/docs/#open-data-license-and-api-terms-of-service).
