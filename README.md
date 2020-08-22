# ztf-bts-filters

Filter code for finding transient candidates in the ZTF alert stream for the Bright Transient Survey.

The Bright Transient Survey (BTS) aims to record and announce all extragalactic transients brighter than <19 mag and obtain spectroscopy of all transients brighter than <18.5.  Filtering is performed on the GROWTH Marshal using a simple custom language; python conversions are provided here.  The filter has changed several times during the project, but only two of these changes were major.  Three filter versions are provided below:

2018.py : Used from the start of the project until summer 2019.
2019.py : Used from summer 2019 until summer 2020.
2020.py : Used from summer 2020 onward.

The filters parse ZTF avro packets converted to python lists/dictionaries.  See the ZTF avro schema (https://zwickytransientfacility.github.io/ztf-avro-alert/) for more information.

Further explanation of these filters can be found in Fremling et al. (2020, ApJ 895:32) and Perley et al. (in prep).
