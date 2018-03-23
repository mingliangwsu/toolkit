#include <iostream>
#include <iomanip>
#include <fstream>
#include "esrigridclass.h"
#include "time_tools.h"

int main(int argc, char *argv[])
{
    if(argc < 9) std::cerr << "wrong number of arguments! ==> "
                           << "<1.start_year> <2.end_year> "
                           << "<3.pre_dir> <4.tmx_dir> <5.tmn_dir> <6.win_dir> <7.out_path> "
                           << "<8.lat_ascii_grid> <9.lat_ascii_grid> ";
    int start_year = atoi(argv[1]);
    int end_year = atoi(argv[2]);
    char filename[1024];

    EsriGridClass<double> glat;
    EsriGridClass<double> glon;
    std::string fnlat(argv[8]);
    std::string fnlon(argv[9]);
    glat.readAsciiGridFile(fnlat);
    glon.readAsciiGridFile(fnlon);
    int cols = glat.getNcols();
    int rows = glat.getNrows();

    for (int year = start_year; year <= end_year; year++) {
        std::clog << argv[7] << "\tYear:" << year << std::endl;
        bool leapyear = LEAPYR(year);
        int *monthdays = leapyear ? monthdays_leap : monthdays_normal;
        for (int mon = 1; mon <= 12; mon++) {
            std::clog << "Mon:" << mon << std::endl;
            int mondays = monthdays[mon - 1];
            for (int day = 1; day <= mondays; day++) {
                filename[0] = 0;
                sprintf(filename,"%s/y%d/m%dd%d.asc",argv[3],year,mon,day);
                std::string ppt(filename);
                filename[0] = 0;
                sprintf(filename,"%s/y%d/m%dd%d.asc",argv[4],year,mon,day);
                std::string tmx(filename);
                filename[0] = 0;
                sprintf(filename,"%s/y%d/m%dd%d.asc",argv[5],year,mon,day);
                std::string tmn(filename);
                filename[0] = 0;
                sprintf(filename,"%s/y%d/m%dd%d.asc",argv[6],year,mon,day);
                std::string win(filename);
                EsriGridClass<double> gppt;
                EsriGridClass<double> gtmx;
                EsriGridClass<double> gtmn;
                EsriGridClass<double> gwin;
                gppt.readAsciiGridFile(ppt);
                gtmx.readAsciiGridFile(tmx);
                gtmn.readAsciiGridFile(tmn);
                gwin.readAsciiGridFile(win);
                #pragma omp parallel for
                for (int row = 0; row < rows; row++) {
                    for (int col = 0; col < cols; col++) {
                        if (glat.IsValidCell(row,col)) {
                            char outfilename[1024];
                            double dlat = glat.getValue(row,col);
                            double dlon = glon.getValue(row,col);
                            sprintf(outfilename,"%s/data_%.5f_%.5f",argv[7],dlat,dlon);
                            std::string outfile(outfilename);
                            std::ofstream fout(outfile,std::ofstream::out | std::ofstream::app);
                            fout << std::fixed
                                 << std::setprecision(2)
                                 << gppt.getValue(row,col)
                                 << " "
                                 << gtmx.getValue(row,col)
                                 << " "
                                 << gtmn.getValue(row,col)
                                 << " "
                                 << gwin.getValue(row,col)
                                 << std::endl;
                            fout.close();
                        }
                    }
                }

            }
        }
    }
    return 0;
}
