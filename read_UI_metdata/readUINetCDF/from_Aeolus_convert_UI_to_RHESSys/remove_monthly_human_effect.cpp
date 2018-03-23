/************************
Convert netcdf data from 1/24 degree to RHESSys ascii format.
Mingliang Liu
02/20/2015
*************************/

//Four variables ppt,tmax,tmin,wind
//unsigned short, signed short, signed short, signed short
#define VIC_CLASSICAL
#include "time_tools.h"
#include "adj_met.h"
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netcdf.h>
#include <math.h>
#include <vector>
#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#define NDAYS_NAME "day"
#define NLAT_NAME "lat"
#define NLONT_NAME "lon"

#define OUT_TIME_NAME "time"
#define OUT_LAT_NAME "lat"
#define OUT_LONT_NAME "lon"

//#define PART1

#define UNITS "units"
#define DESCRIPTION "description"

#define ESRI_PE_STRING "esri_pe_string"
#define COORDINATES "coordinates"

/* Handle errors by printing an error message and exiting with a
 * non-zero status. */
#define ERR(e) {printf("Error: %s\n", nc_strerror(e)); return 2;}

#ifndef _LEAPYR
#define LEAPYR(y) (!((y)%400) || (!((y)%4) && ((y)%100)))
#endif

//using namespace std;
enum var_dimention_type {LAT_LON_DAY,
                         DAY_LAT_LON,
                         DAY_LON_LAT,
                         VAR_DIMENTION_TYPE_COUNTS};
int monthdays[12]={31,28,31,30,31,30,31,31,30,31,30,31};
void add_valid_value(const double add_value, const double invalid_value,double &target, long &count);
/****from year,mon,day converted to days since 1900-01-01****/ 
//no leap years
int get_indays(int year,int mon,int day){
    int inday=0;
    int i;
    if(year<1900) return inday;
    for(i=1900;i<year;i++){
        //if(LEAPYR(i)) inday += 366;
        //else inday += 365;
        inday += 365;
    }
    //if(LEAPYR(year)) monthdays[1] = 29;
    //else monthdays[1] = 28;
    monthdays[1] = 28;

    for(i=1;i<mon;i++){
        inday += monthdays[i-1];
    }
    inday += (day-1); 
    return inday;
};

void cal_year_day(int days,int *year, int *yearday){
    //days: days since 1900-1-1
    div_t divres;
    divres = div(days,365);
    *year = divres.quot + 1900;
    *yearday = divres.rem;
} 

/***Get the start number of lat in netcdf***/
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



int get_days_since_1900(const int yday_from_0,const int year) {
  int start = 0;
  for (int yr = 1900; yr < year; ++yr) {
    if (LEAPYR(yr)) start += 366;
    else start += 365;
  }
  return start + yday_from_0;
}
struct point{
    int row;
    int col;
};

int get_index_from_array(const float target, const float *data, const int ndim) {
  int index = -1;
  for (int i = 0; i < ndim; i++) {
    if (fabs(target-data[i]) <= 1.0e-8) {
      index = i;
      break;
    }
  }
  return index;
}

int search_data_ij(const float *lat,const int ndimlat,const float *lont,const int ndimlont,
const float inlat,const float inlont,const float tol,int *row,int *col){
    std::vector<float> dlat;
    std::vector<float> dlont;
    (*row) = -1;
    (*col) = -1;

    float dminlat = 999.0;
    float dminlont = 999.0;
    dlat.resize(ndimlat);
    dlont.resize(ndimlont);
    for(int i=0;i<ndimlat;i++){
        //printf("i:%d inlat:%f lat[i]:%f\n",i,inlat,lat[i]);
        dlat[i] = fabs(inlat-lat[i]);
        if(dlat[i]<=dminlat) {
            dminlat = dlat[i];
            *row = i;
        }    
        //printf("i:%d inlat:%f lat[i]:%f dlat:%f dminlat:%f\n",i,inlat,lat[i],dlat[i],dminlat);

    }
    for(int j=0;j<ndimlont;j++){
        //printf("i:%d inlont:%f lont[i]:%f\n",i,inlont,lont[j]);
        dlont[j] = fabs(inlont-lont[j]);
        if(dlont[j]<=dminlont) {
            dminlont = dlont[j];
            *col = j;
        }
    }

    //printf("dminlat:%f dminlont:%f tol:%f\n",dminlat,dminlont,tol);    
    if((dminlat >= tol) || (dminlont >= tol)) {
        (*row) = -1;
                (*col) = -1;
        return -1;
    }

    return 0;
};

