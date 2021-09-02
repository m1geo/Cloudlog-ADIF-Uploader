# Cloudlog-ADIF-Uploader
Python3 based Cloudlog uploader based around adif-io and JSON POST requests to Cloudlog API

## Use
This code is currently a rough-and-ready working example. It will take a big ADIF log file (`ADIF_FILE` in the code) and upload QSOs with `DAYS` from the present time to a Cloudlog server running at `CL_SERVER`. You will need an API key for Cloudlog, [see here](https://github.com/magicbug/Cloudlog/wiki/API), which must be entered into the `CL_API_KEY` variable, along with the `CL_STA_PROF` station profile integer (by default 1, but changes if you have more than one station/location configured).

I have this code running daily on a cronjob which takes my master ADIF log file from a server and uploads the daily changes into Cloudlog.

## Requirements
* Python3
* [adif-io](https://pypi.org/project/adif-io/)
* [datetime](https://pypi.org/project/DateTime/)
* [pytz](https://pypi.org/project/pytz/)
* [requests](https://pypi.org/project/requests/)
