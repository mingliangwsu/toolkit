#include <stdio.h>
#include <iostream>
#include <iomanip>
#include <fstream>
#include "esrigridclass.h"
#include "time_tools.h"
#ifndef _LEAPYR
#define LEAPYR(y) (!((y)%400) || (!((y)%4) && ((y)%100)))
#endif
float get_average_from_binary_file(std::string filename,
                                    int from_year, int to_year,
                                    float &avg_ppt, float &avg_tmax,
                                    float &avg_tmin, float &avg_tair,
                                    float &avg_wind);
int main(int argc, char *argv[])
{
    float avg_ppt, avg_tmax, avg_tmin, avg_tair, avg_wind;

    if(argc < 6) std::cerr << "wrong number of arguments! ==> "
                           << "<1. CRB ascii>\n"
                           << "<2.start_year>\n "
                           << "<3.end_year>\n "
                           << "<4.climate_path_no_slash>\n "
                           << "<5.out_path_no_slash\n";

    EsriGridClass<double> crbbnd;
    std::string crbbnd_name(argv[1]);
    int from_year = atoi(argv[2]);
    int to_year = atoi(argv[3]);
    std::string clm_path(argv[4]);
    std::string out_path(argv[5]);

    crbbnd.readAsciiGridFile(crbbnd_name);
    enum {OUT_TMAX,OUT_TMIN,OUT_TAVG,OUT_WIND,OUT_PPT,count_of_out};
    std::string out_vars_name[count_of_out] =
        {"out_tmax","out_tmin","out_tavg","out_wind","out_ppt"};
    EsriGridClass<double> out_grid[count_of_out];
    for (int outvar = OUT_TMAX; outvar < count_of_out; outvar++) {
        out_grid[outvar].CopyHeadInformation(crbbnd);
        out_grid[outvar].AllocateMem();
    }
    for (int row = 0; row < crbbnd.getNrows(); row++) {
        float ycor = crbbnd.getGridYll(row) + crbbnd.getCellsize() / 2.0;        //center
        for (int col = 0; col < crbbnd.getNcols(); col++) {
            if (crbbnd.IsValidCell(row,col)) {
                float xcor = crbbnd.getGridXll(col) + crbbnd.getCellsize() / 2.0; //center
                char filename[300];
                sprintf(filename,"%s/data_%.5f_%.5f",clm_path.c_str(),ycor,xcor);
                std::string bin_file_name(filename);
                float return_value = get_average_from_binary_file(filename
                                             ,from_year,to_year
                                             ,avg_ppt,avg_tmax,avg_tmin
                                             ,avg_tair,avg_wind);
                if (return_value >= 0.0) {
                    out_grid[OUT_TMAX].setValue(row,col,avg_ppt);
                    out_grid[OUT_TMIN].setValue(row,col,avg_tmin);
                    out_grid[OUT_TAVG].setValue(row,col,avg_tmax);
                    out_grid[OUT_WIND].setValue(row,col,avg_wind);
                    out_grid[OUT_PPT].setValue(row,col,avg_ppt);
                }
            }
        }
    }
    for (int outvar = OUT_TMAX; outvar < count_of_out; outvar++) {
        out_grid[outvar].writeAsciiGridFile(out_path + "/"
                                            + out_vars_name[outvar]
                                            + "_"
                                            + std::to_string(from_year)
                                            + "_"
                                            + std::to_string(to_year)
                                            + ".asc");
    }
    //std::string bin_file_name("data_49.09375_-122.71875");
    //get_average_from_binary_file(bin_file_name,start_year,2015,avg_ppt,
     //                            avg_tmax, avg_tmin, avg_tair, avg_wind);
    return 0;
}
//______________________________________________________________________________
float get_average_from_binary_file(std::string filename,
                                    int from_year, int to_year,
                                    float &avg_ppt, float &avg_tmax,
                                    float &avg_tmin, float &avg_tair,
                                    float &avg_wind)
{
    const int clm_start_year = 1979;
    FILE *binf = fopen(filename.c_str(), "rb");
    //enum {PPT,TMAX,TMIN,WIND,SPH,SRAD,RMAX,RMIN,count_of_vars};
    //float multi[count_of_vars] = {40,100,100,100,10000,40,100,100};
    enum {PPT,TMAX,TMIN,WIND,count_of_vars};
    float multi[count_of_vars] = {40,100,100,100};
    if (binf == NULL) return -1;                                                   //nrerror("No data in the forcing file.  Model stopping...");

    fseek(binf,0,SEEK_SET);
    const int days_to_skip = get_days_between_year_with_leaps(clm_start_year,from_year-1);
    const int vars = count_of_vars;
    const int size_of_var = sizeof(short int);
    size_t bin_to_skip = days_to_skip * vars * size_of_var;

    fseek(binf,bin_to_skip,SEEK_SET);
    //float ppt,tmax,tmin,wind,sph,srad,rmax,rmin;
    float fvalue[count_of_vars];
    float avgfvalue[count_of_vars];
    unsigned short int ustmp;
    short int stmp[count_of_vars];
    int total_days = 0;
    for (int var = PPT; var < count_of_vars; var++) {
        avgfvalue[var] = 0.0;
    }

    for(int year = from_year; year <= to_year; year++) {
        int days = LEAPYR(year) ? 366 : 365;

        for (int day = 0; day < days; day++) {
            fread(&ustmp,sizeof(unsigned short int),1,binf);
            fvalue[PPT] = (float) (ustmp / multi[PPT]);
            avgfvalue[PPT] += fvalue[PPT];
            for (int var = TMAX; var < count_of_vars; var++) {
                fread(&stmp[var],sizeof(short int),1,binf);
                fvalue[var] = (float) (stmp[var] / multi[var]);
                avgfvalue[var] += fvalue[var];
            }

            /*
            std::cout << "year:"    << year
                      << "\tday:"   << day
                      << "\tPPT:"   << fvalue[PPT]
                      << "\tTMAX:"  << fvalue[TMAX]
                      << "\tTMIN:"  << fvalue[TMIN]
                      << "\tWIND:"  << fvalue[WIND]
                      //<< "\tSPH:"   << fvalue[SPH]
                      //<< "\tSRAD:"  << fvalue[SRAD]
                      //<< "\tRMAX:"  << fvalue[RMAX]
                      //<< "\tRMIN:"  << fvalue[RMIN]
                      << std::endl;*/
            total_days++;
        }
    }
    avg_ppt = (avgfvalue[PPT] / (float)total_days) * 365.25;
    avg_tmax = avgfvalue[TMAX] / (float)total_days;
    avg_tmin = avgfvalue[TMIN] / (float)total_days;
    avg_tair = (avg_tmax + avg_tmin) / 2.0;
    avg_wind = avgfvalue[WIND] / (float)total_days;
    fclose(binf);
    return 0;
}
