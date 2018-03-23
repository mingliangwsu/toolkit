/************************
Convert netcdf data from 1/24 degree to 1/16 degree dat
Historical UI data into VIC binary format.
Mingliang Liu
06/01/2015
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
	float viclatmin = 41.0;
	float viclatmax = 53.0;
	float viclontmin = -125.0;
	float viclontmax = -109.0;
	float viccell = 1.0/16.0;
	//float *ts;	//wind speed total (m/s)
	enum var{PPT,TMAX,TMIN,WIND};
	std::string varfile_prefix[] {"pr","tmmx","tmmn","vs"};
        std::string varname[] {"precipitation_amount","air_temperature","air_temperature","wind_speed"};
   	if(argc<=1){
	fprintf(stderr,"Usage:%s <1:netcdf_folder_with_slash> <2:VIC_data_folder_with_slash>\n",argv[0]);
		return 1;
	}
	int vicnlat = (int)((viclatmax-viclatmin)/viccell);
	int vicnlont = (int)((viclontmax-viclontmin)/viccell);
	struct point **vicindex = (struct point **)malloc(vicnlat*vicnlont*sizeof(struct point*));
        for (int i = 0; i < vicnlat*vicnlont; ++i)
		vicindex[i] = (struct point *)malloc(9*sizeof(struct point));
	size_t nday = 366;
	size_t nlat = 585;
	size_t nlont = 1386;
 	float *lat = (float *) malloc(nlat * sizeof(float));
  	float *lont = (float *) malloc(nlont * sizeof(float));
	float *tppt = (float *) malloc(nlat * nlont * nday * sizeof(float));
	float *tmax = (float *) malloc(nlat * nlont * nday * sizeof(float));
	float *tmin = (float *) malloc(nlat * nlont * nday * sizeof(float));
        float *vs = (float *) malloc(nlat * nlont * nday * sizeof(float));
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
	int lontid;
	if ((retval = nc_inq_varid(ncid, NLONT_NAME, &lontid)))
		ERR(retval);
	if ((retval = nc_get_var_float(ncid, latid, &lat[0])))
      		ERR(retval);
	if ((retval = nc_get_var_float(ncid, lontid, &lont[0])))
      		ERR(retval);
 	float maxlat = 49.39602;
	float minlat = 25.06308;
	float maxlont = -67.06475;
	float minlont = -124.7722;
	float cellsize = 1.0 / 24.0;

	//identify index to netcdf grid
	const float tol = cellsize;	//half of the netcdf grid
	#pragma omp parallel for
	for(int i=0;i<vicnlat;i++){
		float clat[9],clont[9];//up0;c 1;down: 2   left 0 c 1 right 2
		for(int n=0;n<3;n++){
			clat[3+n] = viclatmax - i*viccell - viccell/2.0; //central location
			clat[0+n] = clat[3+n] + viccell/3.0; //upper 
			clat[6+n] = clat[3+n] - viccell/3.0; //lower
		}
		for(int j=0;j<vicnlont;j++){
			for(int n=0;n<3;n++){
				clont[n*3+1] = viclontmin + j*viccell + viccell/2.0;
				clont[n*3+0] = clont[1] - viccell/3.0;
				clont[n*3+2] = clont[1] + viccell/3.0;
			}
			for(int k=0;k<9;k++){
				int srow,scol;
				int ifind = search_data_ij(lat,nlat,lont,nlont,clat[k],clont[k],tol,&srow,&scol);
				int iloc = i*vicnlont + j;
				vicindex[iloc][k].row = srow;
				vicindex[iloc][k].col = scol;
				//printf("vic_i:%d j:%d k:%d lat:%f lont:%f srow:%d scol:%d\n",i,j,k,clat[k],clont[k],srow,scol);
			}
		}
	}	
	/***Time period data to read***/
    const float multi[] {40,100,100,100};
    int start_year = 1979;
    int end_year = 2015;
    for (int year = start_year; year <= end_year; year++) {
        size_t start[3],count[3];
        size_t tdays = LEAPYR(year) ? 366 : 365;
        start[0] = 0;
        start[1] = 0;        //lat
        start[2] = 0;        //lont
        
        std::cerr<<"Year:"<<year<<std::endl;
            for (int dvar=0;dvar<4;dvar++) {
            if (dvar == WIND && year <= 2010) {
                count[0] = tdays;
                count[1] = nlat;
                count[2] = nlont;
            } else if (year == 2015) {
                count[0] = tdays;
                count[1] = nlont;
                count[2] = nlat;
            } else {
                count[0] = nlat;
                count[1] = nlont;
                count[2] = tdays;
            }
            std::stringstream ss;
            ss<<netcdf_folder<<varfile_prefix[dvar]<<"_"<<year<<".nc";
            int temp_ncid;
            int var_id;
            std::cerr<<"dvar:"<<varname[dvar]<<std::endl;
            if((retval = nc_open(ss.str().c_str(), NC_NOWRITE, &temp_ncid)))
                        ERR(retval);            
            if ((retval = nc_inq_varid(temp_ncid, varname[dvar].c_str(), &var_id)))
                        ERR(retval);
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
            nc_close(temp_ncid);
        }//end dvar
        #pragma omp parallel for
        for(int i=0;i<vicnlat;i++){
            float laty = viclatmax - i*viccell - viccell/2.0;
            for(int j=0;j<vicnlont;j++){
                float lontx = viclontmin + j*viccell + viccell/2.0;
                int iloc = i*vicnlont + j; 
                std::vector<std::vector<float> > value;
                //std::vector<std::vector<float> > netcdfvalue;
                value.resize(4);
                //netcdfvalue.resize(4);
                for (int k = 0; k < 4; k++) {
                    value[k].resize(tdays);
                    //netcdfvalue[k].resize(tdays);
                }
                  for (int day = 0; day < tdays; day++) {
                for(int dvar=0;dvar<4;dvar++){
                    value[dvar][day] = 0.0;
                    int validcells = 0;
                    for(int kd=0;kd<9;kd++){
                        //int iloc = i*vicnlont + j;
                        if(vicindex[iloc][kd].row == -1 || vicindex[iloc][kd].col == -1){}
                        else{
                            long iindex = vicindex[iloc][kd].row*nlont*tdays
                                          + vicindex[iloc][kd].col*tdays
                                          + day;
                            //#pragma omp critical
                            //if (tppt[iindex] > 0) std::cerr<<"laty:"<<laty<<" lonx:"<<lontx<<" kd:"<<kd<<" iloc:"<<iloc<<" iindex:"<<iindex<<" day:"<<day<<" ppt:"<<tppt[iindex]<<" tmax:"<<tmax[iindex]<<" tmin:"<<tmin[iindex]<<" vs:"<<vs[iindex]<<std::endl;
                            if (dvar == WIND && year <= 2010) {
                                iindex = day*nlat*nlont
                                         + vicindex[iloc][kd].row*nlont
                                         + vicindex[iloc][kd].col;
                            } else if (year == 2015) {
                                iindex = day*nlat*nlont
                                         + vicindex[iloc][kd].col*nlat
                                         + vicindex[iloc][kd].row;
                            }
                            float temp(-9999.0);
                            float netcdfvalue;
                            switch(dvar){
                            case PPT:
                                temp = tppt[iindex];
                                netcdfvalue = temp;    
                                break;
                            case TMAX:
                                                                temp = tmax[iindex];
                                netcdfvalue = temp - 273.15 ;
                                                                break;
                            case TMIN:
                                                                temp = tmin[iindex];
                                netcdfvalue = temp - 273.15 ;
                                                                break;
                            case WIND:
                                                                temp = vs[iindex];
                                netcdfvalue = temp;
                                                                break;
                            }
                            if(temp > -999.0){
                                validcells++;
                                value[dvar][day] += netcdfvalue/*[dvar][day]*/;
                            }
                        }
                    }//kd
                    if(validcells>0) {
                        value[dvar][day]/=(float)validcells;
                    }
                    else value[dvar][day] = -9999.0;
                    //#pragma omp critical
                    //if (validcells == 9) std::cerr<<"laty:"<<laty<<" lonx:"<<lontx<<" validcells:"<<validcells<<" value:"<<value[dvar][day]<<" dvar:"<<varname[dvar]<<" day:"<<day<<std::endl;
                }//dvar
                  }//day
                //#pragma omp critical
                                //if (value[0][0] > 0) std::cerr<<"laty:"<<laty<<" lonx:"<<lontx<<" value0:"<<value[0][0]<<" value1:"<<value[1][0]<<" value2:"<<value[2][0]<<" value3:"<<value[3][0]<<" day:"<<0<<std::endl;
                /* open the out put file */
                if(value[0][0] >= -999.0 && 
                   value[1][0] >= -999.0 && 
                   value[2][0] >= -999.0 && 
                   value[3][0] >= -999.0){
                    char tempstr[200];
                    sprintf(tempstr,"%sdata_%.5f_%.5f",argv[2],laty,lontx);
                    //#pragma omp critical
                    //std::cerr<<" file:"<<tempstr<<std::endl;
                    FILE *fout;
                    if((fout = fopen(tempstr,"ab+")) == NULL){
                        #pragma omp critical
                        std::cerr<<"can't open binary file"<<tempstr<<std::endl;
                        exit(1);
                    }
                    fseek(fout,0,SEEK_END);
                    for (int day = 0; day < tdays; day++) {
                        unsigned short int ustmp = (unsigned short int)(value[0][day]*multi[0]);
                        fwrite(&ustmp,sizeof(unsigned short int), 1, fout);
                    
                        for(int dvar=1;dvar<4;dvar++){
                            short int stmp = (short int)(value[dvar][day]*multi[dvar]);
                            fwrite(&stmp,sizeof(short int),1,fout);
                        }
                    }//day
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
        free(vs);
        //free(ts);
        for( int i = 0; i < vicnlat*vicnlont; ++i) free(vicindex[i]);
    free(vicindex);
    return 0;
}
