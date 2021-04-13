import os
from flask import Flask
from flask import jsonify
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# Astra Cluster ID
astraDbId = os.environ.get("ASTRA_DB_ID", "xxx")
# Astra DB region
astraRegion = os.environ.get("ASTRA_DB_REGION", "xxx")
# Astra DB keyspace
astraKeyspace = os.environ.get("ASTRA_DB_KEYSPACE", "xxx")
# Astra collection (think of it like a table) to create
astraTable = os.environ.get("ASTRA_DB_TABLE", "xxx")
# App token
astraAppToken = os.environ.get("ASTRA_DB_APPLICATION_TOKEN", "xxx")


app = Flask(__name__)


@app.route("/slots/<parking_lot>/<floor_num>", methods=["GET"])
def lookup_available_slots(parking_lot, floor_num):
    http_request = "https://" + astraDbId + "-" + astraRegion + ".apps.astra.datastax.com/api/rest/v2/keyspaces/" + \
        astraKeyspace + "/" + astraTable + "/" + parking_lot + "/" + \
        floor_num + "?page-size=1&raw=true&fields=num_available"
    headers = {"x-cassandra-token": astraAppToken}
    response_get_availability = requests.get(http_request, headers=headers)

    if response_get_availability.status_code == 200:
        response_availability = json.loads(response_get_availability.text)
        return 'Total slots available for FloorNum: {} at Parking Lot {} are {}'.format(floor_num, parking_lot, response_availability[0]['num_available']), response_get_availability.status_code
    else:
        return "An error occurred", response_get_availability.status_code


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(
        os.environ.get("PORT", "8080")))