int main(int argc, char *argv[])
{
    setvbuf(stdout, NULL, _IONBF, 0);
    std::ofstream outtmin("/home/liuming/script/UI_historical_to_RHESSys_NetCDF/test_tmin.csv", std::ofstream::out);
    if(argc<=1){
        fprintf(stderr,"Usage:%s <1:netcdf_folder_with_slash> <2:Out_netcdf_data_folder_with_slash> <3:latmin> <4:latmax> <5:lonmin> <6:lonmax> <7:start_year> <8:end_year> <9:remove_human_effect> <10:adj_data_file>\n",argv[0]);
        return 1;
    }

    float viclatmin = atof(argv[3]);//41.0;
    float viclatmax = atof(argv[4]);//53.0;
    float viclontmin = atof(argv[5]);//-125.0;
    float viclontmax = atof(argv[6]);//-109.0;
    if (viclatmax < viclatmin) {
        float temp = viclatmax;
        viclatmax = viclatmin;
        viclatmin = temp;
    }
    if (viclontmax < viclontmin) {
        float temp = viclontmax;
        viclontmax = viclontmin;
        viclontmin = temp;
    }
    float viccell = 1.0/16.0;
    int start_year = atoi(argv[7]);
    int end_year = atoi(argv[8]);//2013;
    int total_years = end_year - start_year + 1;
    int remove_human_effect = 0;
    Adj_records *adjdata = (Adj_record *) malloc(DISTURB_YEARS * 12
                                                 * sizeof(Adj_record));
    if (argc > 9) {
        remove_human_effect = atoi(argv[9]);
        read_disturb_data(argv[10],adjdata);
    }
    //float *ts;    //wind speed total (m/s)
    enum var{PPT,TMAX,TMIN,WIND,SPH,SRAD,RMAX,RMIN,var_counts};
    var_dimention_type **var_dims = (var_dimention_type **) malloc(var_counts * sizeof(var_dimention_type *));
    for (int varinx = 0; varinx < var_counts; varinx++) var_dims[varinx] = (var_dimention_type *)malloc(total_years * sizeof(var_dimention_type));
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


    const float multi[] {40,100,100,100,10000,40,100,100};
    int vicnlat = (int)((viclatmax-viclatmin)/viccell);
    int vicnlont = (int)((viclontmax-viclontmin)/viccell);
    size_t nday = 366;
    size_t nlat;// = 585;
    size_t nlont;// = 1386;

    /* Get the varids of variables. */
    std::string netcdf_folder(argv[1]);
    std::string testnc = netcdf_folder + "vs_1979.nc";
    int retval;
    int ncid;
    if((retval = nc_open(testnc.c_str(), NC_NOWRITE, &ncid)))
                ERR(retval);
    int latid;
    if ((retval = nc_inq_varid(ncid, NLAT_NAME, &latid)))
        ERR(retval);
    if ((retval = nc_inq_dimlen(ncid,latid,&nlat)))
                ERR(retval);
    int lontid;
    if ((retval = nc_inq_varid(ncid, NLONT_NAME, &lontid)))
        ERR(retval);
    if ((retval = nc_inq_dimlen(ncid,lontid,&nlont)))
                ERR(retval);
    float *lat = (float *) malloc(nlat * sizeof(float));
    float *lont = (float *) malloc(nlont * sizeof(float));

#ifdef PART1
    float *tppt = (float *) malloc(nlat * nlont * nday * sizeof(float));
    float *tmax = (float *) malloc(nlat * nlont * nday * sizeof(float));
    float *tmin = (float *) malloc(nlat * nlont * nday * sizeof(float));
    float *vs = (float *) malloc(nlat * nlont * nday * sizeof(float));
#else
    float *sph = (float *) malloc(nlat * nlont * nday * sizeof(float));
    float *srad = (float *) malloc(nlat * nlont * nday * sizeof(float));
    float *rmax = (float *) malloc(nlat * nlont * nday * sizeof(float));
    float *rmin = (float *) malloc(nlat * nlont * nday * sizeof(float));
#endif
    std::cout<<"UI data:\nnlat:"<<nlat<<" nlont:"<<nlont<<std::endl;
    int varnum;// = 8;
    int start_var;
    int end_var;
#ifdef PART1
    start_var = PPT;
    end_var = WIND;
#else
    start_var = SPH;
    end_var = RMIN;
#endif
    varnum = end_var - start_var + 1;
    if ((retval = nc_get_var_float(ncid, latid, &lat[0])))
      ERR(retval);
    if ((retval = nc_get_var_float(ncid, lontid, &lont[0])))
      ERR(retval);

    int total_days = 0;
    for (int year = start_year; year <= end_year; ++year) {
      if (LEAPYR(year)) total_days += 366;
      else total_days += 365;
    }

    int out_nlat = 0;
    int out_nlont = 0;
    for (int nl = 0; nl < nlat; ++nl) {
      if (lat[nl] >= viclatmin && lat[nl] <= viclatmax) out_nlat++;
    }
    for (int nlt = 0; nlt < nlont; ++nlt) {
      if (lont[nlt] >= viclontmin && lont[nlt] <= viclontmax) out_nlont++;
    }

    float *out_lat = (float *) malloc(out_nlat * sizeof(float));
    float *out_lont = (float *) malloc(out_nlont * sizeof(float));
    float *out_time = (float *) malloc(total_days * sizeof(float));
#ifdef PART1
    float *out_tppt = (float *) malloc(out_nlat * out_nlont * total_days * sizeof(float));
    float *out_tmax = (float *) malloc(out_nlat * out_nlont * total_days * sizeof(float));
    float *out_tmin = (float *) malloc(out_nlat * out_nlont * total_days * sizeof(float));
    float *out_vs = (float *) malloc(out_nlat * out_nlont * total_days * sizeof(float));
#else
    float *out_sph = (float *) malloc(out_nlat * out_nlont * total_days * sizeof(float));
    float *out_srad = (float *) malloc(out_nlat * out_nlont * total_days * sizeof(float));
    float *out_rmax = (float *) malloc(out_nlat * out_nlont * total_days * sizeof(float));
    float *out_rmin = (float *) malloc(out_nlat * out_nlont * total_days * sizeof(float));
#endif

    std::cout<<"Out NetCDF data:\nnlat:"<<out_nlat<<" nlont:"<<out_nlont<<" days:"<<total_days<<std::endl;
    int start_lat = 0;
    for (int nl = 0; nl < nlat; ++nl) {
      if (lat[nl] >= viclatmin && lat[nl] <= viclatmax) {
         out_lat[start_lat] = lat[nl];
         start_lat++;
      }
    }
    std::cout<<" Finish out_lat[]\n";
    int start_lont = 0;
    for (int nlt = 0; nlt < nlont; ++nlt) {
      if (lont[nlt] >= viclontmin && lont[nlt] <= viclontmax) {
         out_lont[start_lont] = lont[nlt];
         start_lont++;
      }
    }
    std::cout<<" Finish out_lont[]\n";
    int start_days = 0;
    int start_day_in_day_dim = 0;
    for (int year = 1900; year <= end_year; ++year) {
      int ydays = 365;
      if (LEAPYR(year)) ydays = 366;
      if (year >= start_year) {
         for (int day = 0; day < ydays; day++) {
           out_time[start_day_in_day_dim] = start_days;
           start_day_in_day_dim++;
           start_days++;
         }
      }
      else start_days += ydays;
    }
    std::cout<<" Finish out_time[]\n";
    #pragma omp parallel for
    for (int day = 0; day < total_days; ++day) {
         //std::cout<<"\ttime:"<<day<<std::endl;
         for (int ilat = 0; ilat < out_nlat; ++ilat) {
           for (int ilont = 0; ilont < out_nlont; ++ilont) {
              long loc = day * out_nlat * out_nlont
                           + ilat * out_nlont
                           + ilont;
              #ifdef PART1
              out_tppt[loc] = -9999.0;
              out_tmax[loc] = -9999.0;
              out_tmin[loc] = -9999.0;
              out_vs[loc] = -9999.0;
              #else
              out_sph[loc] = -9999.0;
              out_srad[loc] = -9999.0;
              out_rmax[loc] = -9999.0;
              out_rmin[loc] = -9999.0;
              #endif
          }
        }
    }

    std::cout<<" Finish initilze\n";
    //identify index to netcdf grid
    //const float tol = cellsize;    //half of the netcdf grid
    /***Time period data to read***/
    int shift_days = get_days_since_1900(0,1979);
    for (int year = start_year; year <= end_year; year++) {
        size_t start[3],count[3];
        bool leapyear = LEAPYR(year);
        size_t tdays = leapyear ? 366 : 365;
        start[0] = 0;
        start[1] = 0;        //lat
        start[2] = 0;        //lont
        std::cout<<"Year:"<<year<<std::endl;
        for (int dvar = start_var; dvar <= end_var; dvar++) {
            std::stringstream ss;
            ss<<netcdf_folder<<varfile_prefix[dvar]<<"_"<<year<<".nc";
            int temp_ncid;
            int var_id;
            std::cout<<"dvar:"<<varname[dvar]<<std::endl;
            if((retval = nc_open(ss.str().c_str(), NC_NOWRITE, &temp_ncid)))
                    ERR(retval);            
            if ((retval = nc_inq_varid(temp_ncid, varname[dvar].c_str(), &var_id)))
                    ERR(retval);
            int daysid;
            if (retval = nc_inq_dimid(temp_ncid,NDAYS_NAME,&daysid))      ERR(retval);
            if (retval = nc_inq_dimid(temp_ncid,NLAT_NAME,&latid))        ERR(retval);
            if (retval = nc_inq_dimid(temp_ncid,NLONT_NAME,&lontid))      ERR(retval);
            int var_dim_id[3];
            if (retval = nc_inq_vardimid(temp_ncid,var_id,var_dim_id)) ERR(retval);
            if (var_dim_id[0] == latid && var_dim_id[1] == lontid
                && var_dim_id[2] == daysid) {
                var_dims[dvar][year-start_year] = LAT_LON_DAY;
                count[0] = nlat;
                count[1] = nlont;
                count[2] = tdays;
            } else if (var_dim_id[0] == daysid && var_dim_id[1] == latid
                        && var_dim_id[2] == lontid) {
                var_dims[dvar][year-start_year] = DAY_LAT_LON;
                count[0] = tdays;
                count[1] = nlat;
                count[2] = nlont;
            } else if (var_dim_id[0] == daysid && var_dim_id[1] == lontid
                && var_dim_id[2] == latid) {
                var_dims[dvar][year-start_year] = DAY_LON_LAT;
                count[0] = tdays;
                count[1] = nlont;
                count[2] = nlat;
            } else {
                std::cerr << "ERROR: the variable dimentions are not identified!\n";
                exit(0);
            }
#ifdef PART1
            if (dvar == PPT) {
                if ((retval = nc_get_vara_float(temp_ncid,var_id,start,count,&tppt[0])))
                    ERR(retval);
            }
            else if (dvar == TMAX) {
                                if ((retval = nc_get_vara_float(temp_ncid,var_id,start,count,&tmax[0])))
                                        ERR(retval);
                        }
            else if (dvar == TMIN) {
                                if ((retval = nc_get_vara_float(temp_ncid,var_id,start,count,&tmin[0])))
                                        ERR(retval);
                        }
            else if (dvar == WIND) {
                                if ((retval = nc_get_vara_float(temp_ncid,var_id,start,count,&vs[0])))
                                        ERR(retval);
                        }
#else
            if (dvar == SPH) {
                                if ((retval = nc_get_vara_float(temp_ncid,var_id,start,count,&sph[0])))
                                        ERR(retval);
                        }
            else if (dvar == SRAD) {
                                if ((retval = nc_get_vara_float(temp_ncid,var_id,start,count,&srad[0])))
                                        ERR(retval);
                        }
            else if (dvar == RMAX) {
                                if ((retval = nc_get_vara_float(temp_ncid,var_id,start,count,&rmax[0])))
                                        ERR(retval);
                        }
            else if (dvar == RMIN) {
                                if ((retval = nc_get_vara_float(temp_ncid,var_id,start,count,&rmin[0])))
                                        ERR(retval);
                        }
                        #endif
            nc_close(temp_ncid);
        }//end dvar
        
        //#pragma omp parallel for
        for (int dvar = start_var; dvar <= end_var; ++dvar) {
                //#pragma omp parallel for
              double mean[366];
              long number[366];
              #pragma omp parallel for
              for (int day = 0; day < 365; ++day) {
                    mean[day] = 0;
                    number[day] = 0;
              }
        #pragma omp parallel for
            for (int ilat = 0; ilat < nlat; ++ilat) {
                float f_lat = lat[ilat];
                int out_lat_index = get_index_from_array(f_lat,out_lat,out_nlat);
                //#pragma omp critical
                //std::cout<<"ilat:"<<ilat<<" out_lat:"<<out_lat_index<<std::endl;
                for (int ilon = 0; ilon < nlont; ++ilon) {
                    float f_lont = lont[ilon];
                    int out_lont_index = get_index_from_array(f_lont,out_lont,out_nlont);
                    for (int day = 0; day < tdays; ++day) {
                        month monthindex = get_month(year,day);
                        int sindex = get_disturb_index(year, monthindex+1);
                        long iindex(0);
                        if (var_dims[dvar][year-start_year] == DAY_LAT_LON)
                            iindex = day*nlat*nlont + ilat*nlont + ilon;
                        else if (var_dims[dvar][year-start_year] == DAY_LON_LAT)
                            iindex = day*nlont*nlat + ilon*nlat + ilat;
                        else 
                            iindex = ilat*nlont*tdays + ilon*tdays + day;
                    
                        int out_time_index = get_days_since_1900(day,year) - shift_days;

                        int out_all_index = -1;
                        if (out_lat_index != -1 && out_lont_index != -1) {
                            out_all_index = out_time_index * out_nlat * out_nlont
                                        + out_lat_index * out_nlont
                                        + out_lont_index;
                        }
                        if (out_all_index != -1) {
                            switch(dvar){
#ifdef PART1
                            case PPT:
                                if (tppt[iindex] >= 0.0) out_tppt[out_all_index] = tppt[iindex] / 24.0 / 3600.0;
                                else out_tppt[out_all_index] = 0.0;
                                add_valid_value(out_tppt[out_all_index],-9999.0,mean[day],number[day]);
                                break;
                            case TMAX:
                                 out_tmax[out_all_index] = tmax[iindex];
                                 if (remove_human_effect) out_tmax[out_all_index] -= adjdata[sindex].tmax;
                                 add_valid_value(out_tmax[out_all_index],-9999.0,mean[day],number[day]);
                                 break;
                            case TMIN:
                                 out_tmin[out_all_index] = tmin[iindex];
                                 if (remove_human_effect) out_tmin[out_all_index] -= adjdata[sindex].tmin;
                                 add_valid_value(out_tmin[out_all_index],-9999.0,mean[day],number[day]);
                                 break;
                            case WIND:
                                 out_vs[out_all_index] = vs[iindex];
                                 add_valid_value(out_vs[out_all_index],-9999.0,mean[day],number[day]);
                                 break;
#else
                            case SPH:
                                 out_sph[out_all_index] = sph[iindex];
                                 if (remove_human_effect) {out_sph[out_all_index] -= adjdata[sindex].sph;
                                    if (out_sph[out_all_index] < 0) out_sph[out_all_index] = 0;
                                 }
                                 break;
                            case SRAD:
                                 out_srad[out_all_index] = srad[iindex];
                                 break;
                            case RMAX:
                                 out_rmax[out_all_index] = rmax[iindex];
                                 if (remove_human_effect) out_rmax[out_all_index] -= adjdata[sindex].rmax;
                                 break;
                            case RMIN:
                                 out_rmin[out_all_index] = rmin[iindex];
                                 if (remove_human_effect) out_rmin[out_all_index] -= adjdata[sindex].rmin;
                                 break;
#endif
                            }  //switch
                        }  //out_all_index
                    }  //day
                }  //lon
            }  //lat
            std::cout<<"dvar:"<<varname[dvar]<<" finish set total array!"<<std::endl;
        }  //var
        }  //year
    printf("*** SUCCESS reading file\n");

        //Output netcdf files
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
        std::string date_out = "03 March 2015";
        std::string note1 = "The projection information for this file is: GCS WGS 1984.";
        std::string note2 = "Citation: Abatzoglou, J.T., 2012, Development of gridded surface meteorological data for ecological applications and modeling, International Journal of Climatology, DOI: 10.1002/joc.3413";
        time_t t = time(0);
        struct tm * now = localtime(&t);
        std::string timeinfo(asctime(now));
        std::string note3 = "Reformatted into RHESSys NetCDF format by Mingliang Liu mingliang.liu@wsu.edu on" + timeinfo; 
        int dimids[3];
        size_t count[3],start[3];

        int ndaysid,nlatid,nlontid,dayid,dataid;
        for (int dvar = start_var; dvar <= end_var; dvar++) {
            std::stringstream ss;
            ss<<argv[2]<<"RHESSys_NetCDF_"<<out_varfile_prefix[dvar]<<"_daily_UI_historical_"<<start_year<<"_"<<end_year<<"_CRB.nc";
            if ((retval = nc_create(ss.str().c_str(), NC_CLOBBER, &ncid)))
                             ERR(retval);
            if ((retval = nc_def_dim(ncid, OUT_TIME_NAME, total_days, &ndaysid)))
                    ERR(retval);
            if ((retval = nc_def_dim(ncid, OUT_LAT_NAME, out_nlat, &nlatid)))
                    ERR(retval);
            if ((retval = nc_def_dim(ncid, OUT_LONT_NAME, out_nlont, &nlontid)))
                    ERR(retval);

            if ((retval = nc_def_var(ncid, OUT_TIME_NAME, NC_FLOAT, 1, &ndaysid,&dayid)))
                    ERR(retval);
            if ((retval = nc_def_var(ncid, OUT_LAT_NAME, NC_FLOAT, 1, &nlatid,&latid)))
                    ERR(retval);
            if ((retval = nc_def_var(ncid, OUT_LONT_NAME, NC_FLOAT, 1, &nlontid, &lontid)))
                    ERR(retval);

             /* Assign units attributes to coordinate variables. */

             if ((retval = nc_put_att_text(ncid, dayid, UNITS, days_unit_attlen,unit_days.c_str())))
                     ERR(retval);
             if ((retval = nc_put_att_text(ncid, dayid, "calendar", calnendar.length(), calnendar.c_str())))
                     ERR(retval);
             if ((retval = nc_put_att_text(ncid, latid, UNITS, lat_unit_attlen, unit_lat.c_str())))
                     ERR(retval);
             if ((retval = nc_put_att_text(ncid, lontid, UNITS, lont_unit_attlen, unit_lont.c_str())))
                     ERR(retval);
             if ((retval = nc_put_att_text(ncid, dayid, DESCRIPTION, days_descript_attlen, descript_days.c_str())))
                     ERR(retval);

             if ((retval = nc_put_att_text(ncid, latid, DESCRIPTION, lat_descript_attlen, descript_lat.c_str())))
                     ERR(retval);
             if ((retval = nc_put_att_text(ncid, lontid, DESCRIPTION, lont_descript_attlen, descript_lont.c_str())))
                     ERR(retval);

             dimids[0] = ndaysid;
             dimids[1] = nlatid;
             dimids[2] = nlontid;
             float fill = -9999.0;
             if ((retval = nc_def_var(ncid, out_varname[dvar].c_str(), NC_FLOAT, 3, dimids, &dataid)))
                     ERR(retval);
             if ((retval = nc_put_att_text(ncid, dataid, UNITS, out_varunit[dvar].length(), out_varunit[dvar].c_str())))
                     ERR(retval);
             if ((retval = nc_put_att_text(ncid, dataid, DESCRIPTION,out_var_description[dvar].length(),out_var_description[dvar].c_str())))
                     ERR(retval);
             if ((retval = nc_put_att_float(ncid, dataid, "_FillValue", NC_FLOAT, 1, &fill)))
                     ERR(retval);
             if ((retval = nc_put_att_text(ncid, dataid, ESRI_PE_STRING, data_esri_attlen, descript_esri_pe_string.c_str())))
                     ERR(retval);
             if ((retval = nc_put_att_text(ncid, dataid, COORDINATES, data_coordinates_attlen, descript_coordinates.c_str())))
                     ERR(retval);
             if (dvar != PPT && dvar != SRAD) {
               if ((retval = nc_put_att_text(ncid, dataid, "height", out_varheight[dvar].length(),out_varheight[dvar].c_str())))
                       ERR(retval);
             }
             if ((retval = nc_put_att_float(ncid, dataid, "missing_value", NC_FLOAT, 1, &fill)))
                     ERR(retval);


             if ((retval = nc_put_att_text(ncid, NC_GLOBAL, "author", author.length(), author.c_str())))
                     ERR(retval);
             if ((retval = nc_put_att_text(ncid, NC_GLOBAL, "date", date_out.length(), date_out.c_str())))
                     ERR(retval);
             if ((retval = nc_put_att_text(ncid, NC_GLOBAL, "note1", note1.length(), note1.c_str())))
                     ERR(retval);
             if ((retval = nc_put_att_text(ncid, NC_GLOBAL, "note2", note2.length(), note2.c_str())))
                     ERR(retval);
             if ((retval = nc_put_att_text(ncid, NC_GLOBAL, "note3", note3.length(), note3.c_str())))
                     ERR(retval);

             /* End define mode. */
             if ((retval = nc_enddef(ncid)))
                     ERR(retval);

             if ((retval = nc_put_var_float(ncid, dayid, &out_time[0])))
                     ERR(retval);
             if ((retval = nc_put_var_float(ncid, latid, &out_lat[0])))
                     ERR(retval);
             if ((retval = nc_put_var_float(ncid, lontid, &out_lont[0])))
                     ERR(retval);

             count[0] = total_days;
             count[1] = out_nlat;
             count[2] = out_nlont;
             start[0] = 0;
             start[1] = 0;
             start[2] = 0;
             float *data_subset;
             switch(dvar){
#ifdef PART1
             case PPT:
                 data_subset = out_tppt;
                 break;
             case TMAX:
                  data_subset = out_tmax;
                  break;
             case TMIN:
                  data_subset = out_tmin;
                  break;
             case WIND:
                  data_subset = out_vs;
                  break;
#else
             case SPH:
                  data_subset = out_sph;
                  break;
             case SRAD:
                  data_subset = out_srad;
                  break;
             case RMAX:
                  data_subset = out_rmax;
                  break;
             case RMIN:
                  data_subset = out_rmin;
                  break;
#endif
             }  //switch
             if ((retval = nc_put_vara_float(ncid, dataid, start, count, data_subset)))
                     ERR(retval);
             if ((retval = nc_close(ncid)))
                     ERR(retval);
             printf("*** SUCCESS writing subset file %s!\n", ss.str().c_str());
      }


    free(lat);
    free(lont);
    free(adjdata);
    for (int varinx = 0; varinx < var_counts; varinx++) free(var_dims[varinx]);
    free(var_dims);
#ifdef PART1
    free(tppt);
    free(tmax);
    free(tmin);
        free(vs);
#else
    free(sph);
        free(srad);
        free(rmax);
        free(rmin);
#endif

        free(out_lat);
        free(out_lont);
        free(out_time);
#ifdef PART1
        free(out_tppt);
        free(out_tmax);
        free(out_tmin);
        free(out_vs);
#else
        free(out_sph);
        free(out_srad);
        free(out_rmax);
        free(out_rmin);
#endif
    //free(ts);
    return 0;
}

void add_valid_value(const double add_value, const double invalid_value,double &target, long &count)
{
   if (fabs(add_value-invalid_value) >= 1e-6) {
       target += add_value;
       count++;
   }
}
