#!/usr/bin/python3

"""
Cloudlog ADIF Uploader (v0.1)

George Smart, M1GEO - 02 Sept 2021
https://www.george-smart.co.uk/
https://github.com/m1geo/Cloudlog-ADIF-Uploader

Really simple script to parse an ADIF file and upload to Cloudlog using the API.
See github link above for more details.
"""

import adif_io
from datetime import datetime, timedelta
import pytz
import requests

# ADIF log file to read
ADIF_FILE = "/path/to/log/file.adi"

# How many days back should be uploaded (from now)
DAYS = 1

# Cloudlog server settings
CL_SERVER = "https://my-server.co.uk"
CL_API_KEY = "cl0000000000000"
CL_STA_PROF = 1

def convert_records_to_adif(records_to_convert):
    """Crude ADIF generator"""
    adif_str = ""
    for rec in records_to_convert: # loop records
        for itm, val in rec.items(): # loop record fields
            if itm != 't': # don't convert datetime timestamp
                l = len(val) # find adif field length
                adif_str += "<%s:%u>%s " % (itm, l, val) # write field
        adif_str += "<eor>\n" # add end of record flag
    return adif_str

def upload_to_cloudlog(adif_to_upload):
    """ADI details here: https://github.com/magicbug/Cloudlog/wiki/API"""
    payload = {"key":CL_API_KEY, "station_profile_id":CL_STA_PROF, "type":"adif", "string":adif_to_upload}
    r = requests.post("%s/Cloudlog/index.php/api/qso/" % (CL_SERVER), json=payload)
    return r

# Read ADIF file into list of dicts and sort by timestamp
print("Reading file '%s'... " % (ADIF_FILE), end="")
qsos_raw, adif_header = adif_io.read_from_file(ADIF_FILE)
for qso in qsos_raw:
    qso["t"] = adif_io.time_on(qso)
qsos_raw_sorted = sorted(qsos_raw, key = lambda qso: qso["t"], reverse=True)
qso_raw_count = len(qsos_raw_sorted)
print("%u records." % (qso_raw_count))

# Create a date that's "DAYS" behind now and then only select QSOs newer than that
print("Entries in the last %u days... " % (DAYS), end="")
timecutoff = datetime.utcnow() - timedelta(days=DAYS)
timecutoff = pytz.UTC.localize(timecutoff) # make time tz-aware
qsos_sorted_filtered = list(filter(lambda a: a['t'] > timecutoff, qsos_raw_sorted))
qsos_filtered_count = len(qsos_sorted_filtered)
print("%u records." % (qsos_filtered_count))

# Only process data if there are QSOs to upload.
if len(qsos_sorted_filtered) > 0:
    # Convert filterd new records to ADIF from a list of dicts
    adif_to_upload = convert_records_to_adif(qsos_sorted_filtered)

    # Upload to Cloudlog
    r = upload_to_cloudlog(adif_to_upload)

    # Check Server response
    if r.status_code != 201:
        print("Upload failed:")
        print(r.text)
    else:
        print("Uploaded %u QSOs." % (qsos_filtered_count))
