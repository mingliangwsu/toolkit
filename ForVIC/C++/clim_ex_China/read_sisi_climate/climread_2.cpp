#include <iostream>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <iomanip>
#include "esrigridclass.h"
#include "pubtools.h"
#include "climsiterecords.h"
#include "time_tools.h"


//#define TMAX
//#define TMIN
//#define TAVG
//#define PREC
//#define CLD
//#define WS
//#define EM
//relative humidity
//#define RHUM
#define TMAX
//#define TMIN
//#define TAVG

#define ESTIMATE_LAPSE_RATE

#if (defined(TMAX) || defined(TMIN) || defined(TAVG))
#include "ap.h"
#include "dataanalysis.h"
#endif

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

//6.49K/1000m international standard atmosphere (ISA)
#define CONST_LAPSE_RATE -0.00649


#define PROPCRIS 0.52

#define BLANK 32744
#define NODATA 32766
#define MINORVALUE 32700

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
#ifdef ESTIMATE_LAPSE_RATE
    double lapse_rate[YEARS][12];
#endif

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
#ifdef WS
            sprintf(climfilename,"%s/SURF_CLI_CHN_MUL_DAY-WIN-11002-%d%02d.txt",
                    input_dir.c_str(), (intyear + STARTYEAR), (intmon + 1));
#elif defined(PREC)
            sprintf(climfilename,"%s/SURF_CLI_CHN_MUL_DAY-PRE-13011-%d%02d.txt",
                    input_dir.c_str(), (intyear + STARTYEAR), (intmon + 1));
#elif (defined(TMAX) || defined(TMIN) || defined(TAVG))
            sprintf(climfilename,"%s/SURF_CLI_CHN_MUL_DAY-TEM-12001-%d%02d.txt",
                    input_dir.c_str(), (intyear + STARTYEAR), (intmon + 1));
#endif
            std::ifstream fromdata(climfilename);
            if(!fromdata) error("cann't open input climate data file",climfilename);
            int id, lat, lon, elev, year, mon, day, idump;
#ifdef WS
            int wtavg, wtmax, wtmaxdir, windmax
                ,windmaxdir;
#elif defined(PREC)
            int ppt_night, ppt_day, ppt_allday;
#elif (defined(TMAX) || defined(TMIN) || defined(TAVG))
            int tavg,tmax,tmin;
#endif
            while(!fromdata.eof()) {
                id = -9999;
#ifdef WS
                fromdata>>id>>lat>>lon>>elev>>year>>mon>>day>>wtavg>>wtmax>>wtmaxdir>>windmax>>windmaxdir>>idump>>idump>>idump>>idump>>idump;
#elif defined(PREC)
                fromdata>>id>>lat>>lon>>elev>>year>>mon>>day>>ppt_night>>ppt_day>>ppt_allday>>idump>>idump>>idump;
#elif (defined(TMAX) || defined(TMIN) || defined(TAVG))
                fromdata>>id>>lat>>lon>>elev>>year>>mon>>day>>tavg>>tmax>>tmin>>idump>>idump>>idump;
#endif
                if (id != -9999) {
                    int inner_id = find_id(climall,id);
                    if (inner_id >= 0) {
                        int data
#ifdef WS
                            = wtavg;
#elif defined(PREC)
                            = ppt_allday;
#elif defined(TMAX)
                            = tmax;
#elif defined(TAVG)
                            = tavg;
#elif defined(TMIN)
                            = tmin;
#endif
                        if (data != NODATA && data != BLANK) {
                            if (data == MINORVALUE) data = 0;
#ifdef WS
                            if (data > 1000) data -= 1000;
#elif defined(PREC)
                            if (data >= 30000 && data < 31000) data -= 30000;
                            else if (data >= 31000 && data < 32000) data -= 31000;
                            else if (data >= 32000) data -= 32000;
#endif
                            climate_data[inner_id][intyear][intmon][day-1] = (double)data / 10.0;
                            //std::clog << "wind:" << climate_data[inner_id][intyear][intmon][day-1]
                            //          << std::endl;
                        }
                    }
                }
            }
            fromdata.close();
        }
    }

    std::clog << "Finishing reading climate data.\n";

#if ((defined(TMAX) || defined(TMIN) || defined(TAVG)) && (defined(ESTIMATE_LAPSE_RATE)))
    std::string outlpse,outlpse_mon;
#ifdef TMAX
    outlpse = "/home/liuming/data/climate_from_Sisi/estimated_laprate_tmax.txt";
    outlpse_mon = "/home/liuming/data/climate_from_Sisi/estimated_laprate_tmax_mon.txt";
#elif defined(TAVG)
    outlpse = "/home/liuming/data/climate_from_Sisi/estimated_laprate_tavg.txt";
    outlpse_mon = "/home/liuming/data/climate_from_Sisi/estimated_laprate_tavg_mon.txt";
#else
    outlpse = "/home/liuming/data/climate_from_Sisi/estimated_laprate_tmin.txt";
    outlpse_mon = "/home/liuming/data/climate_from_Sisi/estimated_laprate_tmin_mon.txt";
#endif
    std::ofstream flaps(outlpse);
    std::ofstream flaps_mon(outlpse_mon);
