import json
import requests
from lxml import html
from collections import OrderedDict
import argparse
import certifi
import urllib3

def apiData(st,dest,dep_date,ret_date = None, arr_date = None, arr_time = None, adult = None, child = None, infant = None, max_p = None, curr = "USD"):
    par = {}
    par["apikey"] = "urcU6q4MmXBZ2iWBDp7ghIGg0pygrj3x"
    par["origin"] = st
    par["destination"] = dest
    par["departure_date"] = dep_date
    if ret_date is not None:
        par["return_date"] = ret_date
    if arr_date is not None and arr_time is not None:
        par["arrive_by"] = arr_date+"T"+arr_time
    if adult is None:
        par["adults"] = 1
    else:
        par["adults"] = adult
    if child is not None or child > 0:
        par["children"] = child
    if infant is not None or infant > 0:
        par["infants"] = infant
    if max_p is not None and max_p > 0:
        par["max_price"] = max_p
    if curr is not None:
        par["currency"] = curr

    response = requests.get("https://api.sandbox.amadeus.com/v1.2/flights/low-fare-search", params = par)
    data = response.json()
    return data

def minCostPlane(data):
    if "results" not in data:
        return None
    minFare = -1
    for i in data['results']:
        atot = float(i["fare"]["price_per_adult"]["total_fare"].replace('"','').strip()) + float(i["fare"]["price_per_adult"]["tax"].replace('"','').strip())
        if "price_per_child" in i["fare"]:
            ctot = float(i["fare"]["price_per_child"]["total_fare"].replace('"','').strip()) + float(i["fare"]["price_per_child"]["tax"].replace('"','').strip())
        else:
            ctot = 0
        if "price_per_infant" in i["fare"]:
            itot = float(i["fare"]["price_per_infant"]["total_fare"].replace('"','').strip()) + float(i["fare"]["price_per_infant"]["tax"].replace('"','').strip())
        else:
            itot = 0
        if minFare < 0 or minFare > float(i["fare"]["total_price"].replace('"','').strip())+float(i["fare"]["price_per_adult"]["tax"].replace('"','').strip()):
            minFare = float(i["fare"]["total_price"].replace('"','').strip())+float(i["fare"]["price_per_adult"]["tax"].replace('"','').strip())

    resp = "Lowest Cost: %.2f %s\n" % (minFare,data['currency'])
    x = 0
