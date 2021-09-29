# SGP Postal Code Crawler

Retrieve and store postal code to address mapping from OneMap.
The data will be collected in a hosted [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
For users who want to get a complete download of the data, please refer to [the main repo](https://github.com/OpenSingaporePostalCode/OpenSingaporePostalCode).

## Run

    python3 -m venv venv
    . venv/bin/activate.fish
    pip install -r requirements.txt
    # please populate the env with MONGODB_USER, MONGODB_PASSWORD, MONGODB_HOST, MONGODB_NAME to the data store
    python run.py

## Data License and TOS

The use of the data is governed by [OneMap's Open Data License and API Terms of Service](https://www.onemap.gov.sg/docs/#open-data-license-and-api-terms-of-service).
