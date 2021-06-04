import os

from flask import Flask
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from dotenv import load_dotenv

load_dotenv()

# Astra DB keyspace
astraKeyspace = os.environ.get("ASTRA_DB_KEYSPACE", "xxx")
# Astra collection (think of it like a table) to create
astraTable = os.environ.get("ASTRA_DB_TABLE", "xxx")
# Client ID
astraClientID = os.environ.get("ASTRA_DB_CLIENT_ID", "xxx")
# Client Secret
astraClientSecret = os.environ.get("ASTRA_DB_CLIENT_SECRET", "xxx")

app = Flask(__name__)

cloud_config = {
    'secure_connect_bundle': './creds.zip'
}
auth_provider = PlainTextAuthProvider(astraClientID, astraClientSecret)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()
session.set_keyspace(astraKeyspace)


@app.route("/slots/<parking_lot>/<floor_num>", methods=["GET"])
def lookup_available_slots(parking_lot, floor_num):
    global session
    query = "SELECT parking_lot, floor_num, num_available FROM " + astraTable + f" WHERE parking_lot='{parking_lot}' AND floor_num = {floor_num} LIMIT 1 ;"
    row = session.execute(query).one()

    if row:
        # print('Parking Lot: {pl}, FloorNum: {fn}, SensorSlot: {ss}, Occupied: {oc}'.format(pl=row.parking_lot, fn=row.floor_num, ss=row.sensor_slot, oc=row.occupied))
        return 'Total slots available for FloorNum: {} at Parking Lot {} are {}'.format(floor_num, parking_lot,
                                                                                        row.num_available), 200
    else:
        return "An error occurred", 500


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
