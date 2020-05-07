import cmor
import cdms2 as cdm
import numpy as np
import MV2 as mv
import cdutil
import cdtime

cdm.setAutoBounds('on') # Caution, this attempts to automatically set coordinate bounds - please check outputs using this option
#import pdb ; # Debug statement - import if enabling below

#%% User provided input
cmorTable = '../Tables/PMPObs_Amon-morelevs.json' ; # Aday,Amon,Lmon,Omon,SImon,fx,monNobs,monStderr - Load target table, axis info (coordinates, grid*) and CVs
inputJson = 'ISCCP-input.json' ; # Update contents of this file to set your global_attributes
inputFilePathbgn = '/p/user_pub/pmp/pmp_obs_preparation/orig/data/'

inputFilePathend = ['ISCCP-H/']
inputFileName = ['clisccp_ISCCP_HGG_198301-201712.nc']
inputVarName = ['clisccp']   #['z_0001','u_0001','v_0001','t_0001'] 
outputVarName = ['clisccp']   #['zgplev3a','uaplev3a','vaplev3a','taplev3a']  
outputUnits = ['%']   #['m','m s-1','m s-1','K']


### BETTER IF THE USER DOES NOT CHANGE ANYTHING BELOW THIS LINE...
for fi in range(len(inputVarName)):
 for i in range(35):
  yr = 1983 + i

  print fi, inputVarName[fi]
  inputFilePath = inputFilePathbgn+inputFilePathend[fi]
#%% Process variable (with time axis)
# Open and read input netcdf file
  f = cdm.open(inputFilePath+inputFileName[fi])
# d1 = f(inputVarName[fi], time = (cdtime.comptime(yr,0,),cdtime.comptime(yr,12)),longitude=(6,10),latitude=(6,10))
  d1 = f(inputVarName[fi], time = (cdtime.comptime(yr,0,),cdtime.comptime(yr,12)))

  plev1 = d1.getAxis(2)  #getLevel()

  plev1[:] = plev1[:]*100.
  plev1[6] = 9000.
  plev1 = cdm.createAxis(plev1,id='plev')
  plev1.designateLevel()
  plev1.axis = 'Z'
  plev1.long_name = 'pressure'
  plev1.positive = 'down'
  plev1.realtopology = 'linear'
  plev1.standard_name = 'air_pressure'
  plev1.units = 'Pa'
#get pressure bounds
  b = plev1.getBounds()
  b[:,0] = [100000.0,80000.0,68000.0,56000.0,44000.0,31000.0,18000.0]
  b[:,1] = [80000.0,68000.0,56000.0,44000.0,31000.0,18000.0,0.0]

  lat = d1.getLatitude()
  lon = d1.getLongitude()
#time = d.getTime() ; # Assumes variable is named 'time', for the demo file this is named 'months'
  time = d1.getAxis(0) ; # Rather use a file dimension-based load statement

  tau6 = d1.getAxis(1)
# Deal with tau6 to tau7 conversion
  tau7 = np.append([0.15],tau6) #add smallest tau dimension
  tau7 = cdm.createAxis(tau7, id='tau')
  tau7.designateLevel()
  #tau7.axis = ''
  tau7.long_name = 'cloud optical thickness'
  tau7.units = ''
  tau7[:] = [0.15,0.8,2.45,6.5,16.2,41.5,100.]
  a = tau7.getBounds()
  a[:,0] = [0.0,0.3,1.3,3.6,9.4,23.0,60.0]
  a[:,1] = [0.3,1.3,3.6,9.4,23.0,60.0,100000.0]

#Pad data array with missing values
  d2 = np.ma.array(np.ma.ones([d1.shape[0],1,d1.shape[2],d1.shape[3],d1.shape[4]]),mask=True)*1e20
  d = mv.concatenate((d2,d1),axis=1)

  #del(d1,d2,tau6) # Cleanup


#%% Initialize and run CMOR
# For more information see https://cmor.llnl.gov/mydoc_cmor3_api/
  cmor.setup(inpath='./',netcdf_file_action=cmor.CMOR_REPLACE_4) #,logfile='cmorLog.txt')
  cmor.dataset_json(inputJson)
  cmor.load_table(cmorTable)

# if inputVarName[fi] == 'z_0001':

  heightAx = {'table_entry': 'plev7c',
                            'units': 'Pa',
                            'coord_vals': plev1[:],
                            'cell_bounds': b}

  axes    = [ 
              {'table_entry': 'time',
              'units': time.units, # 'days since 1870-01-01',
             },
	      {'table_entry': 'tau',
              'units': tau7.units,
	      'coord_vals': tau7[:],
              'cell_bounds': a   #tau7.getBounds()
             },
              heightAx,
              {'table_entry': 'latitude',
              'units': 'degrees_north',
              'coord_vals': lat[:],
              'cell_bounds': lat.getBounds()
              },
              {'table_entry': 'longitude',
              'units': 'degrees_east',
              'coord_vals': lon[:],
              'cell_bounds': lon.getBounds()
              },]


  axisIds = list() ; # Create list of axes
  for axis in axes:
    axisId = cmor.axis(**axis)
    axisIds.append(axisId)

#pdb.set_trace() ; # Debug statement

# Setup units and create variable to write using cmor - see https://cmor.llnl.gov/mydoc_cmor3_api/#cmor_set_variable_attribute
  d.units = outputUnits[fi]
  varid   = cmor.variable(outputVarName[fi],d.units,axisIds,missing_value=d.missing)
  values  = np.array(d[:],np.float32)

# Append valid_min and valid_max to variable before writing using cmor - see https://cmor.llnl.gov/mydoc_cmor3_api/#cmor_set_variable_attribute
#cmor.set_variable_attribute(varid,'valid_min','f',2.0)
#cmor.set_variable_attribute(varid,'valid_max','f',3.0)

# Prepare variable for writing, then write and close file - see https://cmor.llnl.gov/mydoc_cmor3_api/#cmor_set_variable_attribute
  cmor.set_deflate(varid,1,1,1) ; # shuffle=1,deflate=1,deflate_level=1 - Deflate options compress file data
  cmor.write(varid,values,time_vals=time[:],time_bnds=time.getBounds()) ; # Write variable with time axis
  f.close()
  cmor.close()
