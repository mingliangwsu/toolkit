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
                                    float *avg_ppt, float *avg_tmax,
                                    float *avg_tmin, float *avg_wind);

const int clm_start_year = 1915;
const int clm_end_year = 2015;
enum {VIC_PPT,VIC_TMAX,VIC_TMIN,VIC_WIND,count_of_vars};
float multi[count_of_vars] = {40,100,100,100};
int cell = 0;

int main(int argc, char *argv[])
{
    float *avg_ppt  = alloc_1d_array<float>(366,"ppt");
    float *avg_tmax = alloc_1d_array<float>(366,"tmax");
    float *avg_tmin = alloc_1d_array<float>(366,"tmin");
    float *avg_wind = alloc_1d_array<float>(366,"wind");

    if(argc < 6) std::cerr << "wrong number of arguments! ==> "
                           << "<1. boundary ascii>\n"
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
    //EsriGridClass<double> out_grid[count_of_out];
    //for (int outvar = OUT_TMAX; outvar < count_of_out; outvar++) {
    //    out_grid[outvar].CopyHeadInformation(crbbnd);
    //    out_grid[outvar].AllocateMem();
    //}
    for (int row = 0; row < crbbnd.getNrows(); row++) {
        float ycor = crbbnd.getGridYll(row) + crbbnd.getCellsize() / 2.0;        //center
        for (int col = 0; col < crbbnd.getNcols(); col++) {
            if (crbbnd.IsValidCell(row,col)) {
                float xcor = crbbnd.getGridXll(col) + crbbnd.getCellsize() / 2.0; //center
                char filename[300];
                sprintf(filename,"%s/data_%.5f_%.5f",clm_path.c_str(),ycor,xcor);
                std::clog << filename << std::endl;
                std::string bin_file_name(filename);
                float return_value = get_average_from_binary_file(filename
                                             ,from_year,to_year
                                             ,avg_ppt,avg_tmax,avg_tmin
                                             ,avg_wind);

                //Write to a binary file

                char outfilename[300];
                sprintf(outfilename,"%s/data_%.5f_%.5f",out_path.c_str(),ycor,xcor);
                FILE *binf = fopen(outfilename, "wb");
                unsigned short int ustmp;
                short int stmp;

                for(int year = clm_start_year; year <= clm_end_year; year++) {
                    int days = LEAPYR(year) ? 366 : 365;
                    for (int day = 0; day < days; day++) {
                        ustmp = (unsigned short int)(avg_ppt[day] * multi[VIC_PPT]);
                        fwrite(&ustmp,sizeof(unsigned short int),1,binf);

                        stmp = (short int)(avg_tmax[day] * multi[VIC_TMAX]);
                        fwrite(&stmp,sizeof(short int),1,binf);

                        stmp = (short int)(avg_tmin[day] * multi[VIC_TMIN]);
                        fwrite(&stmp,sizeof(short int),1,binf);

                        stmp = (short int)(avg_wind[day] * multi[VIC_WIND]);
                        fwrite(&stmp,sizeof(short int),1,binf);

                    }//day
                }//year
                cell++;
            }//if
        }//col
    }//row
    delete_1d_array(avg_ppt);
    delete_1d_array(avg_tmax);
    delete_1d_array(avg_tmin);
    delete_1d_array(avg_wind);
    return 0;
}
//______________________________________________________________________________
float get_average_from_binary_file(std::string filename,
                                    int from_year, int to_year,
                                    float *avg_ppt, float *avg_tmax,
                                    float *avg_tmin, float *avg_wind)
{
    //const int clm_start_year = 1915;
    FILE *binf = fopen(filename.c_str(), "rb");
    //enum {PPT,TMAX,TMIN,WIND,SPH,SRAD,RMAX,RMIN,count_of_vars};
    //float multi[count_of_vars] = {40,100,100,100,10000,40,100,100};
    if (binf == NULL) return -1;                                                   //nrerror("No data in the forcing file.  Model stopping...");

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
    for (int doy = 0; doy < 366; doy ++) {
        avg_ppt[doy] = 0.0;
        avg_tmax[doy] = 0.0;
        avg_tmin[doy] = 0.0;
        avg_wind[doy] = 0.0;
    }

    for(int year = from_year; year <= to_year; year++) {
        int days = LEAPYR(year) ? 366 : 365;
        if (days == 366) days_366++;
        for (int day = 0; day < days; day++) {
            fread(&ustmp,sizeof(unsigned short int),1,binf);
            fvalue = (float) (ustmp / multi[VIC_PPT]);
            avg_ppt[day] += fvalue;
#ifdef TEST_DATA
            float test[count_of_vars];
            test[VIC_PPT] = fvalue;
#endif
            for (int var = VIC_TMAX; var < count_of_vars; var++) {
                fread(&stmp[var],sizeof(short int),1,binf);
                fvalue = (float) (stmp[var] / multi[var]);
#ifdef TEST_DATA
                test[var] = fvalue;
#endif

                switch(var) {
                case VIC_TMAX:
                    avg_tmax[day] += fvalue;
                    break;
                case VIC_TMIN:
                    avg_tmin[day] += fvalue;
                    break;
                case VIC_WIND:
                    avg_wind[day] += fvalue;
                    break;
                }
            }
#ifdef TEST_DATA
            if (cell == 0)
            std::clog << year << "\t" << day << "\t" << test[VIC_PPT] << "\t" << test[VIC_TMAX] << "\t" << test[VIC_TMIN] << "\t" << test[VIC_WIND] << std::endl;
#endif
        }
    }

    for (int day = 0; day < 366; day++) {
        int num = to_year - from_year + 1;
        if (day == 365) {
            num = days_366;
        }
        //std::clog << "day:" << day << "\tnum:" << num << std::endl;
        avg_ppt[day] /= (float) num;
        avg_tmax[day] /= (float) num;
        avg_tmin[day] /= (float) num;
        avg_wind[day] /= (float) num;

#ifdef TEST_DATA
            if (cell == 0)
            std::clog << "mean\t" << day << "\t" << avg_ppt[day] << "\t" << avg_tmax[day] << "\t" << avg_tmin[day] << "\t" << avg_wind[day] << std::endl;
#endif

    }

    fclose(binf);
    return 0;
}
