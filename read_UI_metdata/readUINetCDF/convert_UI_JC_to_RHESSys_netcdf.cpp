#include "et_functions.h"
#include "esrigridclass.h"
#include "time_tools.h"
#include "UInetcdf_constants.h"
#include "adj_met.h"
#include <iostream>
#include <fstream>
#include <math.h>
#include <sstream>
#include <time.h>
#include <omp.h>
#include <netcdf.h>

#define MAX_DIM 1500
#define OUT_TIME_NAME "time"
#define OUT_LAT_NAME "lat"
#define OUT_LONT_NAME "lon"

#define NDAYS_NAME "day"
#define NLAT_NAME "lat"
#define NLONT_NAME "lon"
#define UNITS "units"
#define DESCRIPTION "description"

#define ESRI_PE_STRING "esri_pe_string"
#define COORDINATES "coordinates"
const int LATS = 24;
const int LONS = 24;
const int DAYS = 43070;

int get_index_from_rec(int rec_index, int &dayindex, int &latindex, int &lonindex);
int main(int argc, char *argv[])
{
    std::cout << "Start...\n";
    time_t _tm = time(NULL );
    struct tm * curtime = localtime ( &_tm );
    std::cout << "current time: " << asctime(curtime) << std::endl;

    //data[var][year][day]
    if (argc < 3) {
        std::cerr << "Usage: " << argv[0]
                  << " [start_year] "
                  << " [end_year] "
                  << " [output_file_name] "
                  << std::endl;
        exit(0);
    }
    int start_year  = atoi(argv[1]);
    int end_year    = atoi(argv[2]);
    std::string output_file_name(argv[3]);
    int vars = jc_his_VAR_COUNTS;                                                                   //pr,tmmx,tmmn,rmax,rmin,srad,vs
    int years = end_year - start_year + 1;
    int days = 366;
    const int OUT_DAYS = get_days_between_year_with_leaps(start_year,end_year);


    const long total_rec = LATS * LONS * DAYS;
    const long real_out_total_rec = LATS * LONS * OUT_DAYS;
    //int total_days = years * days;
    double cellsize = 1.0/24.0;

#ifdef CHECK_WITH_GIS
    EsriGridClass<float> grid[jc_his_VAR_COUNTS];
    for (int var = jc_his_PPT; var < jc_his_VAR_COUNTS; var++) {
        grid[var].setNcols(LONS);
        grid[var].setNrows(LATS);
        grid[var].setCellsize(cellsize);
        grid[var].setNodataValue(-9999.0);
        grid[var].setXll(-115.980496724447 - 0.5*cellsize);
        grid[var].setYll(44.0210227966309 - 0.5*cellsize);
        grid[var].AllocateMem();
    }
#endif
  double *lat        = alloc_1d_array<double>(LATS,"lat");
  double *lon        = alloc_1d_array<double>(LONS,"lon");
  float *aday         = alloc_1d_array<float>(DAYS,"aday");
  //double ***data    = alloc_3d_array<double>(vars,years,days,"data");
  //double *average   = alloc_1d_array<double>(vars,"average");
  float *f           = alloc_1d_array<float>(LATS * LONS * DAYS,"f");
  float *out_f           = alloc_1d_array<float>(LATS * LONS * DAYS,"f");
  float *ftmax           = alloc_1d_array<float>(LATS * LONS * DAYS,"ftmax");
  float *ftmin           = alloc_1d_array<float>(LATS * LONS * DAYS,"ftmin");

  float *out_aday         = alloc_1d_array<float>(OUT_DAYS,"aday");
  float *out_f_real       = alloc_1d_array<float>(LATS * LONS * OUT_DAYS,"out_f");
  //float *fmax      = alloc_1d_array<float>(LATS * LONS * DAYS,"f");

  float *out_lat  = alloc_1d_array<float>(LATS,"lat");
  float *out_lon  = alloc_1d_array<float>(LONS,"lon");


  //for (int var = jc_his_PPT; var < jc_his_VAR_COUNTS; var++) {
  //    average[var] = 0.0;
  //}

  std::string ncfilename("test1.nc");
  int retval,ncid,daysid,latid,lonid,varid;
  size_t recs_days,nlat,nlont;
  if((retval = nc_open(ncfilename.c_str(), NC_NOWRITE, &ncid)))
      ERR(retval);
  size_t start[3];
  size_t count[3];

  if (retval = nc_inq_varid(ncid,"lat",&latid))   ERR(retval);
  if (retval = nc_inq_varid(ncid,"lon",&lonid))   ERR(retval);
  if (retval = nc_inq_varid(ncid,"day",&daysid))  ERR(retval);
  if ((retval = nc_get_var_double(ncid, latid, &lat[0]))) ERR(retval);
  if ((retval = nc_get_var_double(ncid, lonid, &lon[0]))) ERR(retval);
  if ((retval = nc_get_var_float(ncid, daysid,  &aday[0]))) ERR(retval);

 for (int ilat = 0; ilat < LATS; ilat++) out_lat[ilat] = (double)lat[ilat];
 for (int ilon = 0; ilon < LONS; ilon++) out_lon[ilon] = (double)lon[ilon];
 for (int i = 0; i < OUT_DAYS; i++) {
     out_aday[i] = (float)(i+1);
     //int year,yearday;
     //cal_year_day(out_aday[i],&year, &yearday);
     //std::clog << out_aday[i] << "\t" << year << "\t" << yearday << std::endl;
 }

  //output information
  enum out_var{PPT,TMAX,TMIN,WIND,SPH,SRAD,RMAX,RMIN,var_counts};
  std::string outvarname[] {"PPT","TMAX","TMIN","WIND","SPH","SRAD","RMAX","RMIN"};
  std::string varfile_prefix[] {"pr","tmmx","tmmn","vs","sph","srad","rmax","rmin"};
  std::string varname[] {"precipitation_amount","air_temperature","air_temperature","wind_speed","specific_humidity","surface_downwelling_shortwave_flux_in_air","relative_humidity","relative_humidity"};

  std::string out_varfile_prefix[] {"pr","tasmax","tasmin","was","huss","rsds","rmax","rmin"};
  std::string out_varname[] {"precipitation_flux","air_temperature","air_temperature","wind_speed","specific_humidity","surface_downwelling_shortwave_flux_in_air","relative_humidity","relative_humidity"};
  std::string out_varunit[] {"kg m-2 s-1","K","K","m s-1","kg/kg","W m-2","%","%"};
  std::string out_varheight[] {"","2 m","2 m","10 m","2 m","","2 m","2 m"};
  std::string out_var_description[] {"Daily Accumulated Precipitation",
                                         "Daily Maximum Temperature",
                                         "Daily Minimum Temperature",
                                         "Daily Mean Wind Speed",
                                         "Daily mean specific humidity",
                                         "Daily Mean downward shortwave radiation at surface",
                                         "Daily Maximum Relative Humidity",
                                         "Daily Minimum Relative Humidity"};


  std::string unit_days = "days since 1900-01-01 00:00:00";
  std::string descript_days = "days since 1900-01-01";
  int days_unit_attlen = unit_days.length();
  int days_descript_attlen = descript_days.length();
  std::string unit_lat = "degrees_north";
  std::string descript_lat = "Latitude of the center of the grid cell";
  int lat_unit_attlen = unit_lat.length();
  int lat_descript_attlen = descript_lat.length();
  std::string unit_lont = "degrees_east";
  std::string descript_lont = "Longitude of the center of the grid cell";
  int lont_unit_attlen = unit_lont.length();
  int lont_descript_attlen = descript_lont.length();
  std::string descript_esri_pe_string = "GEOGCS[\\\"GCS_WGS_1984\\\",DATUM[\\\"D_WGS_1984\\\",SPHEROID[\\\"WGS_1984\\\",6378137.0,298.257223563]],PRIMEM[\\\"Greenwich\\\",0.0],UNIT[\\\"Degree\\\",0.0174532925199433]]";
  int data_esri_attlen = descript_esri_pe_string.length();
  std::string descript_coordinates = "lon lat";
  int data_coordinates_attlen = descript_coordinates.length();

  std::string calnendar = "gregorian";
  std::string author = "John Abatzoglou - University of Idaho, jabatzoglou@uidaho.edu";
  std::string date_out = "19 March 2018";
  std::string note1 = "The projection information for this file is: GCS WGS 1984.";
  std::string note2 = "Citation: Abatzoglou, J.T., 2012, Development of gridded surface meteorological data for ecological applications and modeling, International Journal of Climatology, DOI: 10.1002/joc.3413";
  time_t t = time(0);
  struct tm * now = localtime(&t);
  std::string timeinfo(asctime(now));
#ifdef REMOVE_HUMAN_EFFECT
  std::string note3 = "Removed human's effect by Mingliang Liu mingliang.liu@wsu.edu on" + timeinfo;
#else
  std::string note3 = "Reformatted into RHESSys NetCDF format by Mingliang Liu mingliang.liu@wsu.edu on" + timeinfo;
#endif
  int dimids[3];
  //
#ifdef REMOVE_HUMAN_EFFECT
  Adj_records *adjdata = (Adj_record *) malloc(DISTURB_YEARS * 12
                                               * sizeof(Adj_record));
  std::string delta_file_name("johnsoncreek_delta.csv");
  read_disturb_data(delta_file_name,adjdata);
#endif

  //get day dimition information
  for (int var = jc_his_PPT; var < jc_his_VAR_COUNTS; var++) {
      if (retval = nc_inq_varid(ncid,jc_varname[var].c_str(),&varid))   ERR(retval);
      if ((retval = nc_get_var_float(ncid, varid, &f[0]))) ERR(retval);
      if (var == jc_his_TMAX)
          if ((retval = nc_get_var_float(ncid, varid, &ftmax[0]))) ERR(retval);
      if (var == jc_his_TMIN)
          if ((retval = nc_get_var_float(ncid, varid, &ftmin[0]))) ERR(retval);
#ifdef CHECK_WITH_GIS
      for (int lat = 0; lat < LATS; lat++) {
          for (int lon = 0; lon < LONS; lon++) {
            grid[var].setValue(lat,lon,0);
          }
      }
#endif

      for (long rec = 0; rec < real_out_total_rec; rec++) {
          out_f_real[rec] = -9999.0;
      }

      for (long rec = 0; rec < total_rec; rec++) {
          int day_idx,lat_idx,lon_idx;
          get_index_from_rec(rec,day_idx,lat_idx,lon_idx);                        //index from original day dim
          int day_index = aday[day_idx] - 1;                                      //day from 1900 (from 0)

          long out_rec = day_index * LONS * LATS + lat_idx * LONS + lon_idx;
          //long formerday_out_rec = (day_index - 1) * LONS * LATS + lat_idx * LONS + lon_idx;

          int year,yearday,month;
          cal_year_day(day_index + 1,&year,&yearday);                            //yearday: 1-365/366
          month = get_month(true,yearday-1);

#ifdef REMOVE_HUMAN_EFFECT
           double delta;
           int index = (year - START_YEAR) * 12 + month;
           switch(var) {
             case jc_his_PPT   : delta = adjdata[index].ppt;   break;
             case jc_his_TMAX  : delta = adjdata[index].tmax;  break;
             case jc_his_TMIN  : delta = adjdata[index].tmin;  break;
             case jc_his_VAS   : delta = adjdata[index].wind;  break;
             case jc_his_TDEW  : delta = adjdata[index].sph;   break;
             case jc_his_SRAD  : delta = adjdata[index].srad;  break;
             case jc_his_RHMAX : delta = adjdata[index].rmax;  break;
             case jc_his_RHMIN : delta = adjdata[index].rmin;  break;
           }
#endif
        if (var == jc_his_PPT) {
            out_f[rec] = f[rec] / 24.0 / 3600.0;              //mm/day -> kg/m2/s
        } else if (var == jc_his_TDEW) {
            double tdew = f[rec] - 273.15;                                       //Celsius degree
            double vp = calc_SatVP(tdew);                                        //(kPa)
            double tavg = (ftmax[rec] + ftmin[rec]) * 0.5;                       //(K)
            double p_g_m3 = 2165.0 * vp / tavg;                                  //(g/m3) http://biomet.ucdavis.edu/conversions/HumCon.htm
            double airdensity = 101325.0 / (287.05 * tavg) * 1000.0;             //(g/m3) https://www.brisbanehotairballooning.com.au/calculate-air-density/
            out_f[rec] = p_g_m3 / airdensity;
        } else {
            out_f[rec] = f[rec];
        }
#ifdef REMOVE_HUMAN_EFFECT
        if (var == jc_his_PPT || var == jc_his_TDEW)
            out_f[rec] -= out_f[rec] * delta;
        else out_f[rec] -= delta;

        if (var == jc_his_VAS || var == jc_his_TDEW || var == jc_his_RHMAX || var == jc_his_RHMIN)
        {
            if (out_f[rec] < 0) out_f[rec] = 0;
        }

        if (var == jc_his_RHMAX || var == jc_his_RHMIN)
        {
            if (out_f[rec] > 100.0) out_f[rec] = 100.0;
        }
#endif

        //check leap year day
        out_f_real[out_rec] = out_f[rec];

        //if (LEAPYR(year) && yearday == 61)                                       //the Feb. 29 in leap year
        //{
        //    if (var == jc_his_PPT) out_f_real[formerday_out_rec] = 0;
        //    else out_f_real[formerday_out_rec] = out_f_real[out_rec];
        //}
        if (lat_idx == 1 && lon_idx == 1) {
        std::cerr << "\t"            << jc_varname[var]
                  << "\trec:"        << rec
                  << "\tout_rec:"    << out_rec
                  << "\tdf_1900:"    << (day_index+1)
                  << "\tyear:"       << year
                  << "\tmon:"        << (month+1)
                  << "\tday_of_year:"<< yearday
#ifdef REMOVE_HUMAN_EFFECT
                  << "\tadj:"        << delta
#endif
                  << "\tout_f:"      << out_f[rec]
                  << "\tout_f_real:" << out_f_real[out_rec]
                  << std::endl;
        }
        //if(lat_idx == 1 && lon_idx == 1)
        //    std::clog << "finished rec:" << rec << std::endl;
      } //rec

      for (long rec = 0; rec < real_out_total_rec; rec++) {
          if(out_f_real[rec] <= -9998.0) {
              long f_rec = rec - LONS * LATS;
              if (var == jc_his_PPT) out_f_real[rec] = 0;
              else out_f_real[rec] = out_f_real[f_rec];
          }
          if(out_f_real[rec] <= -9998.0) {
          std::cerr << "rec:" << rec << "\tvalue:" << out_f_real[rec] << std::endl;
          exit(1);
          }
      }

#ifdef CHECK_WITH_GIS
      for (int ilat = 0; ilat < LATS; ilat++) {
          for (int ilon = 0; ilon < LONS; ilon++) {
              double tt = grid[var].getValue(ilat,ilon) / (double)DAYS;
              if (var == jc_his_TDEW || var == jc_his_TMAX || var == jc_his_TMIN)
                  tt -= 273.15;
              grid[var].setValue(ilat,ilon,tt);
          }
      }
#endif

      out_var outvar_idx;
      switch(var) {
        case jc_his_PPT: outvar_idx = PPT;     break;
        case jc_his_TMAX  : outvar_idx = TMAX; break;
        case jc_his_TMIN  : outvar_idx = TMIN; break;
        case jc_his_VAS   : outvar_idx = WIND; break;
        case jc_his_TDEW  : outvar_idx = SPH;  break;
        case jc_his_SRAD  : outvar_idx = SRAD; break;
        case jc_his_RHMAX : outvar_idx = RMAX; break;
        case jc_his_RHMIN : outvar_idx = RMIN; break;
      }


      int ndaysid,nlatid,nlontid,dayid,dataid,outncid;
      int outlatid,outlonid;
      std::stringstream ss;
      ss<<output_file_name<<"RHESSys_NetCDF_"<<out_varfile_prefix[outvar_idx]<<"_daily_UI_historical_"<<start_year<<"_"<<end_year<<"_JC.nc";
      if ((retval = nc_create(ss.str().c_str(), NC_CLOBBER, &outncid)))
                       ERR(retval);
      if ((retval = nc_def_dim(outncid, OUT_TIME_NAME, OUT_DAYS, &ndaysid)))
              ERR(retval);
      if ((retval = nc_def_dim(outncid, OUT_LAT_NAME, LATS, &nlatid)))
              ERR(retval);
      if ((retval = nc_def_dim(outncid, OUT_LONT_NAME, LONS, &nlontid)))
              ERR(retval);

      if ((retval = nc_def_var(outncid, OUT_TIME_NAME, NC_FLOAT, 1, &ndaysid,&dayid)))
              ERR(retval);
      if ((retval = nc_def_var(outncid, OUT_LAT_NAME, NC_FLOAT, 1, &nlatid,&outlatid)))
              ERR(retval);
      if ((retval = nc_def_var(outncid, OUT_LONT_NAME, NC_FLOAT, 1, &nlontid, &outlonid)))
              ERR(retval);

       /* Assign units attributes to coordinate variables. */

       if ((retval = nc_put_att_text(outncid, dayid, UNITS, days_unit_attlen,unit_days.c_str())))
               ERR(retval);
       if ((retval = nc_put_att_text(outncid, dayid, "calendar", calnendar.length(), calnendar.c_str())))
               ERR(retval);
       if ((retval = nc_put_att_text(outncid, outlatid, UNITS, lat_unit_attlen, unit_lat.c_str())))
               ERR(retval);
       if ((retval = nc_put_att_text(outncid, outlonid, UNITS, lont_unit_attlen, unit_lont.c_str())))
               ERR(retval);
       if ((retval = nc_put_att_text(outncid, dayid, DESCRIPTION, days_descript_attlen, descript_days.c_str())))
               ERR(retval);

       if ((retval = nc_put_att_text(outncid, outlatid, DESCRIPTION, lat_descript_attlen, descript_lat.c_str())))
               ERR(retval);
       if ((retval = nc_put_att_text(outncid, outlonid, DESCRIPTION, lont_descript_attlen, descript_lont.c_str())))
               ERR(retval);

       dimids[0] = ndaysid;
       dimids[1] = nlatid;
       dimids[2] = nlontid;
       float fill = -9999.0;
       if ((retval = nc_def_var(outncid, out_varname[outvar_idx].c_str(), NC_FLOAT, 3, dimids, &dataid)))
               ERR(retval);
       if ((retval = nc_put_att_text(outncid, dataid, UNITS, out_varunit[outvar_idx].length(), out_varunit[outvar_idx].c_str())))
               ERR(retval);
       if ((retval = nc_put_att_text(outncid, dataid, DESCRIPTION,out_var_description[outvar_idx].length(),out_var_description[outvar_idx].c_str())))
               ERR(retval);
       if ((retval = nc_put_att_float(outncid, dataid, "_FillValue", NC_FLOAT, 1, &fill)))
               ERR(retval);
       if ((retval = nc_put_att_text(outncid, dataid, ESRI_PE_STRING, data_esri_attlen, descript_esri_pe_string.c_str())))
               ERR(retval);
       if ((retval = nc_put_att_text(outncid, dataid, COORDINATES, data_coordinates_attlen, descript_coordinates.c_str())))
               ERR(retval);
       if (outvar_idx != PPT && outvar_idx != SRAD) {
         if ((retval = nc_put_att_text(outncid, dataid, "height", out_varheight[outvar_idx].length(),out_varheight[outvar_idx].c_str())))
                 ERR(retval);
       }
       if ((retval = nc_put_att_float(outncid, dataid, "missing_value", NC_FLOAT, 1, &fill)))
               ERR(retval);


       if ((retval = nc_put_att_text(outncid, NC_GLOBAL, "author", author.length(), author.c_str())))
               ERR(retval);
       if ((retval = nc_put_att_text(outncid, NC_GLOBAL, "date", date_out.length(), date_out.c_str())))
               ERR(retval);
       if ((retval = nc_put_att_text(outncid, NC_GLOBAL, "note1", note1.length(), note1.c_str())))
               ERR(retval);
       if ((retval = nc_put_att_text(outncid, NC_GLOBAL, "note2", note2.length(), note2.c_str())))
               ERR(retval);
       if ((retval = nc_put_att_text(outncid, NC_GLOBAL, "note3", note3.length(), note3.c_str())))
               ERR(retval);

       /* End define mode. */
       if ((retval = nc_enddef(outncid)))
               ERR(retval);

       if ((retval = nc_put_var_float(outncid, dayid, &out_aday[0])))
               ERR(retval);
       if ((retval = nc_put_var_float(outncid, outlatid, &out_lat[0])))
               ERR(retval);
       if ((retval = nc_put_var_float(outncid, outlonid, &out_lon[0])))
               ERR(retval);

       if ((retval = nc_put_var_float(outncid, dataid, &out_f_real[0])))
               ERR(retval);
       if ((retval = nc_close(outncid)))
               ERR(retval);
       printf("*** SUCCESS writing subset file %s!\n", ss.str().c_str());
  } //var
  nc_close(ncid);
#ifdef CHECK_WITH_GIS
  for (int var = jc_his_PPT; var < jc_his_VAR_COUNTS; var++) {
      grid[var].writeAsciiGridFile(jc_varname[var] + "_grid.asc");
  }
#endif
    //Print out daily met data
#ifdef PRINT_DAILY_MET
    for (int var = 0; var < vars; var++) {
        var_name global_var_name = get_global_var_name(var);
        if (global_var_name != UAS && global_var_name != VAS) {
        for (int year = start_year; year <= end_year; year++) {
            bool leap_year = LEAPYR(year);
            int days = leap_year ? 366 : 365;
            for (int day = 0; day < days; day++) {
                double outvalue = data[var][year-start_year][day];
                outf << lat     << "\t"
                     << lon     << "\t"
                     << year    << "\t"
                     << "\t"
                     << day     << "\t"
                     << out_met_varname[global_var_name] << "\t"
                     << outvalue
                     << std::endl;
            } //day
        } //year
        } //if
    } //var
#endif
    //delete_3d_array(data,vars,years);
    delete_1d_array(f);
    delete_1d_array(ftmax);
    delete_1d_array(ftmin);
    delete_1d_array(out_f);
    delete_1d_array(lat);
    delete_1d_array(lon);
    delete_1d_array(aday);

    delete_1d_array(out_lat);
    delete_1d_array(out_lon);
    delete_1d_array(out_aday);
    delete_1d_array(out_f_real);
#ifdef REMOVE_HUMAN_EFFECT
    free(adjdata);
#endif
    curtime = localtime ( &_tm );
    std::cout << "Finished @ " << asctime(curtime) << std::endl;

    return 0;
}
//get day,lat,lon  total rec to day index (from 0)
int get_index_from_rec(int rec_index, int &dayindex, int &latindex, int &lonindex)
{
    div_t divres;
    divres = div(rec_index,LATS * LONS);
    dayindex = divres.quot;
    div_t t2;
    t2 = div(divres.rem, LONS);
    latindex = t2.quot;
    lonindex = t2.rem;
    return 0;
}
