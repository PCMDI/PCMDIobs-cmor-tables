# EXECUTE THE BELOW TO PRODUCE PMPOBS
# MONTHLY
# SATELLITE/INSITU
python runCmor_CERES4.0_2D.py
python runCmor_CERES4.0_SURFACE_2D.py
python runCmor_GPCP2.3.py
python runCmor_RSS_2D.py
python runCmor_TRMM.py
# REANALYSIS
python runCmor_ERA40_2D.py
python runCmor_ERA40_3D.py
python runCmor_ERAINT_2D.py
python runCmor_ERAINT_3D.py
python runCmor_JRA25_2D.py
python runCmor_JRA25_3D.py 
# DAILY
chmod -R 777 /p/user_pub/pmp/PMPObs/
