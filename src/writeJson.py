#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 15:53:01 2018

Paul J. Durack 24th January 2018

This script generates all json files residing in this subdirectory

PJD 24 Jan 2018     - Started, copied from https://github.com/PCMDI/obs4MIPs-cmor-tables

@author: durack1
"""

#%% Import statements
import copy,gc,json,os,re,shutil,ssl,subprocess,sys,time
from durolib import readJsonCreateDict ; #getGitInfo

#%% Determine path
#homePath = os.path.join('/','/'.join(os.path.realpath(__file__).split('/')[0:-1]))
#homePath = '/export/durack1/git/obs4MIPs-cmor-tables/' ; # Linux
homePath = '/sync/git/PMPObs-cmor-tables/src' ; # OS-X
#os.chdir(homePath)

#%% Create urllib2 context to deal with lab/LLNL web certificates
ctx                 = ssl.create_default_context()
ctx.check_hostname  = False
ctx.verify_mode     = ssl.CERT_NONE

#%% List target tables
masterTargets = [
 'Amon',
 'Lmon',
 'Omon',
 'SImon',
 'fx',
 'coordinate',
 'formula_terms',
 'frequency',
 'grid_label',
 'grids',
 'institution_id',
 'license_',
 'nominal_resolution',
 'product',
 'realm',
 'region',
 'required_global_attributes',
 'source_id',
 'source_type',
 'table_id'
 ] ;

#%% Tables
tableSource = [
 ['coordinate','https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/master/Tables/obs4MIPs_coordinate.json'],
 ['formula_terms','https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/master/Tables/obs4MIPs_formula_terms.json'],
 ['frequency','https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/master/CMIP6_frequency.json'],
 ['fx','https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/master/Tables/obs4MIPs_fx.json'],
 ['grid_label','https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/master/CMIP6_grid_label.json'],
 ['grids','https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/master/Tables/obs4MIPs_grids.json'],
 ['nominal_resolution','https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/master/CMIP6_nominal_resolution.json'],
 ['product','https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/master/obs4MIPs_product.json'],
 ['nominal_resolution','https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/master/CMIP6_nominal_resolution.json'],
 ['realm','https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/master/obs4MIPs_realm.json'],
 ['region','https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/master/obs4MIPs_region.json'],
 ['Amon','https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/master/Tables/obs4MIPs_Amon.json'],
 ['Lmon','https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/master/Tables/obs4MIPs_Lmon.json'],
 ['Omon','https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/master/Tables/obs4MIPs_Omon.json'],
 ['SImon','https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/master/Tables/obs4MIPs_SImon.json']
 ] ;

#%% Loop through tables and create in-memory objects
# Loop through tableSource and create output tables
tmp = readJsonCreateDict(tableSource)
for count,table in enumerate(tmp.keys()):
    #print 'table:', table
    if table in ['frequency','grid_label','nominal_resolution']:
        vars()[table] = tmp[table].get(table)
    else:
        vars()[table] = tmp[table]
del(tmp,count,table) ; gc.collect()

'''
None of this should be required
# Cleanup by extracting only variable lists
for count2,table in enumerate(tableSource):
    tableName = table[0]
    #print 'tableName:',tableName
    #print eval(tableName)
    if tableName in ['coordinate','formula_terms','frequency','grid_label','nominal_resolution']:
        continue
    else:
        if tableName in ['monNobs', 'monStderr']:
            eval(tableName)['Header'] = copy.deepcopy(Amon['Header']) ; # Copy header info from upstream file
            del(eval(tableName)['Header']['#dataRequest_specs_version']) ; # Purge upstream identifier
            eval(tableName)['Header']['realm'] = 'aerosol atmos atmosChem land landIce ocean ocnBgchem seaIce' ; # Append all realms
        eval(tableName)['Header']['Conventions'] = 'CF-1.7 ODS-2.1' ; # Update "Conventions": "CF-1.7 CMIP-6.0"
        if tableName not in ['monNobs', 'monStderr']:
            eval(tableName)['Header']['#dataRequest_specs_version'] = eval(tableName)['Header']['data_specs_version']
        eval(tableName)['Header']['data_specs_version'] = '2.1.0'
        if 'mip_era' in eval(tableName)['Header'].keys():
            eval(tableName)['Header']['#mip_era'] = eval(tableName)['Header']['mip_era']
            del(eval(tableName)['Header']['mip_era']) ; # Remove after rewriting
        eval(tableName)['Header']['product'] = 'observations' ; # Cannot be 'observations reanalysis'
        eval(tableName)['Header']['table_date'] = time.strftime('%d %B %Y')
        eval(tableName)['Header']['table_id'] = ''.join(['Table obs4MIPs_',tableName])
        # Attempt to move information from input.json to table files - #84 - CMOR-limited
        #eval(tableName)['Header']['activity_id'] = 'obs4MIPs'
        #eval(tableName)['Header']['_further_info_url_tmpl'] = 'http://furtherinfo.es-doc.org/<activity_id><institution_id><source_label><source_id><variable_id>'
        #eval(tableName)['Header']['output_file_template'] = '<variable_id><table_id><source_id><variant_label><grid_label>'
        #eval(tableName)['Header']['output_path_template'] = '<activity_id><institution_id><source_id><table_id><variable_id><grid_label><version>'
        #eval(tableName)['Header']['tracking_prefix'] = 'hdl:21.14102'
        #eval(tableName)['Header']['_control_vocabulary_file'] = 'obs4MIPs_CV.json'
        #eval(tableName)['Header']['_AXIS_ENTRY_FILE'] = 'obs4MIPs_coordinate.json'
        #eval(tableName)['Header']['_FORMULA_VAR_FILE'] = 'obs4MIPs_formula_terms.json'
        if 'baseURL' in eval(tableName)['Header'].keys():
            del(eval(tableName)['Header']['baseURL']) ; # Remove spurious entry

# Cleanup realms
Amon['Header']['realm']     = 'atmos'
Amon['variable_entry'].pop('pfull')
Amon['variable_entry'].pop('phalf')
Lmon['Header']['realm']     = 'land'
Omon['Header']['realm']     = 'ocean'
SImon['Header']['realm']    = 'seaIce'
fx['Header']['realm']       = 'fx'
Aday['Header']['table_id']  = 'Table obs4MIPs_Aday' ; # Cleanup from upstream

# Clean out modeling_realm
for jsonName in ['Aday','Amon','Lmon','Omon','SImon']:
    dictToClean = eval(jsonName)
    for key, value in dictToClean.iteritems():
        if key == 'Header':
            continue
        for key1,value1 in value.iteritems():
            if 'modeling_realm' in dictToClean[key][key1].keys():
                dictToClean[key][key1].pop('modeling_realm')
            if 'cell_measures' in dictToClean[key][key1].keys():
                dictToClean[key][key1]['cell_measures'] = '' ; # Set all cell_measures entries to blank

# Set missing value for integer variables
for tab in (Aday, Amon, Lmon, Omon, SImon, fx, Aday, monNobs, monStderr):
    tab['Header']['int_missing_value'] = str(-2**31)

# Add new variables
# Variable sponsor - NOAA-NCEI; Jim Baird (JimBiardCics)
Amon['variable_entry'][u'ttbr'] = {}
Amon['variable_entry']['ttbr']['cell_measures'] = ''
Amon['variable_entry']['ttbr']['cell_methods'] = 'time: mean'
Amon['variable_entry']['ttbr']['comment'] = ''
Amon['variable_entry']['ttbr']['dimensions'] = 'longitude latitude time'
Amon['variable_entry']['ttbr']['frequency'] = 'mon'
Amon['variable_entry']['ttbr']['long_name'] = 'Top of Atmosphere Brightness Temperature'
Amon['variable_entry']['ttbr']['ok_max_mean_abs'] = ''
Amon['variable_entry']['ttbr']['ok_min_mean_abs'] = ''
Amon['variable_entry']['ttbr']['out_name'] = 'ttbr'
Amon['variable_entry']['ttbr']['positive'] = ''
Amon['variable_entry']['ttbr']['standard_name'] = 'toa_brightness_temperature'
Amon['variable_entry']['ttbr']['type'] = 'real'
Amon['variable_entry']['ttbr']['units'] = 'K'
Amon['variable_entry']['ttbr']['valid_max'] = ''
Amon['variable_entry']['ttbr']['valid_min'] = ''
# Variable sponsor - NOAA-NCEI; Jim Baird (JimBiardCics) https://github.com/PCMDI/obs4MIPs-cmor-tables/issues/16
Lmon['variable_entry'][u'ndvi'] = {}
Lmon['variable_entry']['ndvi']['cell_measures'] = ''
Lmon['variable_entry']['ndvi']['cell_methods'] = 'area: mean where land time: mean'
Lmon['variable_entry']['ndvi']['comment'] = ''
Lmon['variable_entry']['ndvi']['dimensions'] = 'longitude latitude time'
Lmon['variable_entry']['ndvi']['frequency'] = 'mon'
Lmon['variable_entry']['ndvi']['long_name'] = 'Normalized Difference Vegetation Index'
Lmon['variable_entry']['ndvi']['ok_max_mean_abs'] = ''
Lmon['variable_entry']['ndvi']['ok_min_mean_abs'] = ''
Lmon['variable_entry']['ndvi']['out_name'] = 'ndvi'
Lmon['variable_entry']['ndvi']['positive'] = ''
Lmon['variable_entry']['ndvi']['standard_name'] = 'normalized_difference_vegetation_index'
Lmon['variable_entry']['ndvi']['type'] = 'real'
Lmon['variable_entry']['ndvi']['units'] = '1'
Lmon['variable_entry']['ndvi']['valid_max'] = '1.0'
Lmon['variable_entry']['ndvi']['valid_min'] = '-0.1'
# Variable sponsor - NOAA-NCEI; Jim Baird (JimBiardCics) https://github.com/PCMDI/obs4MIPs-cmor-tables/issues/15
Lmon['variable_entry'][u'fapar'] = {}
Lmon['variable_entry']['fapar']['cell_measures'] = ''
Lmon['variable_entry']['fapar']['cell_methods'] = 'area: mean where land time: mean'
Lmon['variable_entry']['fapar']['comment'] = 'The fraction of incoming solar radiation in the photosynthetically active radiation spectral region that is absorbed by a vegetation canopy.'
Lmon['variable_entry']['fapar']['dimensions'] = 'longitude latitude time'
Lmon['variable_entry']['fapar']['frequency'] = 'mon'
Lmon['variable_entry']['fapar']['long_name'] = 'Fraction of Absorbed Photosynthetically Active Radiation'
Lmon['variable_entry']['fapar']['ok_max_mean_abs'] = ''
Lmon['variable_entry']['fapar']['ok_min_mean_abs'] = ''
Lmon['variable_entry']['fapar']['out_name'] = 'fapar'
Lmon['variable_entry']['fapar']['positive'] = ''
Lmon['variable_entry']['fapar']['standard_name'] = 'fraction_of_surface_downwelling_photosynthetic_radiative_flux_absorbed_by_vegetation'
Lmon['variable_entry']['fapar']['type'] = 'real'
Lmon['variable_entry']['fapar']['units'] = '1'
Lmon['variable_entry']['fapar']['valid_max'] = '1.0'
Lmon['variable_entry']['fapar']['valid_min'] = '0.0'
#####################################################################################################################
# DWD cloud variables (CM SAF CLARA & ESA Cloud_CCI) ...
# Variable sponsor - DWD; Stephan Finkensieper (Funkensieper) https://github.com/PCMDI/obs4MIPs-cmor-tables/issues/48
Amon['variable_entry'][u'clCCI'] = {}
Amon['variable_entry']['clCCI']['cell_measures'] = ''
Amon['variable_entry']['clCCI']['cell_methods'] = 'area: time: mean'
Amon['variable_entry']['clCCI']['comment'] = 'Percentage cloud cover in optical depth categories.'
Amon['variable_entry']['clCCI']['dimensions'] = 'longitude latitude plev7c tau time'
Amon['variable_entry']['clCCI']['frequency'] = 'mon'
Amon['variable_entry']['clCCI']['long_name'] = 'CCI Cloud Area Fraction'
Amon['variable_entry']['clCCI']['ok_max_mean_abs'] = ''
Amon['variable_entry']['clCCI']['ok_min_mean_abs'] = ''
Amon['variable_entry']['clCCI']['out_name'] = 'clCCI'
Amon['variable_entry']['clCCI']['positive'] = ''
Amon['variable_entry']['clCCI']['standard_name'] = 'cloud_area_fraction_in_atmosphere_layer'
Amon['variable_entry']['clCCI']['type'] = 'real'
Amon['variable_entry']['clCCI']['units'] = '%'
Amon['variable_entry']['clCCI']['valid_max'] = ''
Amon['variable_entry']['clCCI']['valid_min'] = ''
# Variable sponsor - DWD; Stephan Finkensieper (Funkensieper) https://github.com/PCMDI/obs4MIPs-cmor-tables/issues/48
Amon['variable_entry'][u'clCLARA'] = {}
Amon['variable_entry']['clCLARA']['cell_measures'] = ''
Amon['variable_entry']['clCLARA']['cell_methods'] = 'area: mean time: mean'
Amon['variable_entry']['clCLARA']['comment'] = 'Percentage cloud cover in optical depth categories.'
Amon['variable_entry']['clCLARA']['dimensions'] = 'longitude latitude plev7c tau time'
Amon['variable_entry']['clCLARA']['frequency'] = 'mon'
Amon['variable_entry']['clCLARA']['long_name'] = 'CLARA Cloud Area Fraction'
Amon['variable_entry']['clCLARA']['ok_max_mean_abs'] = ''
Amon['variable_entry']['clCLARA']['ok_min_mean_abs'] = ''
Amon['variable_entry']['clCLARA']['out_name'] = 'clCLARA'
Amon['variable_entry']['clCLARA']['positive'] = ''
Amon['variable_entry']['clCLARA']['standard_name'] = 'cloud_area_fraction_in_atmosphere_layer'
Amon['variable_entry']['clCLARA']['type'] = 'real'
Amon['variable_entry']['clCLARA']['units'] = '%'
Amon['variable_entry']['clCLARA']['valid_max'] = ''
Amon['variable_entry']['clCLARA']['valid_min'] = ''
# Variable sponsor - DWD; Stephan Finkensieper (Funkensieper) https://github.com/PCMDI/obs4MIPs-cmor-tables/issues/48
Amon['variable_entry'][u'cltCCI'] = {}
Amon['variable_entry']['cltCCI']['cell_measures'] = ''
Amon['variable_entry']['cltCCI']['cell_methods'] = 'area: time: mean'
Amon['variable_entry']['cltCCI']['comment'] = 'Total cloud area fraction for the whole atmospheric column, as seen from the surface or the top of the atmosphere. Includes both large-scale and convective cloud.'
Amon['variable_entry']['cltCCI']['dimensions'] = 'longitude latitude time'
Amon['variable_entry']['cltCCI']['frequency'] = 'mon'
Amon['variable_entry']['cltCCI']['long_name'] = 'CCI Total Cloud Fraction'
Amon['variable_entry']['cltCCI']['ok_max_mean_abs'] = ''
Amon['variable_entry']['cltCCI']['ok_min_mean_abs'] = ''
Amon['variable_entry']['cltCCI']['out_name'] = 'cltCCI'
Amon['variable_entry']['cltCCI']['positive'] = ''
Amon['variable_entry']['cltCCI']['standard_name'] = 'cloud_area_fraction'
Amon['variable_entry']['cltCCI']['type'] = 'real'
Amon['variable_entry']['cltCCI']['units'] = '%'
Amon['variable_entry']['cltCCI']['valid_max'] = ''
Amon['variable_entry']['cltCCI']['valid_min'] = ''
# Variable sponsor - DWD; Stephan Finkensieper (Funkensieper) https://github.com/PCMDI/obs4MIPs-cmor-tables/issues/48
Amon['variable_entry'][u'cltCLARA'] = {}
Amon['variable_entry']['cltCLARA']['cell_measures'] = ''
Amon['variable_entry']['cltCLARA']['cell_methods'] = 'area: mean time: mean'
Amon['variable_entry']['cltCLARA']['comment'] = 'Total cloud area fraction for the whole atmospheric column, as seen from the surface or the top of the atmosphere. Includes both large-scale and convective cloud.'
Amon['variable_entry']['cltCLARA']['dimensions'] = 'longitude latitude time'
Amon['variable_entry']['cltCLARA']['frequency'] = 'mon'
Amon['variable_entry']['cltCLARA']['long_name'] = 'CLARA Total Cloud Fraction'
Amon['variable_entry']['cltCLARA']['ok_max_mean_abs'] = ''
Amon['variable_entry']['cltCLARA']['ok_min_mean_abs'] = ''
Amon['variable_entry']['cltCLARA']['out_name'] = 'cltCLARA'
Amon['variable_entry']['cltCLARA']['positive'] = ''
Amon['variable_entry']['cltCLARA']['standard_name'] = 'cloud_area_fraction'
Amon['variable_entry']['cltCLARA']['type'] = 'real'
Amon['variable_entry']['cltCLARA']['units'] = '%'
Amon['variable_entry']['cltCLARA']['valid_max'] = ''
Amon['variable_entry']['cltCLARA']['valid_min'] = ''
# Variable sponsor - DWD; Stephan Finkensieper (Funkensieper) https://github.com/PCMDI/obs4MIPs-cmor-tables/issues/48
Amon['variable_entry'][u'clwCCI'] = {}
Amon['variable_entry']['clwCCI']['cell_measures'] = ''
Amon['variable_entry']['clwCCI']['cell_methods'] = 'area: time: mean'
Amon['variable_entry']['clwCCI']['comment'] = 'Percentage liquid cloud cover in optical depth categories.'
Amon['variable_entry']['clwCCI']['dimensions'] = 'longitude latitude plev7c tau time'
Amon['variable_entry']['clwCCI']['frequency'] = 'mon'
Amon['variable_entry']['clwCCI']['long_name'] = 'CCI Liquid Cloud Area Fraction'
Amon['variable_entry']['clwCCI']['ok_max_mean_abs'] = ''
Amon['variable_entry']['clwCCI']['ok_min_mean_abs'] = ''
Amon['variable_entry']['clwCCI']['out_name'] = 'clwCCI'
Amon['variable_entry']['clwCCI']['positive'] = ''
Amon['variable_entry']['clwCCI']['standard_name'] = 'liquid_water_cloud_area_fraction_in_atmosphere_layer'
Amon['variable_entry']['clwCCI']['type'] = 'real'
Amon['variable_entry']['clwCCI']['units'] = '%'
Amon['variable_entry']['clwCCI']['valid_max'] = ''
Amon['variable_entry']['clwCCI']['valid_min'] = ''
# Variable sponsor - DWD; Stephan Finkensieper (Funkensieper) https://github.com/PCMDI/obs4MIPs-cmor-tables/issues/48
Amon['variable_entry'][u'clwCLARA'] = {}
Amon['variable_entry']['clwCLARA']['cell_measures'] = ''
Amon['variable_entry']['clwCLARA']['cell_methods'] = 'area: mean time: mean'
Amon['variable_entry']['clwCLARA']['comment'] = 'Percentage liquid cloud cover in optical depth categories.'
Amon['variable_entry']['clwCLARA']['dimensions'] = 'longitude latitude plev7c tau time'
Amon['variable_entry']['clwCLARA']['frequency'] = 'mon'
Amon['variable_entry']['clwCLARA']['long_name'] = 'CLARA Liquid Cloud Area Fraction'
Amon['variable_entry']['clwCLARA']['ok_max_mean_abs'] = ''
Amon['variable_entry']['clwCLARA']['ok_min_mean_abs'] = ''
Amon['variable_entry']['clwCLARA']['out_name'] = 'clwCLARA'
Amon['variable_entry']['clwCLARA']['positive'] = ''
Amon['variable_entry']['clwCLARA']['standard_name'] = 'liquid_water_cloud_area_fraction_in_atmosphere_layer'
Amon['variable_entry']['clwCLARA']['type'] = 'real'
Amon['variable_entry']['clwCLARA']['units'] = '%'
Amon['variable_entry']['clwCLARA']['valid_max'] = ''
Amon['variable_entry']['clwCLARA']['valid_min'] = ''
# Variable sponsor - DWD; Stephan Finkensieper (Funkensieper) https://github.com/PCMDI/obs4MIPs-cmor-tables/issues/48
Amon['variable_entry'][u'clwtCCI'] = {}
Amon['variable_entry']['clwtCCI']['cell_measures'] = ''
Amon['variable_entry']['clwtCCI']['cell_methods'] = 'area: time: mean'
Amon['variable_entry']['clwtCCI']['comment'] = ''
Amon['variable_entry']['clwtCCI']['dimensions'] = 'longitude latitude time'
Amon['variable_entry']['clwtCCI']['frequency'] = 'mon'
Amon['variable_entry']['clwtCCI']['long_name'] = 'CCI Total Liquid Cloud Area Fraction'
Amon['variable_entry']['clwtCCI']['ok_max_mean_abs'] = ''
Amon['variable_entry']['clwtCCI']['ok_min_mean_abs'] = ''
Amon['variable_entry']['clwtCCI']['out_name'] = 'clwtCCI'
Amon['variable_entry']['clwtCCI']['positive'] = ''
Amon['variable_entry']['clwtCCI']['standard_name'] = 'liquid_water_cloud_area_fraction'
Amon['variable_entry']['clwtCCI']['type'] = 'real'
Amon['variable_entry']['clwtCCI']['units'] = '%'
Amon['variable_entry']['clwtCCI']['valid_max'] = ''
Amon['variable_entry']['clwtCCI']['valid_min'] = ''
# Variable sponsor - DWD; Stephan Finkensieper (Funkensieper) https://github.com/PCMDI/obs4MIPs-cmor-tables/issues/48
Amon['variable_entry'][u'clwtCLARA'] = {}
Amon['variable_entry']['clwtCLARA']['cell_measures'] = ''
Amon['variable_entry']['clwtCLARA']['cell_methods'] = 'area: mean time: mean'
Amon['variable_entry']['clwtCLARA']['comment'] = ''
Amon['variable_entry']['clwtCLARA']['dimensions'] = 'longitude latitude time'
Amon['variable_entry']['clwtCLARA']['frequency'] = 'mon'
Amon['variable_entry']['clwtCLARA']['long_name'] = 'CLARA Total Liquid Cloud Area Fraction'
Amon['variable_entry']['clwtCLARA']['ok_max_mean_abs'] = ''
Amon['variable_entry']['clwtCLARA']['ok_min_mean_abs'] = ''
Amon['variable_entry']['clwtCLARA']['out_name'] = 'clwtCLARA'
Amon['variable_entry']['clwtCLARA']['positive'] = ''
Amon['variable_entry']['clwtCLARA']['standard_name'] = 'liquid_water_cloud_area_fraction'
Amon['variable_entry']['clwtCLARA']['type'] = 'real'
Amon['variable_entry']['clwtCLARA']['units'] = '%'
Amon['variable_entry']['clwtCLARA']['valid_max'] = ''
Amon['variable_entry']['clwtCLARA']['valid_min'] = ''
# Variable sponsor - DWD; Stephan Finkensieper (Funkensieper) https://github.com/PCMDI/obs4MIPs-cmor-tables/issues/48
Amon['variable_entry'][u'pctCCI'] = {}
Amon['variable_entry']['pctCCI']['cell_measures'] = ''
Amon['variable_entry']['pctCCI']['cell_methods'] = 'area: time: mean'
Amon['variable_entry']['pctCCI']['comment'] = ''
Amon['variable_entry']['pctCCI']['dimensions'] = 'longitude latitude time'
Amon['variable_entry']['pctCCI']['frequency'] = 'mon'
Amon['variable_entry']['pctCCI']['long_name'] = 'CCI Mean Cloud Top Pressure'
Amon['variable_entry']['pctCCI']['ok_max_mean_abs'] = ''
Amon['variable_entry']['pctCCI']['ok_min_mean_abs'] = ''
Amon['variable_entry']['pctCCI']['out_name'] = 'pctCCI'
Amon['variable_entry']['pctCCI']['positive'] = ''
Amon['variable_entry']['pctCCI']['standard_name'] = 'air_pressure_at_cloud_top'
Amon['variable_entry']['pctCCI']['type'] = 'real'
Amon['variable_entry']['pctCCI']['units'] = 'Pa'
Amon['variable_entry']['pctCCI']['valid_max'] = ''
Amon['variable_entry']['pctCCI']['valid_min'] = ''
# Variable sponsor - DWD; Stephan Finkensieper (Funkensieper) https://github.com/PCMDI/obs4MIPs-cmor-tables/issues/48
Amon['variable_entry'][u'pctCLARA'] = {}
Amon['variable_entry']['pctCLARA']['cell_measures'] = ''
Amon['variable_entry']['pctCLARA']['cell_methods'] = 'area: mean time: mean'
Amon['variable_entry']['pctCLARA']['comment'] = ''
Amon['variable_entry']['pctCLARA']['dimensions'] = 'longitude latitude time'
Amon['variable_entry']['pctCLARA']['frequency'] = 'mon'
Amon['variable_entry']['pctCLARA']['long_name'] = 'CLARA Mean Cloud Top Pressure'
Amon['variable_entry']['pctCLARA']['ok_max_mean_abs'] = ''
Amon['variable_entry']['pctCLARA']['ok_min_mean_abs'] = ''
Amon['variable_entry']['pctCLARA']['out_name'] = 'pctCLARA'
Amon['variable_entry']['pctCLARA']['positive'] = ''
Amon['variable_entry']['pctCLARA']['standard_name'] = 'air_pressure_at_cloud_top'
Amon['variable_entry']['pctCLARA']['type'] = 'real'
Amon['variable_entry']['pctCLARA']['units'] = 'Pa'
Amon['variable_entry']['pctCLARA']['valid_max'] = ''
Amon['variable_entry']['pctCLARA']['valid_min'] = ''
# Variable sponsor - DWD; Stephan Finkensieper (Funkensieper) https://github.com/PCMDI/obs4MIPs-cmor-tables/issues/72
Amon['variable_entry'][u'pme'] = {}
Amon['variable_entry']['pme']['cell_measures'] = ''
Amon['variable_entry']['pme']['cell_methods'] = 'area: time: mean'
Amon['variable_entry']['pme']['comment'] = ('Net flux of water (in all phases) between the atmosphere and underlying surface '
                                            'including vegetation), mainly resulting from the difference of precipitation '
                                            'and evaporation')
Amon['variable_entry']['pme']['dimensions'] = 'longitude latitude time'
Amon['variable_entry']['pme']['frequency'] = 'mon'
Amon['variable_entry']['pme']['long_name'] = 'Surface Downward Freshwater Flux'
Amon['variable_entry']['pme']['ok_max_mean_abs'] = ''
Amon['variable_entry']['pme']['ok_min_mean_abs'] = ''
Amon['variable_entry']['pme']['out_name'] = 'pme'
Amon['variable_entry']['pme']['positive'] = ''
Amon['variable_entry']['pme']['standard_name'] = 'surface_downward_water_flux'
Amon['variable_entry']['pme']['type'] = 'real'
Amon['variable_entry']['pme']['units'] = 'kg m-2 s-1'
Amon['variable_entry']['pme']['valid_max'] = ''
Amon['variable_entry']['pme']['valid_min'] = ''

# monNobs
#--------
# Example new monNobs entry
#monNobs['variable_entry'][u'ndviNobs']['comment'] = ''
#monNobs['variable_entry'][u'ndviNobs']['dimensions'] = 'longitude latitude time'
#monNobs['variable_entry'][u'ndviNobs']['frequency'] = 'mon'
#monNobs['variable_entry'][u'ndviNobs']['long_name'] = 'NDVI number of observations'
#monNobs['variable_entry'][u'ndviNobs']['modeling_realm'] = 'atmos' ; # Overwrites table realm entry (CMOR will fail if multiple realms are set in the header and this field is missing)
#monNobs['variable_entry'][u'ndviNobs']['out_name'] = 'ndviNobs'
#monNobs['variable_entry'][u'ndviNobs']['standard_name'] = 'number_of_observations'
#monNobs['variable_entry'][u'ndviNobs']['type'] = ''
#monNobs['variable_entry'][u'ndviNobs']['units'] = '1'

# monStderr
#--------
# Example new monStderr entry
#monStderr['variable_entry'][u'ndviStderr'] = {}
#monStderr['variable_entry'][u'ndviStderr']['comment'] = ''
#monStderr['variable_entry'][u'ndviStderr']['dimensions'] = 'longitude latitude time'
#monStderr['variable_entry'][u'ndviStderr']['frequency'] = 'mon'
#monStderr['variable_entry'][u'ndviStderr']['long_name'] = 'NDVI standard error'
#monStderr['variable_entry'][u'ndviStderr']['modeling_realm'] = 'atmos' ; # Overwrites table realm entry (CMOR will fail if multiple realms are set in the header and this field is missing)
#monStderr['variable_entry'][u'ndviStderr']['out_name'] = 'ndviStderr'
#monStderr['variable_entry'][u'ndviStderr']['standard_name'] = 'normalized_difference_vegetation_index standard_error'
#monStderr['variable_entry'][u'ndviStderr']['type'] = 'real'
#monStderr['variable_entry'][u'ndviStderr']['units'] = ''
'''

#%% Coordinate

#%% Frequency

#%% Grid

#%% Grid label

#%% Institution
tmp = [['institution_id','https://raw.githubusercontent.com/PCMDI/obs4mips-cmor-tables/master/obs4MIPs_institution_id.json']
      ] ;
#institution_id = readJsonCreateDict(tmp)
#institution_id = institution_id.get('institution_id')

# Fix issues
institution_id ={}
institution_id['institution_id'] = {}
institution_id['institution_id']['ECMWF'] = 'The European Centre for Medium-Range Weather Forecasts, Shinfield Park, Reading RG2 9AX, UK'
'''
List from https://goo.gl/GySZ56 to be updated
ERA-40/ECMWF
JRA-25/MRI
AIRS/?
MLS/?
CERES/?
GPCP/UofMD
TRMM/?
RSS/REMSS
ISCCP/?
MODIS/?
CALIPSO/?
WOA13v2/NOAA-NCEI
Hosoda/?
IPRC/?
UCSD/?
ERSSTv3b/NOAA-NCEI
GISTEMP/NASA-GISS
HadCRUT4.5/MOHC
Kaplan_Extended_V2/?
NOC1.1/NOC
OAFluxV3/WHOI
Aquarius/REMSS
SMOS/?
'''
#==============================================================================
# Example new institution_id entry
#institution_id['institution_id']['NOAA-NCEI'] = 'NOAA\'s National Centers for Environmental Information, Asheville, NC 28801, USA'
#institution_id['institution_id']['RSS'] = 'Remote Sensing Systems, Santa Rosa, CA 95401, USA'

#%% License
license_ = ('Data in this file produced by <Your Centre Name> is licensed under'
            ' a Creative Commons Attribution-ShareAlike 4.0 International License'
            ' (https://creativecommons.org/licenses/). Use of the data must be'
            ' acknowledged following guidelines found at <a URL maintained by you>.'
            ' Further information about this data, including some limitations,'
            ' can be found via <some URL maintained by you>.)')

#%% Nominal resolution

#%% Product

#%% Realm

#%% Region (taken from http://cfconventions.org/Data/cf-standard-names/docs/standardized-region-names.html)

#%% Required global attributes - # indicates source
required_global_attributes = [
 'Conventions',
 'activity_id',
 'contact',
 'creation_date',
 'data_specs_version',
 'frequency',
 'grid',
 'grid_label',
 'institution',
 'institution_id',
 'license',
 'nominal_resolution',
 'product',
 'realm',
 'source_id',
 'table_id',
 'tracking_id',
 'variable_id',
 'variant_label'
] ;

#%% Source ID
tmp = [['source_id','https://raw.githubusercontent.com/PCMDI/obs4mips-cmor-tables/master/obs4MIPs_source_id.json']
      ] ;
#source_id = readJsonCreateDict(tmp)
#source_id = source_id.get('source_id')

# Enter fixes or additions below
source_id = {}
source_id['source_id'] = {}
key = 'ERA-40'
source_id['source_id'][key] = {}
source_id['source_id'][key]['source_description'] = 'ECMWF - ERA-40 (European ReAnalysis 1957-2002)'
source_id['source_id'][key]['institution_id'] = 'ECMWF'
source_id['source_id'][key]['release_year'] = '2005'
source_id['source_id'][key]['source_id'] = key
source_id['source_id'][key]['source_label'] = 'ECMWF-ERA-40'
source_id['source_id'][key]['source_name'] = 'ECMWF ERA-40'
source_id['source_id'][key]['source_type'] = 'reanalysis'
source_id['source_id'][key]['region'] = ['global']
source_id['source_id'][key]['source_variables'] = ['ta','ua','va']
source_id['source_id'][key]['source_version_number'] = '1.0'

'''
List from https://goo.gl/GySZ56 to be updated
ERA-40/ECMWF
ERA-Interim/ECMWF
JRA-25/MRI
AIRS/
MLS/
CERES/
GPCP/UofMD
TRMM/
RSS/REMSS
ISCCP/
MODIS/
CALIPSO/
WOA13v2/NOAA-NCEI
Hosoda/
IPRC
UCSD
ERSSTv3b
ERSSTv4
ERSSTv5
GISTEMP
HadCRUT4.5
HadISST1.1
HadSST3.1
Kaplan_Extended_V2
CMAP/UofMD
NOC1.1/NOC
OAFluxV3/WHOI
Aquarius/REMSS
SMOS
'''
#==============================================================================
# Example new source_id entry
#key = 'CMSAF-SARAH-2-0'
#source_id['source_id'][key] = {}
#source_id['source_id'][key]['source_description'] = 'Surface solAr RAdiation data set - Heliosat, based on MVIRI/SEVIRI aboard METEOSAT'
#source_id['source_id'][key]['institution_id'] = 'DWD'
#source_id['source_id'][key]['release_year'] = '2017'
#source_id['source_id'][key]['source_id'] = key
#source_id['source_id'][key]['source_label'] = 'CMSAF-SARAH'
#source_id['source_id'][key]['source_name'] = 'CMSAF SARAH'
#source_id['source_id'][key]['source_type'] = 'satellite_retrieval'
#source_id['source_id'][key]['region'] = list('africa','atlantic_ocean','europe')
#source_id['source_id'][key]['source_variables'] = list('rsds')
#source_id['source_id'][key]['source_version_number'] = '2.0'

# Example rename source_id entry
#key = 'CMSAF-SARAH-2-0'
#source_id['source_id'][key] = {}
#source_id['source_id'][key] = source_id['source_id'].pop('CMSAF-SARAH-2.0')

# Example remove source_id entry
#key = 'CMSAF-SARAH-2.0'
#source_id['source_id'].pop(key)

# Test invalid chars
#key = 'CMSAF-SARAH-2 0' ; # Tested ".", “_”, “(“, “)”, “/”, and " "
#source_id['source_id'][key] = {}
#source_id['source_id'][key] = source_id['source_id'].pop('CMSAF-SARAH-2-0')

#%% Source type
source_type = {}
source_type['gridded_insitu'] = 'gridded product based on measurements collected from in-situ instruments'
source_type['reanalysis'] = 'gridded product generated from a model reanalysis based on in-situ instruments and possibly satellite measurements'
source_type['satellite_blended'] = 'gridded product based on both in-situ instruments and satellite measurements'
source_type['satellite_retrieval'] = 'gridded product based on satellite measurements'

#%% Table ID
table_id = [
  'PMPObs_Amon',
  'PMPObs_Lmon',
  'PMPObs_Omon',
  'PMPObs_SImon',
  'PMPObs_fx'
] ;

#%% Validate entries
def entryCheck(entry,search=re.compile(r'[^a-zA-Z0-9-]').search):
    return not bool(search(entry))

# source_id
for key in source_id['source_id'].keys():
    # Validate source_id format
    if not entryCheck(key):
        print 'Invalid source_id format for entry:',key,'- aborting'
        sys.exit()
    # Sort variable entries
    vals = source_id['source_id'][key]['source_variables']
    if not isinstance(vals,list):
        vals = list(vals); vals.sort()
    else:
        vals.sort()
    # Validate source_label format
    val = source_id['source_id'][key]['source_label']
    if not entryCheck(key):
        print 'Invalid source_label format for entry:',key,'- aborting'
        sys.exit()
    # Validate source_type
    val = source_id['source_id'][key]['source_type']
    if val not in source_type:
        print 'Invalid source_type for entry:',key,'- aborting'
        sys.exit()
    # Validate region
    vals = source_id['source_id'][key]['region']
    for val in vals:
        if val not in region['region']:
            print 'Invalid region for entry:',key,'- aborting'
            sys.exit()

#%% Write variables to files
for jsonName in masterTargets:
    # Clean experiment formats
    if jsonName in ['coordinate','grids']: #,'Amon','Lmon','Omon','SImon']:
        dictToClean = eval(jsonName)
        for key, value1 in dictToClean.iteritems():
            for value2 in value1.iteritems():
                string = dictToClean[key][value2[0]]
                if not isinstance(string, list) and not isinstance(string, dict):
                    string = string.strip() ; # Remove trailing whitespace
                    string = string.strip(',.') ; # Remove trailing characters
                    string = string.replace(' + ',' and ')  ; # Replace +
                    string = string.replace(' & ',' and ')  ; # Replace +
                    string = string.replace('   ',' ') ; # Replace '  ', '   '
                    string = string.replace('  ',' ') ; # Replace '  ', '   '
                    string = string.replace('anthro ','anthropogenic ') ; # Replace anthro
                    string = string.replace('decidous','deciduous') ; # Replace decidous
                dictToClean[key][value2[0]] = string
        vars()[jsonName] = dictToClean
    # Write file
    if jsonName in ['Aday', 'Amon', 'Lmon', 'Omon', 'SImon', 'coordinate',
                    'formula_terms', 'fx', 'grids', 'monNobs', 'monStderr']:
        outFile = ''.join(['../Tables/PMPObs_',jsonName,'.json'])
    elif jsonName == 'license_':
        outFile = ''.join(['../PMPObs_license.json'])
    else:
        outFile = ''.join(['../PMPObs_',jsonName,'.json'])
    # Check file exists
    if os.path.exists(outFile):
        print 'File existing, purging:',outFile
        os.remove(outFile)
    if not os.path.exists('../Tables'):
        os.mkdir('../Tables')
    # Create host dictionary
    if jsonName == 'license_':
        jsonDict = {}
        jsonDict[jsonName.replace('_','')] = eval(jsonName)
    elif jsonName not in ['coordinate','formula_terms','fx','grids',
                          'institution_id','source_id','Aday','Amon','Lmon',
                          'Omon','SImon','monNobs','monStderr']:
        jsonDict = {}
        jsonDict[jsonName] = eval(jsonName)
    else:
        jsonDict = eval(jsonName)
    fH = open(outFile,'w')
    json.dump(jsonDict,fH,ensure_ascii=True,sort_keys=True,indent=4,separators=(',',':'),encoding="utf-8")
    fH.close()

del(jsonName,outFile) ; gc.collect()

# Validate - only necessary if files are not written by json module

#%% Generate files for download and use
demoPath = os.path.join('/','/'.join(os.path.realpath(__file__).split('/')[0:-2]),'demo')
outPath = os.path.join(demoPath,'Tables')
if os.path.exists(outPath):
    shutil.rmtree(outPath) ; # Purge all existing
    os.makedirs(outPath)
else:
    os.makedirs(outPath)
os.chdir(demoPath)

# Integrate all controlled vocabularies (CVs) into master file - create obs4MIPs_CV.json
# List all local files
inputJson = ['frequency','grid_label','institution_id','license',
             'nominal_resolution','product','realm','region',
             'required_global_attributes','source_id','source_type','table_id', # These are controlled vocabs
             'coordinate','grids','formula_terms', # These are not controlled vocabs - rather lookup tables for CMOR
             'Amon','Lmon','Omon','SImon','fx' # Update/add if new tables are generated
            ]
tableList = ['Amon', 'Lmon', 'Omon', 'SImon', 'coordinate',
             'formula_terms', 'fx', 'grids']

# Load dictionaries from local files
CVJsonList = copy.deepcopy(inputJson)
CVJsonList.remove('coordinate')
CVJsonList.remove('grids')
CVJsonList.remove('formula_terms')
CVJsonList.remove('Amon')
CVJsonList.remove('Lmon')
CVJsonList.remove('Omon')
CVJsonList.remove('SImon')
CVJsonList.remove('fx')
for count,CV in enumerate(inputJson):
    if CV in tableList:
        path = '../Tables/'
    else:
        path = '../'
    vars()[CV] = json.load(open(''.join([path,'PMPObs_',CV,'.json'])))

# Build CV master dictionary


PMPObs_CV = {}
PMPObs_CV['CV'] = {}
for count,CV in enumerate(CVJsonList):
    # Create source entry from source_id
    if CV == 'source_id':
        source_id_ = source_id['source_id']
        PMPObs_CV['CV']['source_id'] = {}
        for key,values in source_id_.iteritems():
            PMPObs_CV['CV']['source_id'][key] = {}
            string = ''.join([source_id_[key]['source_label'],' ',
                              source_id_[key]['source_version_number'],' (',
                              source_id_[key]['release_year'],'): ',
                              source_id_[key]['source_description']])
            PMPObs_CV['CV']['source_id'][key]['source_label'] = values['source_label']
            PMPObs_CV['CV']['source_id'][key]['source_type'] = values['source_type']
            PMPObs_CV['CV']['source_id'][key]['source_version_number'] = values['source_version_number']
            PMPObs_CV['CV']['source_id'][key]['region'] = ', '.join(str(a) for a in values['region'])
            PMPObs_CV['CV']['source_id'][key]['source'] = string
    # Rewrite table names
    elif CV == 'table_id':
        PMPObs_CV['CV']['table_id'] = []
        for value in table_id['table_id']:
            PMPObs_CV['CV']['table_id'].append(value)
    # Else all other CVs
    elif CV not in tableList:
        PMPObs_CV['CV'].update(eval(CV))
# Add static entries to obs4MIPs_CV.json
PMPObs_CV['CV']['activity_id'] = 'PMPObs'

# Dynamically update "data_specs_version": "2.0.0", in rssSsmiPrw-input.json
#print os.getcwd()
#versionInfo = getGitInfo('../demo/rssSsmiPrw-input.json')
#tagTxt = versionInfo[2]
#tagInd = tagTxt.find('(')
#tagTxt = tagTxt[0:tagInd].replace('latest_tagPoint: ','').strip()

# Write demo PMPObs_CV.json
if os.path.exists('Tables/PMPObs_CV.json'):
    print 'File existing, purging:','PMPObs_CV.json'
    os.remove('Tables/PMPObs_CV.json')
fH = open('Tables/PMPObs_CV.json','w')
json.dump(PMPObs_CV,fH,ensure_ascii=True,sort_keys=True,indent=4,separators=(',',':'),encoding="utf-8")
fH.close()

# Write ../Tables obs4MIPs_CV.json
if os.path.exists('../Tables/PMPObs_CV.json'):
    print 'File existing, purging:','PMPObs_CV.json'
    os.remove('../Tables/PMPObs_CV.json')
fH = open('../Tables/PMPObs_CV.json','w')
json.dump(PMPObs_CV,fH,ensure_ascii=True,sort_keys=True,indent=4,separators=(',',':'),encoding="utf-8")
fH.close()

# Loop and write all other files
os.chdir('Tables')
#tableList.extend(lookupList)
for count,CV in enumerate(tableList):
    outFile = ''.join(['PMPObs_',CV,'.json'])
    if os.path.exists(outFile):
        print 'File existing, purging:',outFile
        os.remove(outFile)
    fH = open(outFile,'w')
    json.dump(eval(CV),fH,ensure_ascii=True,sort_keys=True,indent=4,separators=(',',':'),encoding="utf-8")
    fH.close()

# Cleanup
del(coordinate,count,formula_terms,frequency,grid_label,homePath,institution_id,
    nominal_resolution,PMPObs_CV,product,realm,inputJson,tableList,
    required_global_attributes,table_id)

#%% Generate zip archive
# Add machine local 7za to path - solve for @gleckler1
'''
env7za = os.environ.copy()
if os.environ.get('USER') == 'gleckler1':
    if 'oceanonly' in os.environ.get('HOSTNAME'):
        env7za['PATH'] = env7za['PATH'] + ':/export/durack1/bin/downloads/p7zip9.38.1/150916_build/p7zip_9.38.1/bin'
    elif 'crunchy' in os.environ.get('HOSTNAME'):
        env7za['PATH'] = env7za['PATH'] + ':/export/durack1/bin/downloads/p7zip9.20.1/130123_build/p7zip_9.20.1/bin'
    else:
        print 'No 7za path found'

# Cleanup rogue files
os.chdir(demoPath)
if os.path.exists('.DS_Store'):
    os.remove('.DS_Store')
if os.path.exists('demo.zip'):
    os.remove('demo.zip')
if os.path.exists('demo/demo.zip'):
    os.remove('demo/demo.zip')
if os.path.exists('../demo/demo.zip'):
    os.remove('../demo/demo.zip')
# Jump up one directory
os.chdir(demoPath.replace('/demo',''))
# Zip demo dir
p = subprocess.Popen(['7za','a','demo.zip','demo','tzip','-xr!demo/demo'],
                         stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                         cwd=os.getcwd(),env=env7za)
stdout = p.stdout.read() ; # Use persistent variables for tests below
stderr = p.stderr.read()
# Move to demo dir
shutil.move('demo.zip', 'demo/demo.zip')
'''
