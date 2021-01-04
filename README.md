## SensorsRUs MVP - Parking Lot Occupancy

This simple codebase allows one to connect to Datastax Astra and pull down specific query results for the number of open slots at a particular floor of a specific Parking Lot.

This github repo is setup to deploy continuously to [Google Cloud Run](https://parking-lot-astra-ynv6tadumq-ue.a.run.app/) and can be called like below:

Before running this sample, in your environment, make sure you have downloaded the secure connect bundle from your instance of Datastax Astra and saved in this folder as `creds.zip`

### Interacting with the REST APIs
Look up Slots using this pattern `http -v https://parking-lot-astra-ynv6tadumq-ue.a.run.app/slots/{parking_lot}/{floor_num}`

```shell
http -v https://parking-lot-astra-ynv6tadumq-ue.a.run.app/slots/nasa_east/1

GET /slots/nasa_east/1 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: parking-lot-astra-ynv6tadumq-ue.a.run.app
User-Agent: HTTPie/2.3.0



HTTP/1.1 200 OK
Alt-Svc: h3-29=":443"; ma=2592000,h3-T051=":443"; ma=2592000,h3-Q050=":443"; ma=2592000,h3-Q046=":443"; ma=2592000,h3-Q043=":443"; ma=2592000,quic=":443"; ma=2592000; v="46,43"
Content-Length: 68
Date: Sun, 03 Jan 2021 21:20:23 GMT
Server: Google Frontend
X-Cloud-Trace-Context: 65cbc3a241aad091b5b59b6837cda159
content-type: text/html; charset=utf-8

Total slots available for FloorNum: 1 at Parking Lot nasa_east are 4
```

## Deployment to Cloud Run:
1. Create a container build by using Dockerfile:
```
gcloud builds submit --tag gcr.io/fe-shgupta/parking-lot-astra
```
2. Deploy the container using Cloud Run:
```
gcloud run deploy --image=gcr.io/fe-shgupta/parking-lot-astra --platform=managed
```

