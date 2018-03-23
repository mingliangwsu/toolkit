/************************
Convert Ben's netcdf data to traditional VIC Binary met data
Mingliang Liu
06/19/2017
*************************/

//Four variables ppt,tmax,tmin,wind
//unsigned short, signed short, signed short, signed short
#define VIC_CLASSICAL

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netcdf.h>
#include <math.h>
#include <vector>
#include <iostream>
#include <string>
#include <sstream>
#define NDAYS_NAME "day"
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
std::string month_str[12]={"01","02","03","04","05","06","07","08","09","10","11","12"};

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
int get_start_lat(float *lat,int ndim,float inlat){
    int start = -9999;
    int i;
    for(i=0;i<ndim;i++){
        if(inlat>=lat[i]){
            start = i-1;
            break;
        } 
    }
    if(start == -9999) return -1;
    else if(start == -1) return 0;
    else return start;
};

/***Get the start number of lont in netcdf***/
int get_start_lont(float *lont,int ndim,float inlont){
    int start = -9999;
    int i;
    for(i=0;i<ndim;i++){
        if(inlont<=lont[i]){
            start = i-1;
            break;
        } 
    }
    if(start == -9999) return -1;
    else if(start == -1) return 0;
    else return start;
};

struct point{
    int row;
    int col;
};

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
    double nodata = -9999.0;
    double viccell = 1.0 / 16.0;
    double half_viccell = viccell / 2.0;
    enum var{PPT,TMAX,TMIN,WIND};
    //std::string varfile_prefix[] {"pr","tmmx","tmmn","vs"};
    std::string varname[] {"Prec","Tmax","Tmin","wind"};
    if (argc < 9) {
        fprintf(stderr,"Usage:%s <1:netcdf_folder_with_slash> <2:VIC_data_folder_with_slash> <3:latmin_or_max> <4:latmin_or_max> <5:lonmin_or_max> <6:lonmin_or_max> <7:start_year> <8:end_year>\n",argv[0]);
        return 1;
    }
    

    //subset of selected region
    double tlat1 = round(atof(argv[3]));
    double tlat2 = round(atof(argv[4]));
    double tlon1 = round(atof(argv[5]));
    double tlon2 = round(atof(argv[6]));
    int start_year = atoi(argv[7]);
    int end_year = atoi(argv[8]);
    int years = end_year - start_year + 1;
    long potdays = years * 366;

    double viclatmin = tlat1 < tlat2 ? tlat1 : tlat2;
    double viclatmax = tlat1 > tlat2 ? tlat1 : tlat2;
    double viclontmin = tlon1 < tlon2 ? tlon1 : tlon2;
    double viclontmax = tlon1 > tlon2 ? tlon1 : tlon2;
    int vicnlat = (int)((viclatmax-viclatmin)/viccell);
    int vicnlont = (int)((viclontmax-viclontmin)/viccell);
    //allocate mem for storing the data
    long long potrecords = potdays * vicnlat * vicnlont;   //[day][lat][lon]
    long long tt = 1000 * vicnlat * vicnlont;
    printf("Potrecords:%lld\ttt:%lld\tpotdays:%d\tvicnlat:%d\tvicnlont:%d\tviclatmin:%f\tviclontmin:%f\n",potrecords,tt,potdays,vicnlat,vicnlont,viclatmin,viclontmin);

    float *data_ppt = (float *) malloc(potrecords * sizeof(float));
    float *data_tmax = (float *) malloc(potrecords * sizeof(float));
    float *data_tmin = (float *) malloc(potrecords * sizeof(float));
    float *data_vs = (float *) malloc(potrecords * sizeof(float));
    #pragma omp parallel for
    for (long long i = 0; i < potrecords; i++) {
        data_ppt[i] = nodata;
        data_tmax[i] = nodata;
        data_tmin[i] = nodata;
        data_vs[i] = nodata;
    }
    
    //hard coded the Ben's netCDF data set
    long long nday = 31;
    long long onemonth_size = nday * vicnlat * vicnlont;
    float *tppt = (float *) malloc(onemonth_size * sizeof(float));
    float *tmax = (float *) malloc(onemonth_size * sizeof(float));
    float *tmin = (float *) malloc(onemonth_size * sizeof(float));
    float *vs = (float *) malloc(onemonth_size* sizeof(float));
    std::string netcdf_folder(argv[1]);
    float nc_minlat = 14.65625;
    float nc_minlont = -124.96875;

    //identify index to netcdf grid
    const float multi[] {40,100,100,100};
    size_t start[3],count[3];
    /***Time period data to read***/
    long long day_index = 0;
    for (int year = start_year; year <= end_year; year++) {
        count[1] = vicnlat;
        count[2] = vicnlont;

        start[0] = 0;
        start[1] = (long long) round((viclatmin + half_viccell - nc_minlat) / viccell);      //lat
        start[2] = (long long) round((viclontmin + half_viccell - nc_minlont) / viccell);    //lont
        for (int month = 1; month <= 12; month++) {
            count[0] = monthdays[month - 1];
            if (LEAPYR(year) && month == 2) count[0] = 29;
            /*std::cerr<<"Year:"<<year
                     <<"\tmonth:"<<month
                     <<"\tcount[0]:"<<count[0]
                     <<"\tcount[1]:"<<count[1]
                     <<"\tcount[2]:"<<count[2]
                     <<std::endl;*/
            char testnc[1024];
            sprintf(testnc, "%slivneh_NAmerExt_1Sep2016.%d%s.nc", argv[1],year,month_str[month-1].c_str());
            //std::string testnc = netcdf_folder + "livneh_NAmerExt_1Sep2016." + year + month_str[month];
            int retval;
            int ncid;
            int var_id;
            /* Get the varids of variables. */
            if((retval = nc_open(testnc, NC_NOWRITE, &ncid)))
                ERR(retval);
            for (int dvar = 0; dvar < 4; dvar++) {            
                if ((retval = nc_inq_varid(ncid, varname[dvar].c_str(), &var_id)))
                    ERR(retval);
                if (dvar == PPT) {
                    if ((retval = nc_get_vara_float(ncid,var_id,start,count,&tppt[0])))
                        ERR(retval);
                } else if (dvar == TMAX) {
                    if ((retval = nc_get_vara_float(ncid,var_id,start,count,&tmax[0])))
                        ERR(retval);
                } else if (dvar == TMIN) {
                    if ((retval = nc_get_vara_float(ncid,var_id,start,count,&tmin[0])))
                        ERR(retval);
                } else if (dvar == WIND) {
                    if ((retval = nc_get_vara_float(ncid,var_id,start,count,&vs[0])))
                        ERR(retval);
                }
            } //end dvar
            nc_close(ncid);
            //transfer data to overall array
            #pragma omp parallel for
            for (int day = 0; day < count[0]; day++) {
                for (int lat_id = 0; lat_id < vicnlat; lat_id++) {
                    for (int lont_id = 0; lont_id < vicnlont; lont_id++) {
                        long long local_index = day * vicnlat * vicnlont + lat_id * vicnlont + lont_id;
                        long long global_index = (day + day_index) * vicnlat * vicnlont + lat_id * vicnlont + lont_id;
                        if (tppt[local_index] < 1.0e10) data_ppt[global_index]  = tppt[local_index];
                        if (tmax[local_index] < 1.0e10) data_tmax[global_index] = tmax[local_index];
                        if (tmin[local_index] < 1.0e10) data_tmin[global_index] = tmin[local_index];
                        if (vs[local_index]   >= 0.0)   data_vs[global_index]   = vs[local_index];
                    } //lont_id
                } //lat_id
            } //day
            day_index += count[0];
        } //month
    } //year
    printf("*** Reading Complete!!!\n");
    /* open the out put file */
    
    for (int lat_id = 0; lat_id < vicnlat; lat_id++) {
        double laty = viclatmin + half_viccell + lat_id * viccell;
        printf("*** Writing lat:%f\n",laty);
        for (int lont_id = 0; lont_id < vicnlont; lont_id++) {
            double lontx = viclontmin + half_viccell + lont_id * viccell;
            long long first_day_index = lat_id * vicnlont + lont_id;
            if (data_ppt[first_day_index] >= -999.0 && 
                data_tmax[first_day_index]              >= -999.0 && 
                data_tmin[first_day_index]              >= -999.0 && 
                data_vs[first_day_index]                >= -999.0) {
                char tempstr[200];
                sprintf(tempstr,"%sdata_%.5f_%.5f",argv[2],laty,lontx);
                printf("Output file name:%s\n",tempstr);
                //#pragma omp critical
                //std::cerr<<" file:"<<tempstr<<std::endl;
                FILE *fout;
                if((fout = fopen(tempstr,"wb")) == NULL){
                    //#pragma omp critical
                    std::cerr<<"can't open binary file:"<<tempstr<<std::endl;
                    exit(1);
                }
                fseek(fout,0,SEEK_END);
                float value[4];
                for (long long day = 0; day < day_index; day++) {
                    long long global_index = day * vicnlat * vicnlont + lat_id * vicnlont + lont_id;
                    value[0] = data_ppt[global_index];
                    value[1] = data_tmax[global_index];
                    value[2] = data_tmin[global_index];
                    value[3] = data_vs[global_index];
                    unsigned short int ustmp = (unsigned short int)(value[0]*multi[0]);
                    fwrite(&ustmp,sizeof(unsigned short int), 1, fout);
                    for (int dvar = 1; dvar < 4;dvar++) {
                        short int stmp = (short int)(value[dvar]*multi[dvar]);
                        fwrite(&stmp,sizeof(short int),1,fout);
                    }
                    //printf("day:%d\tlat:%f\tlon:%f\tppt:%f\ttmax:%f\ttmin:%f\twind:%f\n",day,laty,lontx,value[0],value[1],value[2],value[3]);
                }//day
                fclose(fout);
            }  //if
        } //lont_id
    } //lat_id
    printf("*** SUCCESS writing file!\n");
    //free(lat);
    //free(lont);
    free(tppt);
    free(tmax);
    free(tmin);
    free(vs);
    free(data_ppt);
    free(data_tmax);
    free(data_tmin);
    free(data_vs);

    return 0;
}