#     resp = ""
    for i in data['results']:
        if minFare == float(i["fare"]["total_price"].replace('"','').strip())+float(i["fare"]["price_per_adult"]["tax"].replace('"','').strip()):
            for j in i:
                if j == "itineraries":
                    for k in range(len(i[j])):
                        x += 1
                        resp = "%s%s%s\n" % (resp,"Flight ",str(x))
                        resp = "%s%s\n" % (resp,"Outbound:")
                        out = i[j][k]["outbound"]
                        resp = "%s%s%s\n" % (resp,"Duration: ",str(out["duration"]))
    #                     print("\t\t\tFlights Options:")
                        for m in range(len(out["flights"])):
                            resp = "%s%s%s\n" % (resp,"\tConnection: ",str(m+1))
                            flight = out["flights"][m]
                            leave = flight["departs_at"]
                            resp = "%s%s%s %s\n" % (resp,"\tDeparture: ",leave[:leave.find('T')],leave[leave.find('T')+1:])
                            reach = flight["arrives_at"]
                            resp = "%s%s%s %s\n" % (resp,"\tArrival: ",reach[:reach.find('T')],reach[reach.find('T')+1:])
                            if len(flight["origin"]) == 1:
                                resp = "%s%s%s\n" % (resp,"\tOrigin: ",flight["origin"]["airport"])
                            else:
                                resp = "%s%s%s %s\n" % (resp,"\tOrigin: ",flight["origin"]["airport"],flight["origin"]["terminal"])
                            if len(flight["destination"]) == 1:
                                resp = "%s%s%s\n" % (resp,"\tDestination: ",flight["destination"]["airport"])
                            else:
                                resp = "%s%s%s %s\n" % (resp,"\tDestination: ",flight["destination"]["airport"],flight["destination"]["terminal"])
                            resp = "%s%s%s %s\n" % (resp,"\tPlane: ",flight["operating_airline"],flight["aircraft"])
                            resp = "%s%s%s\n" % (resp,"\tFlight No: ",flight["flight_number"])
                            resp = "%s%s%s\n\n" % (resp,"\tClass: ",flight["booking_info"]["travel_class"])
                        
                        resp = "%s%s\n" % (resp,"Inbound:")
                        out = i[j][k]["inbound"]
                        resp = "%s%s%s\n" % (resp,"Duration: ",str(out["duration"]))
    #                     print("\t\t\tFlights Options:")
                        for m in range(len(out["flights"])):
                            resp = "%s%s%s\n" % (resp,"\tConnection: ",str(m+1))
                            flight = out["flights"][m]
                            leave = flight["departs_at"]
                            resp = "%s%s%s %s\n" % (resp,"\tDeparture: ",leave[:leave.find('T')],leave[leave.find('T')+1:])
                            reach = flight["arrives_at"]
                            resp = "%s%s%s %s\n" % (resp,"\tArrival: ",reach[:reach.find('T')],reach[reach.find('T')+1:])
                            if len(flight["origin"]) == 1:
                                resp = "%s%s%s\n" % (resp,"\tOrigin: ",flight["origin"]["airport"])
                            else:
                                resp = "%s%s%s %s\n" % (resp,"\tOrigin: ",flight["origin"]["airport"],flight["origin"]["terminal"])
                            if len(flight["destination"]) == 1:
                                resp = "%s%s%s\n" % (resp,"\tDestination: ",flight["destination"]["airport"])
                            else:
                                resp = "%s%s%s %s\n" % (resp,"\tDestination: ",flight["destination"]["airport"],flight["destination"]["terminal"])
                            resp = "%s%s%s %s\n" % (resp,"\tPlane: ",flight["operating_airline"],flight["aircraft"])
                            resp = "%s%s%s\n" % (resp,"\tFlight No: ",flight["flight_number"])
                            resp = "%s%s%s\n\n" % (resp,"\tClass: ",flight["booking_info"]["travel_class"])
                elif j == "fare":
                    for k in i[j]:
                        if k == "price_per_adult":
                            resp = "%s%s\n" % (resp,"Adult:")
                            resp = "%s%s%s\n" % (resp,"\tTotal Price: ",i[j][k]["total_fare"])
                            resp = "%s%s%s\n" % (resp,"\tTax: ",i[j][k]["tax"])
                        elif k == "price_per_child":
                            resp = "%s%s\n" % (resp,"Child:")
                            resp = "%s%s%s\n" % (resp,"\tTotal Price: ",i[j][k]["total_fare"])
                            resp = "%s%s%s\n" % (resp,"\tTax: ",i[j][k]["tax"])
                        elif k == "price_per_infant":
                            resp = "%s%s\n" % (resp,"Infant:")
                            resp = "%s%s%s\n" % (resp,"\tTotal Price: ",i[j][k]["total_fare"])
                            resp = "%s%s%s\n" % (resp,"\tTax: ",i[j][k]["tax"])
                        elif k == "restrictions":
                            resp = "%s%s%s\n" % (resp,"Refundable: ",i[j][k]["refundable"])
                            resp = "%s%s%s\n" % (resp,"Change Penalty: ",i[j][k]["change_penalties"])
    #                     else:
    #                         print(k,i[j][k])
            resp = "%s\n" % resp

    return resp

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/', methods=["POST"])
def newform():
    if request.method == "POST":
        st = request.form["st"]
        dest = request.form["dest"]
        dep_date = request.form["dep_date"]
        ret_date = request.form["ret_date"]
        adult = int(request.form["adult"])
        child = int(request.form["child"])
        infant = int(request.form["infant"])
        
        x = apiData(st,dest,dep_date,ret_date = ret_date, adult = adult, child = child, infant = infant)
        if x is None:
            out = "No flights available"
        else:
            out = minCostPlane(x)
#        out = x
        
        return render_template("index.html", out = out)
if __name__ == "__main__":
    app.run(debug=True)