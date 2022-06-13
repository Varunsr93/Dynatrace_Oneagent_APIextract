import invokeDynatraceApi as dynatraceapi
import os


def host_units(tenantURL, token):
    markettohudict = {}
    hostdict = dynatraceapi.dt_get_requests(tenantURL, token, "HostList", "")
    processDict(hostdict,markettohudict)
    if not hostdict["nextPageKey"] is None:
        print("---inside next page-------")
        nextPageKey = hostdict["nextPageKey"]
        nextPage = True
        while nextPage:
            hostdict = dynatraceapi.dt_get_requests(tenantURL, token, "nextPage", str(nextPageKey))
            processDict(hostdict,markettohudict)
            if hostdict["nextPageKey"] is None:
                nextPage = False
            else:
                nextPageKey = hostdict["nextPageKey"]


    return markettohudict

def processDict(hostdict,markettohudict):
    for dict in hostdict["hosts"]:
        consumedHostUnits = float(dict["hostInfo"]["consumedHostUnits"])
        Market = "Empty"
        for tags in dict["hostInfo"]["tags"]:
            if tags["key"] == "Hostgroup":
                Market = tags["value"]
        if Market not in markettohudict:
            markettohudict[Market] = consumedHostUnits
        else:
            markettohudict[Market] = markettohudict[Market] + consumedHostUnits

    return markettohudict



