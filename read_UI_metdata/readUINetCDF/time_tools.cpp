#include "UInetcdf_constants.h"
#include "time_tools.h"

#include <iostream>
#include <math.h>
#include <netcdf.h>
#include <sstream>
#include <string>
#include <vector>
int monthdays_normal[13]    = {31,28,31,30,31,30,31,31,30,31,30,31,365};
int monthdays_leap[13]      = {31,29,31,30,31,30,31,31,30,31,30,31,366};
int start_doy_nomal[12]     = {1,32,60,91,121,152,182,213,244,274,305,335};
int start_doy_leap[12]      = {1,32,61,92,122,153,183,214,245,275,306,336};
std::string out_met_varname[] {"ppt","tmax", "tmin","uas","vas",
                               "srad", "rhmax", "rhmin", ""};
std::string output_var_type_name[] {"PPT",
                                    "TAVG",
                                    "TMAX",
                                    "TMIN",
                                    "RHUM",
                                    "RHMAX",
                                    "RHMIN",
                                    "WIND",
                                    "SRAD",
                                    "PT",
                                    "PM",
                                    ""};
#ifdef HISTORICAL_MET
std::string varfile_prefix[] {"pr","tmmx","tmmn","","vs","srad","rmax","rmin",
                              ""};
std::string varname[] {"precipitation_amount","air_temperature",
                       "air_temperature","","wind_speed",
                        "surface_downwelling_shortwave_flux_in_air",
                        "relative_humidity", "relative_humidity", ""};

std::string jc_varname[] {"precipitation_amount",
                            "maximum_air_temperature",
                            "minimum_air_temperature",
                            "wind_speed",
                            "surface_downwelling_shortwave_flux_in_air",
                            "maximum_relative_humidity",
                            "minimum_relative_humidity",
                            "dewpoint_temperature",
                            ""};

//ALL dimentions of the variable:
//After 2015: day, lon, lat
//Before 2014 (including 2014): the dimention is lat, lon, day
//wind & srad: before 2010 (including 2010): day, lat, lon
//      2011-2014: lat, lon, day
//      after 2015: day, lon, lat
//PPT(mm); TMAX,TMIN:(K);
//srad: surface_downwelling_shortwave_flux_in_air(day, lat, lon)  "W m-2"
//relative_humidity(day, lon, lat) "%"
//wind_speed(day, lon, lat) "m/s"
#else
std::string varfile_prefix[] {"pr",
                              "tasmax",
                              "tasmin",
                              "uas",
                              "vas",
                              "rsds",
                              "rhsmax",
                              "rhsmin",
                              ""};
std::string varname[] { "precipitation",
                        "air_temperature",
                        "air_temperature",
                        "eastward_wind",
                        "northward_wind",
                        "surface_downwelling_shortwave_flux_in_air",
                        "relative_humidity",
                        "relative_humidity",
                        ""};
//units: pr: mm; temp: K; wind: m/s; rhum:% rsds: W/m2
std::string gcm_name[] {"bcc-csm1-1",
                        "BNU-ESM",
                        "CanESM2",
                        "CNRM-CM5",
                        "CSIRO-Mk3-6-0",
                        "GFDL-ESM2G",
                        "GFDL-ESM2M",
                        "HadGEM2-CC365",
                        "HadGEM2-ES365",
                        "inmcm4",
                        "IPSL-CM5A-LR",
                        "IPSL-CM5A-MR",
                        "IPSL-CM5B-LR",
                        "MIROC5",
                        "MIROC-ESM-CHEM",
                        "MIROC-ESM",
                        "MRI-CGCM3",
                        ""};
std::string maca_rcps_name[] {"historical",
                              "rcp45",
                              "rcp85",
                              ""};
int maca_rcps_periods[] = {12, 19, 19};
#endif

