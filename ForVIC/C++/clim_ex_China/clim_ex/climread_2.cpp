#include <iostream>
#include <fstream.h>
#include <stdio.h>
#include <stdlib.h>

#include "climsiterecords.h"

#define REC_NUM 740  //number of climate stations

//#define YEARS 40
//#define MONTHS 12
//#define DAYS 31

#define YEARS 40
#define MONTHS 12
#define DAYS 31
#define STARTYEAR 1961
//temperature decline rate according to elevation  degree per 100 meter
#define TMAX_RATE 0.9
#define TMIN_RATE 0.4
#define TAVG_RATE 0.6

#define PROPCRIS 0.52

//Trancation radius  km
//#define TRANCATION_RADIUS 300.0

#define TRANCATION_MAX 1000.0
#define TRANCATION_MIN3 700.0
#define TRANCATION_MIN2 500.0
#define TRANCATION_MIN1 300.0

//#define TMAX
//#define TMIN
//#define TAVG
//#define PREC
#define CLD
//#define WS
//#define EM
//relative humidity
//#define RHUM

void error(const char* p, const char* p2=" ")
{
	cerr<<p<<' '<<p2<<'\n';
	exit(1);
}

//find the inner id cooresponding to the valid_id in map
int find_id(ClimSiteRecords* clim,int validid)
{
        int i=0;
        while((i < REC_NUM) && (validid != clim[i].clim_id))
        {i++;}
        if(i == 741) i = -1;
        return(i);
}



