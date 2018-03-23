#include <iostream>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "esrigridclass.h"
#include "pubtools.h"
#include "climsiterecords.h"
#include "time_tools.h"

#define REC_NUM 756  //number of climate stations

#define MONTHS 12
#define DAYS 31
#define STARTYEAR 1961
#define ENDYEAR 2015
#define YEARS (ENDYEAR - STARTYEAR + 1)
//temperature decline rate according to elevation  degree per 100 meter
#define TMAX_RATE 0.9
#define TMIN_RATE 0.4
#define TAVG_RATE 0.6

#define PROPCRIS 0.52
#define NODATA 32766

//Trancation radius  km
//#define TRANCATION_RADIUS 300.0

//#define TRANCATION_MAX 1000.0
//#define TRANCATION_MIN3 700.0
//#define TRANCATION_MIN2 500.0
//#define TRANCATION_MIN1 300.0

#define TRANCATION_MAX 500.0
#define TRANCATION_MIN3 500.0
#define TRANCATION_MIN2 500.0
#define TRANCATION_MIN1 500.0

//#define TMAX
//#define TMIN
//#define TAVG
//#define PREC
//#define CLD
#define WS
//#define EM
//relative humidity
//#define RHUM

void error(const char* p, const char* p2=" ")
{
    std::cerr<<p<<' '<<p2<<'\n';
    exit(1);
}
//find the inner id cooresponding to the valid_id in map
int find_id(ClimSiteRecords* clim,int validid)
{
    int i=0;
    while((i < REC_NUM) && (validid != clim[i].clim_id)) i++;
    if(i == REC_NUM) i = -1;
    return(i);
}
//______________________________________________________________________________
int main(int argc, char* argv[])
{
    if(argc < 5) error("wrong number of arguments! ==> ",
                       "commands <climinfo> <dem> <input_dir> <output_dir>");
    std::ifstream from(argv[1]);
    if(!from) error("cann't open input file",argv[1]);
    EsriGridClass<float> dem;
    dem.readAsciiGridFile(argv[2]);
    std::string input_dir(argv[3]);
    std::string output_dir(argv[4]);
    ClimSiteRecords climall[REC_NUM];

    std::cout<<"Test!..."<<std::endl;

    //initialize the climall i.e., the climate station information
    for (int i = 0; i < REC_NUM; i++)
    {
        int tempint;
        double tempdouble;
        from>>climall[i].id>>climall[i].clim_id>>climall[i].lont>>climall[i].lat;
        from>>tempint;
        climall[i].elev = (double)tempint/10.0;
        from>>climall[i].azoch_elev>>climall[i].f_year>>climall[i].f_mon>>climall[i].t_year>>climall[i].t_mon;
        from>>tempdouble;
        climall[i].x_km = tempdouble/1000.0;
        from>>tempdouble;
        climall[i].y_km = tempdouble/1000.0;
        std::cout<<climall[i].id<<std::endl;
    }
    from.close();
    //initialize all the climate data from stations
    //double climate_data[REC_NUM][YEARS][MONTHS][DAYS];
    double ****climate_data;
    climate_data = new double***[REC_NUM];
    std::cout<<"allocating the climate data space....."<<std::endl;
    for (int i = 0; i < REC_NUM; i++)
    {
        climate_data[i] = new double**[YEARS];
        for (int intyear = 0; intyear < YEARS; intyear++)
        {
            climate_data[i][intyear] = new double*[MONTHS];
            for (int intmon = 0; intmon < MONTHS; intmon++)
            {
                climate_data[i][intyear][intmon] = new double[DAYS];
            }
        }
    }
    std::cout<<"complet allocation."<<std::endl;
    for (int i = 0; i < REC_NUM; i++)
        for (int intyear = 0; intyear < YEARS; intyear++)
            for (int intmon = 0; intmon < MONTHS; intmon++)
                for (int intday = 0; intday < DAYS; intday++)
                    climate_data[i][intyear][intmon][intday]=-9999.0;
    //read each climate data
    for (int intyear = 0; intyear < YEARS; intyear++) {
        std::clog << "Year:" << (intyear + STARTYEAR) << std::endl;
        for (int intmon = 0; intmon < MONTHS; intmon++) {
            char climfilename[1024];
            sprintf(climfilename,"%s/SURF_CLI_CHN_MUL_DAY-WIN-11002-%d%02d.txt",
                    input_dir.c_str(), (intyear + STARTYEAR), (intmon + 1));
            std::ifstream fromdata(climfilename);
            if(!fromdata) error("cann't open input climate data file",climfilename);
            int id, lat, lon, elev, year, mon, day, tavg, tmax, tmin, wind
                ,wdir, idump;
            while(!fromdata.eof()) {
                id = -9999;
                fromdata>>id>>lat>>lon>>elev>>year>>mon>>day>>tavg>>tmax>>tmin>>wind>>wdir>>idump>>idump>>idump>>idump>>idump;
                if (id != -9999) {
                    int inner_id = find_id(climall,id);
                    if (inner_id >= 0) {
#ifdef WS
                        if (wind != NODATA) {
                            climate_data[inner_id][intyear][intmon][day-1] = (double)wind / 10.0;
                            //std::clog << "wind:" << climate_data[inner_id][intyear][intmon][day-1]
                            //          << std::endl;
                        }
#endif
                    }
                }
            }
            fromdata.close();
        }
    }

    std::clog << "Finishing reading climate data.\n";
    double p_xcor,p_ycor,wi,sitex,sitey,distp,wall,valueall;
    const double alfa = 3.0;
    ValidClimData validclimsite[REC_NUM];
    std::cout<<"\nStarting interpolating processing...\n";
    for (int intyear = 0; intyear < YEARS; intyear++) {
        int *daynum = LEAPYR(intyear + STARTYEAR) ?
                      monthdays_leap : monthdays_normal;
        for (int intmon = 0; intmon < MONTHS; intmon++) {
            for (int intday = 0; intday < daynum[intmon]; intday++) {
                int validclimnum = 0;
                for (int i = 0; i < REC_NUM; i++) {
                    if(climate_data[i][intyear][intmon][intday] != -9999.0) {
                        validclimsite[validclimnum].inner_id = i;
                        validclimsite[validclimnum].value = climate_data[i][intyear][intmon][intday];
                        /*
                        std::clog << "\tyear:" << (intyear + STARTYEAR)
                                  << "\tmon:" << (intmon + 1)
                                  << "\tday:" << (intday + 1)
                                  << "\tinner_id:" << i
                                  << "\tstation:" << climall[i].id
                                  << "\tvalidclimsite:" << validclimsite[validclimnum].value
                                  << std::endl;
                        */
                        validclimnum++;
                    }
                }
                char outclimfilename[1024];
                sprintf(outclimfilename,"%s/y%dm%dd%d.asc",output_dir.c_str(),
                        intyear+STARTYEAR, intmon+1, intday+1);
                EsriGridClass<float> to;
                to.CopyHeadInformation(dem);
                to.setNodataValue(-9999.0);
                to.AllocateMem();
                //start process all the grid data
                int line = to.getNrows();
                int pixel = to.getNcols();
                float cellsize = to.getCellsize();
                float xllcorner = to.getXll();
                float yllcorner = to.getYll();
                #pragma omp parallel for
                for (int i = 0; i < line; i++) {
                    //std::cout<<"complete %"<<i*100/line;
                    for( int j = 0; j < pixel;j++)
                    {
                        double wall = 0.0;
                        double valueall = 0.0;
                        double popp = 0.0;
                        int validstations1 = 0;
                        int validstations2 = 0;
                        int validstations3 = 0;
                        for (int k = 0; k < validclimnum; k++) {
                            double p_xcor = (j*cellsize + xllcorner)/1000.0; //cell cor (km)
                            double p_ycor = (yllcorner + (line-i-1)*cellsize)/1000.0;
                            double sitex = climall[validclimsite[k].inner_id].x_km;
                            double sitey = climall[validclimsite[k].inner_id].y_km;
                            double distp = sqrt((sitex-p_xcor)*(sitex-p_xcor)+(sitey-p_ycor)*(sitey-p_ycor));
                            if(distp<=TRANCATION_MIN1) validstations1++;
                            if(distp<=TRANCATION_MIN2) validstations2++;
                            if(distp<=TRANCATION_MIN3) validstations3++;
                        }
                        double ratius = TRANCATION_MAX;
                        if(validstations1 >= 4) ratius = TRANCATION_MIN1;
                        else if(validstations2 >= 4 && validstations1<4) ratius = TRANCATION_MIN2;
                        else if(validstations3 >= 4 && validstations2<4) ratius = TRANCATION_MIN3;
                        for (int k = 0; k < validclimnum; k++) {
                            double p_xcor = (j*cellsize + xllcorner)/1000.0; //cell cor (km)
                            double p_ycor = (yllcorner + (line-i-1)*cellsize)/1000.0;
                            double sitex = climall[validclimsite[k].inner_id].x_km;
                            double sitey = climall[validclimsite[k].inner_id].y_km;
                            double distp = sqrt((sitex-p_xcor)*(sitex-p_xcor)+(sitey-p_ycor)*(sitey-p_ycor));
                            double wi = 0;
                            if (distp > ratius) wi = 0.0;   //Trancation radius 1000km
                            else wi = exp((-1.0)*(distp/ratius)*(distp/ratius)*alfa)-exp((-1.0)*alfa);
                            wall += wi;
                            double dtempvalue;
                            #ifdef PREC
                            if(validclimsite[k].value > 0.0) poi = 1.0;
                            else poi = 0.0;
                            popp += wi * poi;
                            dtempvalue = validclimsite[k].value;
                            #endif
                            //only related location
                            //dtempvalue = validclimsite[k].value - (dem[i][j]-climall[validclimsite[k].inner_id].elev_s)*TMIN_RATE*0.01;
                            #ifdef TAVG
                            dtempvalue = validclimsite[k].value - (dem[i][j]-climall[validclimsite[k].inner_id].elev)*TAVG_RATE*0.01;
                            #endif
                            #ifdef TMAX
                            dtempvalue = validclimsite[k].value - (dem[i][j]-climall[validclimsite[k].inner_id].elev)*TMAX_RATE*0.01;
                            #endif
                            #ifdef TMIN
                            dtempvalue = validclimsite[k].value - (dem[i][j]-climall[validclimsite[k].inner_id].elev)*TMIN_RATE*0.01;
                            #endif
                            #if (defined(CLD) || defined(RHUM) || defined(WS))
                            dtempvalue = validclimsite[k].value;
                            #endif
                            valueall += wi*dtempvalue;  //dem affected
                        } //k
                        double outvalue;
                        if(wall > 0.0) outvalue = valueall / wall;
                        else outvalue = -9999.0;
                        #ifdef PREC
                        if(wall > 0.0) popp =  popp / wall;
                        else popp = 0.0;
                        if(popp<PROPCRIS && wall>0.0) outvalue = 0.0;
                        #endif
                        to.setValue(i,j,outvalue);
                    } //j
                } //i
                to.writeAsciiGridFile(outclimfilename);
                std::clog << "year:" << (intyear+STARTYEAR)
                          << "\tmon:" << (intmon+1)
                          << "\tday:" << (intday+1)
                          << std::endl;
            } //intday
        } //int mon
    } //int year
    //delete the allocations for clim
    for (int i = 0; i < REC_NUM; i++)
    {
            for (int intyear = 0; intyear < YEARS; intyear++)
            {
                    for (int intmon=0;intmon<MONTHS;intmon++)
                    {
                            delete[] climate_data[i][intyear][intmon];
                    }
                    delete[] climate_data[i][intyear];
            }
            delete[] climate_data[i];
    }
    delete[] climate_data;
}

