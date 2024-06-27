'''
  demo_geofences.py - This is basic Finamon GNSS/4G Modem HAT Shield positioning function example.
'''
import time
import sys
sys.path.append('./')   # Adds higher directory to python modules path.


from gps4ghat.BG77X import BG77X
from gps4ghat.BG77X import GEO_FENCE_REPORT_MODE
from gps4ghat.BG77X import GEO_FENCE_SHAPE

def rect(lat, lon, x, y):
    x = x/2
    y = y/2
    return [(round(lat + x,5), round(lon + y,5)),
            (round(lat + x,5), round(lon - y,5)),
            (round(lat - x,5), round(lon - y,5)),
            (round(lat - x,5), round(lon + y,5))]


lat_org = 51.22906
lon_org = 6.71467

geofence_center =  [(lat_org, lon_org)]

geofence_quad = [
    (round(lat_org + 0.00010,5), round(lon_org - 0.00008,5)),
    (round(lat_org + 0.00012,5), round(lon_org - 0.00001,5)),
    (round(lat_org - 0.00004,5), round(lon_org + 0.00007,5)),
    (round(lat_org - 0.00006,5), round(lon_org + 0.00001,5)),
     ]

geofence_query = [
    "position unknown",
    "position is inside the geo-fence",
    "position is outside the geo-fence",
    "geo-fence ID does not exist"
    ]

print("\nhttps://maps.google.com/?q=%s,%s\n" % (lat_org, lon_org))

navigator = BG77X()
navigator.gnssOn()
time.sleep(2.)

try:
    sleep_time = 10
    start_time = time.time()
    while(not navigator.acquirePositionInfo()):
        navigator.acquireSatellitesInfo()
        time.sleep(sleep_time)

    print ("position search time %s seconds" % int(time.time() - start_time))

    circle = 0
    quad   = 3

    navigator.addGeofence(circle, GEO_FENCE_REPORT_MODE.ENTER_LEAVE, GEO_FENCE_SHAPE.CIRCLE_RADIUS, geofence_center, 100)
    navigator.queryGeofence(circle)

    navigator.addGeofence(quad, GEO_FENCE_REPORT_MODE.ENTER_LEAVE, GEO_FENCE_SHAPE.QUADRANGLE, geofence_quad)
    navigator.queryGeofence(quad)

    print(geofence_query[navigator.queryGeofence(circle)])
    print(geofence_query[navigator.queryGeofence(quad)])

    navigator.deleteGeofence(circle)
    navigator.deleteGeofence(quad)

    # create 10 geofences in form of shuting target with radius step 10 meter 
    for geoid in range(9):
        navigator.addGeofence(geoid, GEO_FENCE_REPORT_MODE.ENTER_LEAVE, GEO_FENCE_SHAPE.CIRCLE_RADIUS, geofence_center, (geoid + 1) * 10)

    for i in range(10):
        points = list('---------')
        for geoid in range(9):
            res = navigator.queryGeofence(geoid)
            if(res == 1):
                points[geoid] = '+'
        str_points = ''.join(points)        
        print(str_points)
        time.sleep(5.)

    navigator.gnssOff()
    navigator.close()

finally:
    print("Ctrl+C pressed, switch BG77X off and exit")
    navigator.close()
    sys.exit(0)
