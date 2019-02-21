# EXECUTE THE BELOW TO PRODUCE PMPOBS
# MONTHLY
python runCmor_CERES4.0_2D.py
python runCmor_CERES4.0_SURFACE_2D.py
python runCmor_GPCP2.3.py
python runCmor_RSS_v07r01_2D.py 
python runCmor_TRMM_3B43v.7.py
python runCmor_ERA40_2D.py
python runCmor_ERA40_3D.py
python runCmor_ERAINT_2D.py
python runCmor_ERAINT_3D.py
# Longer time series
python runCmor_20CR_2D.py
python runCmor_ERA20C_2D.py

#python runCmor_JRA25_2D.py BAD TIME MODEL
#python runCmor_JRA25_3D.py   "      "

# DAILY


chmod -R 777 /p/user_pub/pmp/PCMDIobs

