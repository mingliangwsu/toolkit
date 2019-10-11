#include <stdio.h>
#include <iostream>
#include <iomanip>
#include <fstream>
#include "time_tools.h"
#ifndef _LEAPYR
#define LEAPYR(y) (!((y)%400) || (!((y)%4) && ((y)%100)))
#endif
int get_average_from_binary_file(std::string filename,
                                    int from_year, int to_year,
                                    float ** avgdata);

const int clm_start_year = 1915;
const int clm_end_year = 2015;
enum clmvar {VIC_PPT,VIC_TMAX,VIC_TMIN,VIC_WIND,VIC_QAIR, VIC_SHORTWAVE, VIC_RHUM_MAX, VIC_RHUM_MIN, count_of_vars};
std::string out_vars_name[count_of_vars] =
    {"PPT","TMAX","TMIN","WIND","QAIR", "SHORTWAVE", "RHUM_MAX","RHUM_MIN"};
float multi[count_of_vars] = {40, 100, 100, 100, 10000, 40, 100, 100};
int cell = 0;

int main(int argc, char *argv[])
{
    float **monthly_avg  = alloc_2d_array<float>(count_of_vars,12,"average");

    if(argc == 1) std::cerr << " Usage:" << argv[0] << " "
                           << "<1.binary_dir_no_slash> "
                           << "<2.out_filename> "
                           << "<3.xmin> "
                           << "<4.ymin> "
                           << "<5.xmax> "
                           << "<6.ymax>\n ";
    const int from_year = 1981;
    const int to_year = 2000;
    std::string clm_path(argv[1]);
    std::string out_path(argv[2]);
    float xmin = atof(argv[3]);
    float ymin = atof(argv[4]);
    float xmax = atof(argv[5]);
    float ymax = atof(argv[6]);

    char outfilename[300];
    sprintf(outfilename,"%s",out_path.c_str());
    std::ofstream outf(outfilename);
    outf << "mon lat lon PPT TMAX TMIN WIND QAIR SHORTWAVE RHUM_MAX RHUM_MIN\n";

    for (float x = xmin; x < xmax; x += 0.0625) {
        for (float y = ymin; y < ymax; y += 0.0625) {
             char filename[300];
             sprintf(filename,"%s/data_%.5f_%.5f",clm_path.c_str(),y,x);
             //std::clog << filename << std::endl;
             std::string bin_file_name(filename);
             int return_value = get_average_from_binary_file(filename
                                          ,from_year,to_year
                                          ,monthly_avg);
             if (return_value == 0) {
                std::clog << filename << std::endl;
                for (int mon = 0; mon < 12; mon++) {
                    outf    << mon << " "
                            << std::fixed << std::setprecision(5)
                            << y << " "
                            << x << " ";
                    for (int var = VIC_PPT; var < count_of_vars; var++) {
                            outf << std::fixed << std::setprecision(3);
                            outf << monthly_avg[var][mon] << " ";
                    }
                    outf << std::endl;
                }
             }
        }//col
    }//row

    delete_2d_array(monthly_avg,count_of_vars);
    outf.close();
    return 0;
}
//______________________________________________________________________________
int get_average_from_binary_file(std::string filename,
                                    int from_year, int to_year,
                                    float ** avgdata)
{
    const int clm_start_year = 1979;
    FILE *binf = fopen(filename.c_str(), "rb");
    if (binf == NULL) return -1;                                                 //nrerror("No data in the forcing file.  Model stopping...");

    fseek(binf,0,SEEK_SET);
    const int days_to_skip = get_days_between_year_with_leaps(clm_start_year,from_year-1);
    const int vars = count_of_vars;
    const int size_of_var = sizeof(short int);
    size_t bin_to_skip = days_to_skip * vars * size_of_var;

    fseek(binf,bin_to_skip,SEEK_SET);
    //float ppt,tmax,tmin,wind,sph,srad,rmax,rmin;
    float fvalue;
    //float **avgfvalue = alloc_2d_array<float>(count_of_vars,366,"avgfvalue");//[count_of_vars][doy];
    int days_366 = 0;
    unsigned short int ustmp;
    short int stmp[count_of_vars];
    int month_days[12];
    for (int var = 0; var < count_of_vars; var++) {
        for (int mon = 0; mon < 12; mon ++) {
            avgdata[var][mon] = 0.0;
            if (var == 0) month_days[mon] = 0;
        }
    }

    for(int year = from_year; year <= to_year; year++) {
        bool leapyear = LEAPYR(year);
        int days = leapyear ? 366 : 365;
        if (days == 366) days_366++;
        for (int day = 0; day < days; day++) {
            month mon = get_month(leapyear,day);
            month_days[mon]++;
            fread(&ustmp,sizeof(unsigned short int),1,binf);
            fvalue = (float) (ustmp / multi[VIC_PPT]);
            avgdata[VIC_PPT][mon] += fvalue;
            for (int var = VIC_TMAX; var < count_of_vars; var++) {
                fread(&stmp[var],sizeof(short int),1,binf);
                fvalue = (float) (stmp[var] / multi[var]);
                avgdata[var][mon] += fvalue;
            }
        }
    }
    for (int var = VIC_PPT; var < count_of_vars; var++) {
        for (int mon = 0; mon < 12; mon++) {
            avgdata[var][mon] /= (float)month_days[mon];
        }
    }
    fclose(binf);
    return 0;
}