/****from year,mon,day converted to days since 1900-01-01****/
/****from year,mon,day converted to days since 1900-01-01****/
//leap years
int get_indays_leap_years(const int year,const int mon,const int day){
   //mon:1-12 day:1-31
   int *monthdays;
   int inday = 0;
   if(year<1900) return inday;
   for (int i = 1900; i < year; i++) {
      if(LEAPYR(i)) inday += 366;
      else inday += 365;
   }
   if(LEAPYR(year)) monthdays = monthdays_leap;
   else monthdays = monthdays_normal;
   if (year < 1900 || mon < 1 || mon > 12 || day < 1 || day > monthdays[mon-1]) {
      std::cerr<<"Wrong input date!!!\n";
      exit(0);
   }
   for (int i = 1; i < mon; i++) {
      inday += monthdays[i-1];
   }
   inday += (day-1);
   return inday;
};
//______________________________________________________________________________
int get_start_lat_or_lont(float *lxxt,int ndim,float inlxxt){
  int start = -9999;
  int i;
  bool descending = lxxt[0] > lxxt[1] ? true : false;
  for (i = 0; i < ndim; i++) {
    if ((inlxxt <= lxxt[i] && !descending) || (inlxxt >= lxxt[i] && descending)) {
      start = i-1;
      return (i == 0) ? 0 : start;
    }
  }
  if(start == -9999) return -1;
};
//______________________________________________________________________________
//no leap years
int get_indays(int year,int mon,int day){
    int inday=0;
    int i;
    if(year<1900) return inday;
    for(i=1900;i<year;i++){
        inday += 365;
    }
    monthdays_normal[1] = 28;
    for(i=1;i<mon;i++){
        inday += monthdays_normal[i-1];
    }
    inday += (day-1);
    return inday;
};
//______________________________________________________________________________
void cal_year_day(int days,int *year, int *yearday){
    //days: days since 1900-1-1 from 1

    int syear = 1900;
    while (days > 0) {
        int yrday = LEAPYR(syear) ? 366 : 365;
        days -= yrday;
        syear++;
    }
    *year = syear - 1;
    *yearday = days + (LEAPYR(*year) ? 366 : 365);
}
//______________________________________________________________________________
int get_days_between_year_with_leaps(int start_year, int end_year)
{   //including end_years; if equal, return the days of that year
    int days = 0;
    if (end_year < start_year) std::swap<int>(start_year,end_year);
    for (int year = start_year; year <= end_year; year++) {
        days += LEAPYR(year) ? 366 : 365;
    }
    return days;
}
//______________________________________________________________________________
month get_month(const bool leapyear,const int doy_from_0)
{
    int *p;
    int doy = doy_from_0 + 1;
    month month_index = JAN;
    if (leapyear) p = start_doy_leap;
    else          p = start_doy_nomal;
    if (doy >= p[JAN] && doy <= (p[FEB] - 1)) month_index = JAN;
    else if (doy >= p[FEB] && doy <= (p[MAR] - 1)) month_index = FEB;
    else if (doy >= p[MAR] && doy <= (p[APR] - 1)) month_index = MAR;
    else if (doy >= p[APR] && doy <= (p[MAY] - 1)) month_index = APR;
    else if (doy >= p[MAY] && doy <= (p[JUN] - 1)) month_index = MAY;
    else if (doy >= p[JUN] && doy <= (p[JUL] - 1)) month_index = JUN;
    else if (doy >= p[JUL] && doy <= (p[AUG] - 1)) month_index = JUL;
    else if (doy >= p[AUG] && doy <= (p[SEP] - 1)) month_index = AUG;
    else if (doy >= p[SEP] && doy <= (p[OCT] - 1)) month_index = SEP;
    else if (doy >= p[OCT] && doy <= (p[NOV] - 1)) month_index = OCT;
    else if (doy >= p[NOV] && doy <= (p[DEC] - 1)) month_index = NOV;
    else month_index = DEC;
    return month_index;
}
//______________________________________________________________________________
season get_season(const bool leapyear,const int doy)
{

}
//______________________________________________________________________________
#ifdef HISTORICAL_MET
std::string get_historical_netcdf_file_name(const std::string prefix,
  const int var_type, const int year)
{
    std::stringstream ss;
    ss << prefix << varfile_prefix[var_type] << "_" << year << ".nc";
    return ss.str();
}
#else
std::string get_maca_netcdf_file_name(const std::string prefix,
  const int var_type, const int gcm_model_index, const int rcp_index,
  const int start_year, const int end_year)
{
    std::stringstream ss;
    ss << prefix
       << "macav2metdata_"
       << varfile_prefix[var_type]
       << "_"
       << gcm_name[gcm_model_index]
       << "_r1i1p1_"
       << maca_rcps_name[rcp_index]
       << "_"
       << start_year
       << "_"
       << end_year
       << "_CONUS_daily.nc";
    return ss.str();
}
#endif
//______________________________________________________________________________
int get_index_from_dimension_var(const int ncid, const char* dim_name,
  const size_t dim_size, const double target, float *f, double *d)
{
    nc_type dimtype;
    int retval, var_id, index;
    if (retval = nc_inq_varid(ncid,dim_name,&var_id))   ERR(retval);
    if (retval = nc_inq_var(ncid,var_id,NULL,&dimtype,NULL,NULL,NULL))
                                                         ERR(retval);
    //float *f;
    //double *d;
    if (dimtype == NC_FLOAT) {
        //f = (float *) malloc(dim_size * sizeof(float));
        if ((retval = nc_get_var_float(ncid, var_id, &f[0]))) ERR(retval);
        float tol = fabs(f[0] - f[1]) / 2.0;
        index = find_closest_index_from_sorted_array<float>(f,(float)target,dim_size,
                                                            tol);
        //free(f);
    } else if (dimtype == NC_DOUBLE) {
        //d = (double *) malloc(dim_size * sizeof(double));
        if ((retval = nc_get_var_double(ncid, var_id, &d[0]))) ERR(retval);
        double tol = fabs(d[0] - d[1]) / 2.0;
        index = find_closest_index_from_sorted_array<double>(d,target,
                      dim_size, tol);
        //free(d);
    }
    return index;
}
//______________________________________________________________________________
bool get_data_from_UI_netcdf(const std::string ncfilename, const int var_type,
  const double lat, const double lon, int& start_day, int& end_day,
  double *data, float *f, double *d, float *fdim, double *ddim)
{   //lon: -180 - 180
    int retval,ncid,daysid,latid,lontid,varid;
    size_t recs_days,nlat,nlont;
    if((retval = nc_open(ncfilename.c_str(), NC_NOWRITE, &ncid)))
        ERR(retval);
    if (retval = nc_inq_dimid(ncid,NDAYS_NAME,&daysid))      ERR(retval);
    if (retval = nc_inq_dimlen(ncid,daysid,&recs_days))      ERR(retval);
    if (retval = nc_inq_dimid(ncid,NLAT_NAME,&latid))        ERR(retval);
    if (retval = nc_inq_dimlen(ncid,latid,&nlat))            ERR(retval);
    if (retval = nc_inq_dimid(ncid,NLONT_NAME,&lontid))      ERR(retval);
    if (retval = nc_inq_dimlen(ncid,lontid,&nlont))          ERR(retval);
    int day_var_id,var_var_id;
    //get lat and lon index
    int lat_index = get_index_from_dimension_var(ncid,NLAT_NAME,nlat,lat,
                                                 fdim,ddim);
    //lon
    double adjlon =
#ifdef HISTORICAL_MET
            lon;
#else
            lon < 0 ? (360 + lon) : lon;
#endif
    int lon_index = get_index_from_dimension_var(ncid,NLONT_NAME,nlont,adjlon,
                                                 fdim, ddim);
    if (lat_index == -1 || lon_index == -1) {
        return false;
    }
    //get day dimition information
    if (retval = nc_inq_varid(ncid,NDAYS_NAME,&day_var_id))   ERR(retval);
    float *day_var = (float *) malloc(recs_days * sizeof(float));
    if ((retval = nc_get_var_float(ncid, day_var_id, &day_var[0]))) ERR(retval);
    start_day = (int)day_var[0];
    end_day = (int)day_var[recs_days - 1];
    free(day_var);
    //get var information
    if (retval = nc_inq_varid(ncid,varname[var_type].c_str(),&var_var_id))
        ERR(retval);
    int var_dim_id[3];
    size_t start[3];
    size_t count[3];
    var_dimention_type var_dim_type;
    if (retval = nc_inq_vardimid(ncid,var_var_id,var_dim_id)) ERR(retval);
    if (var_dim_id[0] == latid && var_dim_id[1] == lontid
        && var_dim_id[2] == daysid) {
        var_dim_type = LAT_LON_DAY;
        start[0] = lat_index;
        start[1] = lon_index;
        start[2] = 0;
        count[0] = 1;
        count[1] = 1;
        count[2] = recs_days;
    } else if (var_dim_id[0] == daysid && var_dim_id[1] == latid
               && var_dim_id[2] == lontid) {
        var_dim_type = DAY_LAT_LON;
        start[0] = 0;
        start[1] = lat_index;
        start[2] = lon_index;
        count[0] = recs_days;
        count[1] = 1;
        count[2] = 1;
    } else if (var_dim_id[0] == daysid && var_dim_id[1] == lontid
               && var_dim_id[2] == latid) {
        var_dim_type = DAY_LON_LAT;
        start[0] = 0;
        start[1] = lon_index;
        start[2] = lat_index;
        count[0] = recs_days;
        count[1] = 1;
        count[2] = 1;

    } else {
        std::cerr << "ERROR: the variable dimentions are not identified!\n";
        exit(0);
    }

    //read data
    nc_type tvar_type;
    if (retval = nc_inq_vartype(ncid,var_var_id,&tvar_type)) ERR(retval);
    //float *f;
    //double *d;
    if (tvar_type == NC_FLOAT) {
        //f = (float *) malloc(recs_days * sizeof(float));
        if (retval = nc_get_vara_float(ncid,var_var_id,start,count,f))
            ERR(retval);
        for (int i = 0; i < recs_days; i++)
            data[i] = (double)f[i];
        //free(f);
    } else if (tvar_type == NC_DOUBLE) {
        //d = (double *) malloc(recs_days * sizeof(double));
        if (retval = nc_get_vara_double(ncid,var_var_id,start,count,d))
            ERR(retval);
        for (int i = 0; i < recs_days; i++)
            data[i] = d[i];
        //free(d);
    }
    nc_close(ncid);
    return true;
}
//______________________________________________________________________________
var_name get_global_var_name(const int var_index)
{
    var_name global_var_name;
#ifdef HISTORICAL_MET
    switch (var_index) {
        case his_PPT:
            global_var_name = PPT;
            break;
        case his_TMAX:
            global_var_name = TMAX;
            break;
        case his_TMIN:
            global_var_name = TMIN;
            break;
        case his_VAS:
            global_var_name = VAS;
            break;
        case his_SRAD:
            global_var_name = SRAD;
            break;
        case his_RHMAX:
            global_var_name = RHMAX;
            break;
        case his_RHMIN:
            global_var_name = RHMIN;
            break;
        default:
            std::cerr << "cannot find var_index!\n";
    }
#else
    switch (var_index) {
        case fut_PPT:
            global_var_name = PPT;
            break;
        case fut_TMAX:
            global_var_name = TMAX;
            break;
        case fut_TMIN:
            global_var_name = TMIN;
            break;
        case fut_UAS:
            global_var_name = UAS;
            break;
        case fut_VAS:
            global_var_name = VAS;
            break;
        case fut_SRAD:
            global_var_name = SRAD;
            break;
        case fut_RHMAX:
            global_var_name = RHMAX;
            break;
        case fut_RHMIN:
            global_var_name = RHMIN;
            break;
        default:
            std::cerr << "cannot find var_index!\n";
    }
#endif
    return global_var_name;
}
//______________________________________________________________________________
#ifndef HISTORICAL_MET
int get_maca_period_start_year(const int period_index, const int rcp_type_index)
{
    if (rcp_type_index != historical) {
        return period_index * 5 + 2006;
    } else {
        if (period_index != (maca_rcps_periods[historical] - 1))
            return period_index * 5 + 1950;
        else
            return 2005;
    }
}
//______________________________________________________________________________
int get_maca_period_end_year(const int period_index, const int rcp_type_index)
{
    int start_year = get_maca_period_start_year(period_index,rcp_type_index);
    int end_year = start_year + 4;
    if (rcp_type_index == historical
        && period_index == (maca_rcps_periods[historical] - 1))
        end_year = 2005;
    else if (start_year == 2096)
        end_year = 2099;
    return end_year;
}
//______________________________________________________________________________
int get_gcm_model_index(std::string gcm_model_name)
{
    for (int i = bcc_csm1_1; i < gcm_model_counts; i++) {
        if (gcm_name[i].compare(gcm_model_name) == 0) {
            return i;
        }
    }
    return -1;
}
//______________________________________________________________________________
int get_maca_rcp_index(std::string rcp_name)
{
    for (int i = historical; i < maca_rcps_counts; i++) {
        if (maca_rcps_name[i].compare(rcp_name) == 0) {
            return i;
        }
    }
    return -1;
}
#endif