main(int argc, char* argv[])
{

	ClimSiteRecords climall[REC_NUM];
        //ClimSiteRecords climall;

        int outvalue;      //output value 0.1 mm  0.1 degree 0.1 hour
        double popp,poi,ratius;
	int i,j,k;
        int itempvalue;
        int tempint;
        double tempdouble;
        int climdatafileid,validstations1,validstations2,validstations3;
        char climdatafilename[20];
        char outclimfilename[20];

        int daynum[12] = {31,28,31,30,31,30,31,31,30,31,30,31};

        int intyear,intmon,intday,intid;

        cout<<"Test!..."<<endl;

 	if(argc!=4) error("wrong number of arguments! ==> ","commands <climinfo> <dem> <output>");

	ifstream from(argv[1]);
	if(!from) error("cann't open input file",argv[1]);

        ifstream demdatafile(argv[2]);
        if(!demdatafile) error("cann't open input dem data file",argv[3]);
	//from.setmode(filebuf::binary);

        //initialize the climall i.e., the climate station information
	for(i=0;i<REC_NUM;i++)
	{
             from>>climall[i].id>>climall[i].clim_id>>climall[i].lont>>climall[i].lat;
             from>>tempint;
             climall[i].elev = (double)tempint/10.0;
             from>>climall[i].azoch_elev>>climall[i].f_year>>climall[i].f_mon>>climall[i].t_year>>climall[i].t_mon;
             from>>tempdouble;
             climall[i].x_km = tempdouble/1000.0;
             from>>tempdouble;
             climall[i].y_km = tempdouble/1000.0;
             cout<<climall[i].id<<endl;
       }

        from.close();
        //initialize all the climate data from stations
        //double climate_data[REC_NUM][YEARS][MONTHS][DAYS];
        double ****climate_data;
        climate_data = new double***[REC_NUM];
        cout<<"allocating the climate data space....."<<endl;
        for(i=0;i<REC_NUM;i++)
        {
                climate_data[i] = new double**[YEARS];
                for(intyear=0;intyear<YEARS;intyear++)
                {
                        climate_data[i][intyear] = new double*[MONTHS];
                        for(intmon=0;intmon<MONTHS;intmon++)
                        {
                                climate_data[i][intyear][intmon] = new double[DAYS];
                        }
                }
        }
        cout<<"complet allocation."<<endl;
        for(i=0;i<REC_NUM;i++)
                for(intyear=0;intyear<YEARS;intyear++)
                        for(intmon=0;intmon<MONTHS;intmon++)
                                for(intday=0;intday<DAYS;intday++)
                                climate_data[i][intyear][intmon][intday]=32744.0;

        //read each climate data

        int clima_id,inner_id;
#ifdef TAVG
                sprintf(climdatafilename, "qx_day.txt");
#endif

#ifdef RHUM
                sprintf(climdatafilename, "qx_day.txt");
#endif

#ifdef TMAX
                sprintf(climdatafilename, "ptt.txt");
#endif

#ifdef TMIN
                sprintf(climdatafilename, "ptt.txt");
#endif

#ifdef CLD
                sprintf(climdatafilename, "c_day.txt");
#endif

#ifdef PREC
                sprintf(climdatafilename, "rain_day_6100.txt");
#endif

#ifdef EM
                sprintf(climdatafilename, ".\\em\\em%d.txt",climdatafileid);
#endif

#ifdef WS
                sprintf(climdatafilename, ".\\ws\\ws%d.txt",climdatafileid);
#endif


                ifstream fromdata(climdatafilename);
                if(!fromdata) error("cann't open input climate data file",climdatafilename);

                int t_avg,rh_avg,ws_avg;
                int t_max,t_min,t_delta;
                int pressure;
                int stationid = 0;
                int completed = 0;
                int dtempvalue;
                int c_02,c_04,c_08,c_20,c_t;
                int d_02,d_04,d_08,d_20,d_t;
                while(!fromdata.eof())
                {
#ifdef TAVG
                        fromdata>>intid>>intyear>>intmon>>intday>>t_avg>>rh_avg>>ws_avg;
                        itempvalue = t_avg;
#endif

#ifdef TMAX
                        fromdata>>intid>>intyear>>intmon>>intday>>pressure>>t_max>>t_min>>t_delta;
                        itempvalue = t_max;
#endif

#ifdef TMIN
                        fromdata>>intid>>intyear>>intmon>>intday>>pressure>>t_max>>t_min>>t_delta;
                        itempvalue = t_min;
#endif


#ifdef RHUM
                        fromdata>>intid>>intyear>>intmon>>intday>>t_avg>>rh_avg>>ws_avg;
                        itempvalue = rh_avg;
#endif



#ifdef PREC
                        fromdata>>intid>>intyear>>intmon>>intday>>tempdouble;
                        itempvalue = (int)tempdouble;
#endif

#ifdef CLD
                        fromdata>>intid>>intyear>>intmon>>intday>>c_02>>c_04>>c_08>>c_20>>c_t>>d_02>>d_04>>d_08>>d_20>>d_t;
                        //fromdata;

                        itempvalue = (int)(c_t * 100);
                        if(itempvalue>1000) itempvalue = 32744;
#endif

                        if(intid!=stationid){
                                inner_id = find_id(climall,intid);
                                stationid = intid;
                                cout<<completed<<" complete!"<<stationid<<endl;
                                completed++;
                        }

                        if((itempvalue == 32744) || (itempvalue == 32766)) dtempvalue = 32744.0;
                        else if(itempvalue > 30000) dtempvalue = 0.1;
                        else dtempvalue = (double)(itempvalue)/10.0;
                        if(intyear>=STARTYEAR&&inner_id!=-1&&intyear<=2000){
                                //cout<<inner_id<<" "<<intyear-STARTYEAR<<" "<<intmon-1<<" "<<intday-1<<endl;
                                 climate_data[inner_id][intyear-STARTYEAR][intmon-1][intday-1]=dtempvalue;
                        }
                }
                fromdata.close();

        cout<<endl<<"Reading dem data ... ..."<<endl;

        int line=4053;
        int pixel=4848;
        int xllcorner=-2638000;	//Lower Left  Corner E
        int yllcorner=1870000;	//Lower Left  Corner N
        int cellsize=1000;
        int nodata_value=-9999;
        int demdata;

	demdatafile>>"NCOLS ">>pixel;
	demdatafile>>"NROWS ">>line;
	demdatafile>>"XLLCORNER ">>xllcorner;
	demdatafile>>"YLLCORNER ">>yllcorner;
	demdatafile>>"CELLSIZE ">>cellsize;
	demdatafile>>"NODATA_value ">>nodata_value;

        double **dem;
        dem = new double*[line];
        for(i=0;i<line;i++) dem[i] = new double[pixel];
        for(i=0;i<line;i++)
                for(j=0;j<pixel;j++)
                {
                        demdatafile>>demdata;
                        dem[i][j] = (double)demdata;
                }
        demdatafile.close();

        //define the valid clim site collections
        ValidClimData validclimsite[REC_NUM];
        int validclimnum = 0;

        double p_xcor,p_ycor,wi,sitex,sitey,distp,wall,valueall;
        const double alfa = 3.0;

//        for(intyear=0;intyear<YEARS;intyear++)
//                for(intmon=0;intmon<MONTHS;intmon++)
//                        for(intday=0;intday<DAYS;intday++)

        cout<<endl<<"Starting processing..."<<endl;
        for(intyear=0;intyear<40;intyear++)
                for(intmon=0;intmon<MONTHS;intmon++)
                        for(intday=0;intday<daynum[intmon];intday++)
                        {
                                validclimnum=0;
                                for(i=0;i<REC_NUM;i++)
                                {
                                        if(climate_data[i][intyear][intmon][intday] != 32744.0)
                                        {
                                                validclimsite[validclimnum].inner_id = i;
                                                validclimsite[validclimnum].value = climate_data[i][intyear][intmon][intday];
                                                validclimnum++;
                                        }
                                }

                                //sprintf(outclimfilename,"%s%dm%dd%d.txt",argv[4],intyear+STARTYEAR,intmon+1,intday+1);
                                sprintf(outclimfilename,"%s%dm%dd%d.txt",argv[3],intyear+STARTYEAR,intmon+1,intday+1);
                        	ofstream to(outclimfilename);
	                        if(!to) error("cann't open output file",outclimfilename);

                                to<<"NCOLS "<<pixel<<endl;
	                        to<<"NROWS "<<line<<endl;
	                        to<<"XLLCORNER "<<xllcorner<<endl;
	                        to<<"YLLCORNER "<<yllcorner<<endl;
	                        to<<"CELLSIZE "<<cellsize<<endl;
	                        to<<"NODATA_value "<<nodata_value<<endl;

                                //start process all the grid data
                                for(i=0;i<line;i++)
                                        {
                                        //cout<<"complete %"<<i*100/line;
                                        for(j=0;j<pixel;j++)
                                        {
                                                wall = 0.0;
                                                valueall = 0.0;
                                                popp = 0.0;

                                                validstations1 = 0;
                                                validstations2 = 0;
                                                validstations3 = 0;

                                                for(k=0;k<validclimnum;k++)
                                                {
                                                        p_xcor = (j*cellsize + xllcorner)/1000.0; //cell cor (km)
                                                        p_ycor = (yllcorner + (line-i-1)*cellsize)/1000.0;
                                                        sitex = climall[validclimsite[k].inner_id].x_km;
                                                        sitey = climall[validclimsite[k].inner_id].y_km;
                                                        distp = sqrt((sitex-p_xcor)*(sitex-p_xcor)+(sitey-p_ycor)*(sitey-p_ycor));
                                                        if(distp<=TRANCATION_MIN1) validstations1++;
                                                        if(distp<=TRANCATION_MIN2) validstations2++;
                                                        if(distp<=TRANCATION_MIN3) validstations3++;
                                                }
                                                ratius = TRANCATION_MAX;
                                                if(validstations1>=4) ratius = TRANCATION_MIN1;
                                                if(validstations2>=4 && validstations1<4) ratius = TRANCATION_MIN2;
                                                if(validstations3>=4 && validstations2<4) ratius = TRANCATION_MIN3;
                                                

                                                for(k=0;k<validclimnum;k++)
                                                {
                                                        p_xcor = (j*cellsize + xllcorner)/1000.0; //cell cor (km)
                                                        p_ycor = (yllcorner + (line-i-1)*cellsize)/1000.0;
                                                        sitex = climall[validclimsite[k].inner_id].x_km;
                                                        sitey = climall[validclimsite[k].inner_id].y_km;
                                                        distp = sqrt((sitex-p_xcor)*(sitex-p_xcor)+(sitey-p_ycor)*(sitey-p_ycor));

                                                        if(distp>ratius) wi = 0.0;   //Trancation radius 1000km
                                                        else wi = exp((-1.0)*(distp/ratius)*(distp/ratius)*alfa)-exp((-1.0)*alfa);

                                                        wall+=wi;

                                        #ifdef PREC
                                                        if(validclimsite[k].value>0.0) poi = 1.0;
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

                                         #ifdef CLD
                                                        dtempvalue = validclimsite[k].value;
                                         #endif

                                         #ifdef RHUM
                                                        dtempvalue = validclimsite[k].value;
                                         #endif


                                                        //valueall+=wi*validclimsite[k].value;

                                                        valueall+=wi*dtempvalue;  //dem affected

                                                        
                                                }

                                                if(wall>0.0) outvalue = (int)((valueall*10)/wall);
                                                else outvalue = -9999;

                                         #ifdef PREC
                                                if(wall > 0.0) popp =  popp / wall;
                                                else popp = 0.0;
                                                if(popp<PROPCRIS && wall>0.0) outvalue = 0.0;
                                         #endif

                                                to<<outvalue<<" ";
                                        }
                                        to<<endl;
                                        //cout<<"complete %"<<i*100/line<<endl;
                                        }
                                to.close();
                                printf("year:%d mon:%d day:%d\n",intyear+STARTYEAR,intmon+1,intday+1);
                        }



        //delete the allocations for clim
        for(i=0;i<REC_NUM;i++)
        {
                for(intyear=0;intyear<YEARS;intyear++)
                {
                        for(intmon=0;intmon<MONTHS;intmon++)
                        {
                                delete[] climate_data[i][intyear][intmon];
                        }
                        delete[] climate_data[i][intyear];
                }
                delete[] climate_data[i];
        }
        delete[] climate_data;

        //delete dem data
        for(i=0;i<line;i++)
                delete[] dem[i];
        delete[] dem;


}

