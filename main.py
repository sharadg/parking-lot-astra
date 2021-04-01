import os

from flask import Flask
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from flask import jsonify

app = Flask(__name__)

cloud_config = {
    'secure_connect_bundle': '/tmp/secure-connect-petclinic.zip'
}
auth_provider = PlainTextAuthProvider('gYkAszLdRdNZfPqFaLTUmUem', 'tCNepGtye_Whk9+jcGeFCo,ZyIiRwk5_1E8AZHwidFpk+KWrQnoGkS752UJ15nvTy5Z,X9jZ7,Ayg5ayEjj1Q2p.qWkLFfbCTcr.BalxmfpqlYDCo5Yxcv4l+2ZcWakZ')
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()
session.set_keyspace("petclinickp")


@app.route("/slots/<parking_lot>/<floor_num>", methods=["GET"])
def lookup_available_slots(parking_lot, floor_num):
    global session
    query = 'SELECT parking_lot, floor_num, sensor_slot, max(recorded_time), occupied FROM parking_lot_occupancy WHERE parking_lot=\'{parking_lot}\' AND floor_num = {floor_num} GROUP BY parking_lot, floor_num, sensor_slot ALLOW FILTERING ;'.format(
        parking_lot=parking_lot, floor_num=floor_num)
    rows = session.execute(query).all()

    if rows:
        slots = 0
        for row in rows:
            if not bool(row.occupied):
                slots += 1
            # print('Parking Lot: {pl}, FloorNum: {fn}, SensorSlot: {ss}, Occupied: {oc}'.format(pl=row.parking_lot, fn=row.floor_num, ss=row.sensor_slot, oc=row.occupied))
        return 'Total slots available for FloorNum: {} at Parking Lot {} are {}'.format(floor_num, parking_lot, slots), 200
    else:
        return "An error occurred", 500


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
