#include <vector>
#include <string>
#include <sstream>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <math.h>
#define xEXTENDED_BINARY
bool bLeapYear(const int year)
{   //Leap year: 1
    return !((year)%400) || (!((year)%4) && ((year)%100));
}

int main(int argc, char *argv[])
{
    std::cerr<<"Beginning of main.\n";
    if (argc < 5) {
        std::cerr << "Usage:"
                  << argv[0]
                  << " [start_year] [end_year] [input_met_file]"
                  << " [output_met_file_pre]\n";
        exit(0);
    }
    int start_year = atoi(argv[1]);
    int end_year = atoi(argv[2]);
    std::string binmet(argv[3]);
    std::string outpre(argv[4]);
    std::string metfilename = binmet.substr(binmet.find("/") + 1);
    int years = end_year - start_year + 1;
    enum varname{PPT,TMAX,TMIN,WIND,SPH,SRAD,RMAX,RMIN,varname_COUNTS};
    std::string varname[] {"PPT","TMAX","TMIN","WIND"};
    std::cerr << "Start...\n";
    std::vector<std::vector<std::vector<double> > > data;  //[var][year][day]
    data.resize(varname_COUNTS);
    for (int i = 0; i < varname_COUNTS; i++) {
        data[i].resize(years);
        for (int j = 0; j < years; j++) {
            data[i][j].resize(366);
        }
    }
    std::clog << "Resize vector finished!\n";
    //Initialize
    #pragma omp parallel for
    for (int i = 0; i < varname_COUNTS; i++) {
        for (int j = 0; j < years; j++) {
            for (int day = 0; day < 366; ++day)
                data[i][j][day] = -9999.0;
        }
    }
    std::clog << "Initialized!\n";
    std::clog << "Reading binary met...\n";
    #pragma omp parallel for
    std::ifstream datafile(metfilename.c_str(),std::ios::binary);
    if (datafile.is_open()) {
        for (int year = start_year; year <= end_year; ++year) {
            int days = bLeapYear(year) ? 366 : 365;
            for (int day = 0; day < days; ++day) {
                //std::string dataline("");
                //std::getline(datafile,dataline);
                //std::stringstream ss(dataline);
                unsigned short bppt;
                signed short btmax,btmin,bwind;
#ifdef EXTENDED_BINARY
                signed short bSPH,bSRAD,bRMAX,bRMIN;
#endif
                datafile.read((char *)&bppt,sizeof(unsigned short));
                datafile.read((char *)&btmax,sizeof(signed short));
                datafile.read((char *)&btmin,sizeof(signed short));
                datafile.read((char *)&bwind,sizeof(signed short));
#ifdef EXTENDED_BINARY
                datafile.read((char *)&bSPH,sizeof(signed short));
                datafile.read((char *)&bSRAD,sizeof(signed short));
                datafile.read((char *)&bRMAX,sizeof(signed short));
                datafile.read((char *)&bRMIN,sizeof(signed short));
#endif
                if (year >= start_year) {
                    data[PPT][year-start_year][day] = (double)bppt / 40.0;
                    data[TMAX][year-start_year][day] = (double)btmax / 100.0;
                    data[TMIN][year-start_year][day] = (double)btmin / 100.0;
                    data[WIND][year-start_year][day] = (double)bwind / 100.0;
#ifdef EXTENDED_BINARY
                    data[SPH][year-start_year][day] = (double)bSPH / 10000.0;
                    data[SRAD][year-start_year][day] = (double)bSRAD / 40.0;
                    data[RMAX][year-start_year][day] = (double)bRMAX / 100.0;
                    data[RMIN][year-start_year][day] = (double)bRMIN / 100.0;
#endif
                }
            } //day
        } //year
    }
    if (datafile.is_open()) datafile.close();
    std::clog << "Reading met data finished!\n";
    std::string outfilename = outpre + metfilename + ".txt";
    std::ofstream fstat(outfilename);
#ifdef EXTENDED_BINARY
    fstat<<"year\tDOY\tppt\ttmax\ttmin\twind\tsph\tsrad\trmax\trmin\n";
#else
    fstat<<"year\tDOY\tppt\ttmax\ttmin\twind\n";
#endif
    for (int year = start_year; year <= end_year; year++) {
        int days = bLeapYear(year) ? 366 : 365;
        for (int day = 0; day < days; ++day) {
            //#pragma omp parallel for reduction(+:cells,mean)
#ifdef EXTENDED_BINARY
            fstat << year       << "\t"
                  << (day + 1)  << "\t"
                  << data[PPT][year-start_year][day] << "\t"
                  << data[TMAX][year-start_year][day] << "\t"
                  << data[TMIN][year-start_year][day] << "\t"
                  << data[WIND][year-start_year][day] << "\t"
                  << data[SPH][year-start_year][day]  << "\t"
                  << data[SRAD][year-start_year][day] << "\t"
                  << data[RMAX][year-start_year][day] << "\t"
                  << data[RMIN][year-start_year][day] << "\n";
#else
            fstat << year       << "\t"
                  << (day + 1)  << "\t"
                  << data[PPT][year-start_year][day] << "\t"
                  << data[TMAX][year-start_year][day] << "\t"
                  << data[TMIN][year-start_year][day] << "\t"
                  << data[WIND][year-start_year][day] << "\n";

#endif
        }
    }
    fstat.close();
    std::cerr<<"Output finished!\n";

    data.clear();
    std::cerr<<"End!\n";
}