#endif

    double p_xcor,p_ycor,wi,sitex,sitey,distp,wall,valueall;
    const double alfa = 3.0;
    ValidClimData validclimsite[REC_NUM];
    std::cout<<"\nStarting interpolating processing...\n";

#ifdef ESTIMATE_LAPSE_RATE
    for (int intyear = 0; intyear < YEARS; intyear++) {
        int *daynum = LEAPYR(intyear + STARTYEAR) ?
                      monthdays_leap : monthdays_normal;
        for (int intmon = 0; intmon < MONTHS; intmon++) {
            lapse_rate[intyear][intmon] = 0.0;
            for (int intday = 0; intday < daynum[intmon]; intday++) {
                int validclimnum = 0;
                for (int i = 0; i < REC_NUM; i++) {
                    if(climate_data[i][intyear][intmon][intday] != -9999.0) {
                        validclimsite[validclimnum].inner_id = i;
                        validclimsite[validclimnum].value = climate_data[i][intyear][intmon][intday];
                        validclimnum++;
                    }
                } //i
                //Estimate the global lapse rate with linear regression model
                alglib_impl::ae_matrix xy;
                alglib_impl::ae_int_t n = 3;                                     //lat, lon, elev
                alglib_impl::ae_int_t info;
                alglib_impl::linearmodel wt;
                alglib_impl::lrreport ar;
                alglib_impl::ae_state _state;
                alglib_impl::ae_vector coef;
                ae_matrix_init(&xy, 0, 0, alglib_impl::DT_REAL, &_state);
                ae_vector_init(&coef, 0, alglib_impl::DT_REAL, &_state);
                ae_matrix_set_length(&xy,validclimnum, n+1, &_state);
                _linearmodel_init(&wt, &_state);
                _lrreport_init(&ar, &_state);
                for (int k = 0; k < validclimnum; k++) {
                    int id = validclimsite[k].inner_id;
                    xy.ptr.pp_double[k][0] = climall[id].lat;
                    xy.ptr.pp_double[k][1] = climall[id].lont;
                    xy.ptr.pp_double[k][2] = climall[id].elev;
                    xy.ptr.pp_double[k][3] = validclimsite[k].value;
                    /*std::clog << "id:"          << climall[id].clim_id
                              << "\t[lat]:"    << climall[id].lat
                              << "\t[lon]:"    << climall[id].lont
                              << "\t[elev]:"   << climall[id].elev
                              << "\t[data]:"   << validclimsite[k].value
                              << std::endl;*/
                }
                lrbuild(&xy, validclimnum, n, &info, &wt, &ar, &_state);
                lrunpack(&wt,&coef,&n,&_state);
                /*std::clog << "info:"        << info
                          << "\tw[lat]:"    << coef.ptr.p_double[0]
                          << "\tw[lon]:"    << coef.ptr.p_double[1]
                          << "\tw[elev]:"   << coef.ptr.p_double[2]
                          << "\tw[resid]:"  << coef.ptr.p_double[3]
                          << std::endl;*/
                flaps     << "year:"        << (intyear + STARTYEAR)
                          << "\tmon:"         << intmon
                          << "\tday:"         << intday
                          << "\tw[elev]:"   << coef.ptr.p_double[2]
                          << std::endl;
                lapse_rate[intyear][intmon] += coef.ptr.p_double[2];
                ae_matrix_destroy(&xy);
                _linearmodel_destroy(&wt);
                _lrreport_destroy(&ar);
                ae_vector_destroy(&coef);
            } //intday
            lapse_rate[intyear][intmon] /= (double)daynum[intmon];
            flaps_mon << "year:"        << (intyear + STARTYEAR)
                      << "\tmon:"       << intmon
                      << "\tlapsrate:"  << lapse_rate[intyear][intmon]
                      << std::endl;
        } //int mon
    } //int year
#endif


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
                } //i
                char outclimfilename[1024];
                sprintf(outclimfilename,"%s/y%dm%dd%d.asc",output_dir.c_str(),
                        intyear+STARTYEAR, intmon+1, intday+1);
                std::ofstream outf(outclimfilename);
                if (!outf) {
                    std::cerr << "Can't open file " << outclimfilename << std::endl;
                    exit(0);
                }
                for (int k = 0; k < validclimnum; k++) {
                    int id = validclimsite[k].inner_id;
                    double outvalue = validclimsite[k].value;
#if (defined(TMAX) || defined(TMIN) || defined(TAVG))
#ifdef ESTIMATE_LAPSE_RATE
                    outvalue -= climall[id].elev * lapse_rate[intyear][intmon];
#else
                    outvalue -= climall[id].elev * CONST_LAPSE_RATE;
#endif
#endif
                    outf << climall[id].clim_id
                         << ","
                         << std::fixed
                         << std::setprecision(1)
                         << (climall[id].x_km * 1000.0)
                         << ","
                         << std::fixed
                         << std::setprecision(1)
                         << (climall[id].y_km * 1000.0)
                         << ","
                         << std::fixed
                         << std::setprecision(1)
                         << outvalue
                         << std::endl;
                } //k
                outf << "end\n";
                outf.close();
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
#if (defined(TMAX) || defined(TMIN) || defined(TAVG))
    flaps.close();
    flaps_mon.close();
#endif
    std::clog << "\nDone!\n";
}

