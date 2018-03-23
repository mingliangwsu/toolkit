/************************
Convert netcdf data from 1/24 degree to 1/16 degree data
MACA V2 UI data into VIC binary format.
Mingliang Liu
10/21/2015
*************************/

//Four variables ppt,tmax,tmin,wind
//unsigned short, signed short, signed short, signed short
#define VIC_CLASSICAL
#define OUT_VIC_BINARY

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netcdf.h>
#include <math.h>
#include <vector>
#include <iostream>
#include <string>
#include <sstream>
#define NDAYS_NAME "time"
#define NLAT_NAME "lat"
#define NLONT_NAME "lon"

#define UNITS "units"
#define DESCRIPTION "description"

/* Handle errors by printing an error message and exiting with a
 * non-zero status. */
#define ERR(e) {printf("Error: %s\n", nc_strerror(e)); return 2;}

#ifndef _LEAPYR
#define LEAPYR(y) (!((y)%400) || (!((y)%4) && ((y)%100)))
#endif

//using namespace std;

int monthdays[12]={31,28,31,30,31,30,31,31,30,31,30,31};

/****from year,mon,day converted to days since 1900-01-01****/ 
//leap years
int get_indays_leap_years(const int year,const int mon,const int day){
   //mon:1-12 day:1-31
   int inday = 0;
   if(year<1900) return inday;
   for (int i = 1900; i < year; i++) {
      if(LEAPYR(i)) inday += 366;
      else inday += 365;
   }
   if(LEAPYR(year)) monthdays[1] = 29;
   else monthdays[1] = 28;
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
struct point{
   int row;
   int col;
};
//______________________________________________________________________________
int search_data_ij(const float *lat,const int ndimlat,const float *lont,const int ndimlont,
const float inlat,const float inlont,const float tol,int *row,int *col){
   //std::vector<float> dlat;
   //std::vector<float> dlont;
   float dlat,dlont;
   (*row) = -1;
   (*col) = -1;
   float dminlat = 999.0;
   float dminlont = 999.0;
   //dlat.resize(ndimlat);
   //dlont.resize(ndimlont);
   for (int i = 0; i < ndimlat; i++){
      //printf("i:%d inlat:%f lat[i]:%f\n",i,inlat,lat[i]);
      dlat = fabs(inlat-lat[i]);
      if(dlat <= dminlat) {
         dminlat = dlat;
         *row = i;
      }
      //printf("i:%d inlat:%f lat[i]:%f dlat:%f dminlat:%f\n",i,inlat,lat[i],dlat[i],dminlat);
   }
   for(int j = 0; j < ndimlont; j++){
      //printf("i:%d inlont:%f lont[i]:%f\n",i,inlont,lont[j]);
      dlont = fabs(inlont-lont[j]);
      if (dlont <= dminlont) {
         dminlont = dlont;
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
//______________________________________________________________________________
bool find_netcdf_filename(const std::string data_folder, const std::string model, 
   const std::string scn, const int year, const std::string var, std::string &filename,
   int &nc_start_year, int &nc_end_year) {
   int period_longth = 5;
   nc_start_year = year;
   nc_end_year   = nc_start_year + period_longth - 1;
   if (scn == "historical") {
      if (nc_end_year > 2005) nc_end_year = 2005;
   } else {
     if (nc_end_year > 2099) nc_end_year = 2099;
   }
   std::stringstream ss("");
    int trys(0);
    while (trys < 6/*150908LML 3*/) {
        ss.str("");
        if (trys == 0) {
            ss<<data_folder<<"maca_"          <<var<<"_"<<model<<"_"        <<scn<<"_"<<nc_start_year<<"_"<<nc_end_year       <<"_"<<"CONUS_daily.nc";
        } else if (trys == 1) {
            ss<<data_folder<<"macav2metdata_" <<var<<"_"<<model<<"_r1i1p1_" <<scn<<"_"<<nc_start_year<<"_"<<nc_end_year       <<"_"<<"CONUS_daily.nc";
        } else if (trys == 2) {
            ss<<data_folder<<"macav2metdata_" <<var<<"_"<<model<<"_r6i1p1_" <<scn<<"_"<<nc_start_year<<"_"<<nc_end_year       <<"_"<<"CONUS_daily.nc";
        } else if (trys == 3) {
            ss<<data_folder<<"maca_"          <<var<<"_"<<model<<"_"        <<scn<<"_"<<nc_start_year<<"_"<<(nc_end_year + 1) <<"_"<<"CONUS_daily.nc";
        } else if (trys == 4) {
            ss<<data_folder<<"macav2metdata_" <<var<<"_"<<model<<"_r1i1p1_" <<scn<<"_"<<nc_start_year<<"_"<<(nc_end_year + 1) <<"_"<<"CONUS_daily.nc";
        } else if (trys == 5) {
            ss<<data_folder<<"macav2metdata_" <<var<<"_"<<model<<"_r6i1p1_" <<scn<<"_"<<nc_start_year<<"_"<<(nc_end_year + 1) <<"_"<<"CONUS_daily.nc";
        }
        std::cerr<<"Try:"<<trys<<" file name:"<<ss.str()<<std::endl;
        int ncid;
        int retval = nc_open(ss.str().c_str(), NC_NOWRITE, &ncid);
        if (retval == NC_NOERR) {
            filename = ss.str();
            nc_close(ncid);
            if (trys >= 3) nc_end_year++;
            return true;
        }
        trys++;
    }
    if (trys == 6) {
        nc_start_year = 0;
        nc_end_year = 0;
        filename = "";
        return false;
    }
}
//______________________________________________________________________________
void setminmax(float &minv,float &maxv) {
   double temp;
   if (minv > maxv) {
      temp = minv;
      minv = maxv;
      maxv = temp;
   }
}

int main(int argc, char *argv[])
{
   setvbuf(stdout, NULL, _IONBF, 0);
   if (argc < 9) {
       fprintf(stderr,"Usage:\n\t%s [1:maca_netcdf_folder_with_slash] [2:model_name] [3:scenario] [4:version] [5:latmin] [6:latmax] [7:lontmin] [8:lontmax] [9:output_folder_with_slash]\n",argv[0]);
     return 1;
   }
   std::string macav1_foldername(argv[1]);
   std::string model(argv[2]);
   std::string scn(argv[3]);
   std::string version(argv[4]);
   float viclatmin = atof(argv[5]);
   float viclatmax = atof(argv[6]);
   float viclontmin = atof(argv[7]);
   float viclontmax = atof(argv[8]);
   std::string outbinary_foldername(argv[9]);
   float viccell = 1.0/16.0;
   setminmax(viclatmin,viclatmax);
   setminmax(viclontmin,viclontmax);
   //float *ts;   //wind speed total (m/s)
   enum var{PPT,TMAX,TMIN,UAS,VAS,SPH,SRAD,RMAX,RMIN};
   //MACA V2 units: pr (mm/day) tasmax (K @ 2m) uas (m/s @ 10m)
   //        dimensions: lat 585 lon 1386 var(time,lat,lon)
   //        lat & lon: center of each gridcell
   //        lon: 0-360
   std::string varfile_prefix[] {"pr","tasmax","tasmin","uas"
               ,"vas","huss","rsds","rhsmax","rhsmin"};
   std::string varname[] {"precipitation","air_temperature","air_temperature","eastward_wind"
           ,"northward_wind","specific_humidity","surface_downwelling_shortwave_flux_in_air","relative_humidity","relative_humidity"};
   if (argc <= 1) {
       fprintf(stderr,"Usage:%s <1:model_name> <2:scenario>\n",argv[0]);
     return 1;
   }
   int vicnlat = (int)((viclatmax-viclatmin)/viccell);
   int vicnlont = (int)((viclontmax-viclontmin)/viccell);
   struct point **vicindex = (struct point **) malloc(vicnlat*vicnlont*sizeof(struct point*));
   for (int i = 0; i < vicnlat*vicnlont; ++i)
      vicindex[i] = (struct point *)malloc(9*sizeof(struct point));

   /* Get the varids of variables. */
   std::string testnc = macav1_foldername + "macav2metdata_pr_" + model + "_" + version + "_historical_1950_1954_CONUS_daily.nc";
   int retval,ncid,daysid,latid,lontid;
   size_t recs_days,nlat,nlont;
   if (retval = nc_open(testnc.c_str(),NC_NOWRITE,&ncid))   ERR(retval);
   if (retval = nc_inq_dimid(ncid,NDAYS_NAME,&daysid))      ERR(retval);
   if (retval = nc_inq_dimlen(ncid,daysid,&recs_days))      ERR(retval);
   if (retval = nc_inq_dimid(ncid,NLAT_NAME,&latid))        ERR(retval);
   if (retval = nc_inq_dimlen(ncid,latid,&nlat))            ERR(retval);
   if (retval = nc_inq_dimid(ncid,NLONT_NAME,&lontid))      ERR(retval);
   if (retval = nc_inq_dimlen(ncid,lontid,&nlont))          ERR(retval);
   if (recs_days != (get_indays_leap_years(1954,12,31) - get_indays_leap_years(1950,1,1) + 1)) {
      std::cerr<<"ERROR: MACA netcdf is not gregorian calendar!!!\n";
      exit(1);
   }
   std::clog<<"\nnlat:"<<nlat
            <<"\nnlon:"<<nlont
            <<std::endl;
   int nday = 366 * 5;

   float *lat =  (float *) malloc(nlat * sizeof(float));
   float *lont = (float *) malloc(nlont * sizeof(float));
   float *tppt = (float *) malloc(nlat * nlont * nday * sizeof(float));
   float *tmax = (float *) malloc(nlat * nlont * nday * sizeof(float));
   float *tmin = (float *) malloc(nlat * nlont * nday * sizeof(float));
   float *uas =  (float *) malloc(nlat * nlont * nday * sizeof(float));
   float *vas =  (float *) malloc(nlat * nlont * nday * sizeof(float));
#ifndef VIC_CLASSICAL
   float *sph =  (float *) malloc(nlat * nlont * nday * sizeof(float));
   float *srad = (float *) malloc(nlat * nlont * nday * sizeof(float));
   float *rmax = (float *) malloc(nlat * nlont * nday * sizeof(float));
   float *rmin = (float *) malloc(nlat * nlont * nday * sizeof(float));
#endif

   int varlatid,varlontid;
   if ((retval = nc_inq_varid(ncid, NLAT_NAME, &varlatid)))       ERR(retval);
   if ((retval = nc_inq_varid(ncid, NLONT_NAME, &varlontid)))     ERR(retval);
   if ((retval = nc_get_var_float(ncid, latid, &lat[0])))         ERR(retval);
   if ((retval = nc_get_var_float(ncid, lontid, &lont[0])))       ERR(retval);
   for (int i = 0; i < nlont; i++) if (lont[i] > 180.0) lont[i] -= 360.0;
   nc_close(ncid);
   //identify index to netcdf grid
   const float tol = 0.6 * fabs(lont[0] - lont[1]);
   #pragma omp parallel for
   for(int i = 0; i < vicnlat; i++){
      float clat[9],clont[9];//up0;c 1;down: 2   left 0 c 1 right 2
      for (int n = 0; n < 3; n++){
         clat[3+n] = viclatmax - i*viccell - viccell/2.0; //central location
         clat[0+n] = clat[3+n] + viccell/3.0; //upper
         clat[6+n] = clat[3+n] - viccell/3.0; //lower
      }
      for (int j = 0; j < vicnlont; j++) {
         for(int n = 0; n < 3; n++){
            clont[n*3+1] = viclontmin + j*viccell + viccell/2.0;
            clont[n*3+0] = clont[1] - viccell/3.0;
            clont[n*3+2] = clont[1] + viccell/3.0;
         }
         int iloc = i*vicnlont + j;
         for (int k = 0; k < 9; k++) {
            int srow,scol;
            int ifind = search_data_ij(lat,nlat,lont,nlont,clat[k],clont[k],tol,&srow,&scol);
            vicindex[iloc][k].row = srow;
            vicindex[iloc][k].col = scol;
            //printf("vic_i:%d j:%d k:%d lat:%f lont:%f srow:%d scol:%d\n",i,j,k,clat[k],clont[k],srow,scol);
         }
      }
   }
   int start_year(0);
   int end_year(0);
    //std::string output_vic_folder;
   if (scn == "historical") {
      start_year = 1950;
      end_year = 2005;
   } else {
      start_year = 2006;
      end_year = 2099;
   }
    const float multi[] {40,100,100,100,100,10000,40,100,100};

    div_t time_div = std::div(end_year - start_year + 1,5);
    int total_periods = time_div.quot;
    int years_in_last_period = time_div.rem;
    if (years_in_last_period > 0) total_periods++;
    std::clog  <<model<<","
               <<scn<<",periods:"
               <<total_periods<<",years_last_period:"
               <<years_in_last_period
               <<std::endl;
    //process each period
    for (int period = 0; period < total_periods; period++) {
       size_t start[3],count[3];
       size_t tdays = 366 * 5;        //total number of records in time dimension
       int pstart_year(0);
       int pend_year(0);
       int period_start = start_year + period * 5;
       if (period == total_periods - 1) tdays = 366 * years_in_last_period;
       start[0] = 0;
       start[1] = 0;      //lat
       start[2] = 0;      //lont
       count[1] = nlat;
       count[2] = nlont;

       //std::string nc_file_name[9];//HERE
      int vars(0);
#ifdef VIC_CLASSICAL
      vars = 5;
#else
      vars = 9;
#endif
      for (int var = 0; var < vars; var++) {
         std::string nc_file_name("");
         bool get_data = find_netcdf_filename(macav1_foldername,
                                              model,
                                              scn,
                                              period_start,
                                              varfile_prefix[var],
                                              nc_file_name,
                                              pstart_year,
                                              pend_year);
         if (!get_data) {
             std::cerr<<"Can not find netcdf file: "<<nc_file_name
                        <<" for var:"
                        <<varfile_prefix[var]
                        <<" year: "<<period_start
                        <<" scn: "<<scn
                        <<" model:"<<model
                        <<std::endl;
             exit(1);
         }

         int ncid,var_id;
         std::cerr<<"var:"<<varname[var]<<std::endl;
         if((retval = nc_open(nc_file_name.c_str(), NC_NOWRITE, &ncid))) ERR(retval);
         //Test time calendar
         if (retval = nc_inq_dimid(ncid,NDAYS_NAME,&daysid))    ERR(retval);
         if (retval = nc_inq_dimlen(ncid,daysid,&recs_days))    ERR(retval);
         if (recs_days != (get_indays_leap_years(pend_year,12,31) - get_indays_leap_years(pstart_year,1,1) + 1)) {
             std::cerr<<nc_file_name<<" time dimension is NOT gregorian calendar!\n";
             exit(1);
         }
         count[0] = recs_days;

         //Get data
         if ((retval = nc_inq_varid(ncid, varname[var].c_str(), &var_id))) ERR(retval);
         if (var == PPT) {
         if ((retval = nc_get_vara_float(ncid,var_id,start,count,&tppt[0])))
            ERR(retval);
         } else if (var == TMAX) {
             if ((retval = nc_get_vara_float(ncid,var_id,start,count,&tmax[0])))
                 ERR(retval);
         } else if (var == TMIN) {
             if ((retval = nc_get_vara_float(ncid,var_id,start,count,&tmin[0])))
                 ERR(retval);
         } else if (var == UAS) {
             if ((retval = nc_get_vara_float(ncid,var_id,start,count,&uas[0])))
                 ERR(retval);
         } else if (var == VAS) {
             if ((retval = nc_get_vara_float(ncid,var_id,start,count,&vas[0])))
                 ERR(retval);
         }
#ifndef VIC_CLASSICAL
         else if (var == SPH) {
             if ((retval = nc_get_vara_float(ncid,var_id,start,count,&sph[0])))
                 ERR(retval);
         }
         else if (var == SRAD) {
             if ((retval = nc_get_vara_float(ncid,var_id,start,count,&srad[0])))
                 ERR(retval);
         }
         else if (var == RMAX) {
             if ((retval = nc_get_vara_float(ncid,var_id,start,count,&rmax[0])))
                 ERR(retval);
         }
         else if (var == RMIN) {
             if ((retval = nc_get_vara_float(ncid,var_id,start,count,&rmin[0])))
                 ERR(retval);
         }
#endif
         nc_close(ncid);
      }  //end var

      //Aggregate MACA v1 data for each VIC grid cell
      #pragma omp parallel for
      for (int i = 0; i < vicnlat; i++){
         float laty = viclatmax - i*viccell - viccell/2.0;
         for (int j = 0; j < vicnlont; j++){
            float lontx = viclontmin + j*viccell + viccell/2.0;
            int iloc = i*vicnlont + j;
            std::vector<std::vector<float> > value;
            value.resize(vars);
            for (int k = 0; k < vars; k++) {
               value[k].resize(tdays);
            }
            for (int day = 0; day < tdays; day++) {
                for(int dvar = 0; dvar < vars; dvar++){
                    value[dvar][day] = 0.0;
                    int validcells = 0;
                    for (int kd = 0; kd < 9; kd++){
                        if(vicindex[iloc][kd].row == -1 || vicindex[iloc][kd].col == -1){}
                        else{
                            long iindex = day*nlat*nlont
                                          + vicindex[iloc][kd].row*nlont
                                          + vicindex[iloc][kd].col;
                            float temp(-9999.0);
                            float netcdfvalue;
                            switch(dvar){
                            case PPT:
                                temp = tppt[iindex];
                                netcdfvalue = temp;                              //mm day-1
                                break;
                            case TMAX:
                                temp = tmax[iindex];
                                netcdfvalue = temp - 273.15 ;                    //K -> Celsius degree
                                break;
                            case TMIN:
                                temp = tmin[iindex];
                                netcdfvalue = temp - 273.15 ;
                                break;
                            case UAS:
                                temp = uas[iindex];
                                netcdfvalue = temp;
                                break;
                            case VAS:
                                temp = vas[iindex];
                                netcdfvalue = temp;
                                break;
                            #ifndef VIC_CLASSICAL
                            case SPH:
                                temp = sph[iindex];
                                netcdfvalue = temp;
                                break;
                            case SRAD:
                                temp = srad[iindex];
                                netcdfvalue = temp;
                                break;
                            case RMAX:
                                temp = rmax[iindex];
                                netcdfvalue = temp;
                                break;
                            case RMIN:
                                temp = rmin[iindex];
                                netcdfvalue = temp;
                                break;
                            #endif
                            }
                            if(temp > -999.0){
                                validcells++;
                                value[dvar][day] += netcdfvalue;
                            }
                        }
                      }  //kd
                      if (validcells > 0)
                         value[dvar][day] /= (float)validcells;
                      else value[dvar][day] = -9999.0;
                }  //dvar
            }  //day
            //#pragma omp critical
                //if (value[0][0] > 0) std::cerr<<"laty:"<<laty<<" lonx:"<<lontx<<" value0:"<<value[0][0]<<" value1:"<<value[1][0]<<" value2:"<<value[2][0]<<" value3:"<<value[3][0]<<" day:"<<0<<std::endl;
            /* open the out put file */
            if( value[PPT][0]  >= -999.0 &&
                value[TMAX][0] >= -999.0 &&
                value[TMIN][0] >= -999.0 &&
                value[UAS][0]  >= -999.0 &&
                value[VAS][0]  >= -999.0
                #ifndef VIC_CLASSICAL
                && value[SPH][0]  >= -999.0
                && value[SRAD][0] >= -999.0
                && value[RMAX][0] >= -999.0
                && value[RMIN][0] >= -999.0
                #endif
              )
            {
               char tempstr[200];
                    sprintf(tempstr,"%s%s/%s/data_%.5f_%.5f",outbinary_foldername.c_str(),model.c_str(),scn.c_str(),laty,lontx);
               //#pragma omp critical
               //std::cerr<<" file:"<<tempstr<<std::endl;
               FILE *fout;
               #ifdef OUT_VIC_BINARY
               if((fout = fopen(tempstr,"ab+")) == NULL){
                  #pragma omp critical
                  std::cerr<<"can't open binary file"<<tempstr<<std::endl;
                  exit(1);
               }
               #else
               if((fout = fopen(tempstr,"a+")) == NULL){
                   #pragma omp critical
                   std::cerr<<"can't open text file"<<tempstr<<std::endl;
                   exit(1);
               }
               #endif
               fseek(fout,0,SEEK_END);
               long day = 0;
               for (int year = pstart_year; year <= pend_year; year++) {
                   int year_days(365);
                   bool leap_year = LEAPYR(year);
                   if (leap_year) year_days = 366;
                   for (int doy = 0; doy < year_days; doy++) {
                       float temp_value = value[PPT][day];
                       #ifdef OUT_VIC_BINARY
                       unsigned short int ustmp = (unsigned short int)(temp_value*multi[PPT]);
                       fwrite(&ustmp,sizeof(unsigned short int), 1, fout);
                       #else
                       fprintf(fout,"%.5f\t",temp_value);
                       #endif
                       for (int dvar = 1; dvar < 3; dvar++) {
                           temp_value = value[dvar][day];
                           #ifdef OUT_VIC_BINARY
                           short int stmp = (short int)(temp_value*multi[dvar]);
                           fwrite(&stmp,sizeof(short int),1,fout);
                           #else
                           fprintf(fout,"%.5f\t",temp_value);
                           #endif
                       }

                       float wind = sqrt(value[UAS][day] * value[UAS][day] +
                                         value[VAS][day] * value[VAS][day]);
                       temp_value = wind;
                       #ifdef OUT_VIC_BINARY
                       short int stmp = (short int)(temp_value*multi[UAS]);
                       fwrite(&stmp,sizeof(short int),1,fout);
                       #else
                       fprintf(fout,"%.5f\t",temp_value);
                       #endif

                       #ifndef VIC_CLASSICAL
                       for (int dvar = 5; dvar < 9; dvar++) {
                           temp_value = value[dvar][day];
                           #ifdef OUT_VIC_BINARY
                           short int stmp = (short int)(temp_value*multi[dvar]);
                           fwrite(&stmp,sizeof(short int),1,fout);
                           #else
                           fprintf(fout,"%.5f\t",temp_value);
                           #endif
                       }
                       #endif
                       #ifndef OUT_VIC_BINARY
                       fprintf(fout,"\n");
                       #endif
                       day++;
                   } //doy
               }  //year
               fclose(fout);
            }
         }//j lont
      }//i lat
   }//year
   printf("*** SUCCESS reading file\n");
   free(lat);
   free(lont);
   free(tppt);
   free(tmax);
   free(tmin);
   free(uas);
   free(vas);
   #ifndef VIC_CLASSICAL
   free(sph);
   free(srad);
   free(rmax);
   free(rmin);
   #endif
   //free(ts);
   for( int i = 0; i < vicnlat*vicnlont; ++i) free(vicindex[i]);
   free(vicindex);
   return 0;
}
