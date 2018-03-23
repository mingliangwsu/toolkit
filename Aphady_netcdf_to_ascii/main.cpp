#include "time_tools.h"
#include <iostream>
#include <fstream>
#include <math.h>
#include <sstream>
#include <time.h>
#include <omp.h>
#include <netcdf.h>
#include "esrigridclass.h"
#define MAX_DIM 1500

#define ERR(e) {printf("Error: %s\n", nc_strerror(e)); return false;}
#define NDAYS_NAME "time"
#define NLAT_NAME "latitude"
#define NLONT_NAME "longitude"
#define VAR_NAME "precip"

int main(int argc, char *argv[])
{
    std::cout << "Start...\n";
    time_t _tm = time(NULL );
    struct tm * curtime = localtime ( &_tm );
    std::cout << "current time: " << asctime(curtime) << std::endl;

    //data[var][year][day]
    if (argc < 3) {
        std::cerr << "Usage: " << argv[0]
                  << " [start_year] "
                  << " [end_year] "
                  << " [metdata_path_with_slash] "
                  << " [output_file_name] "
                  << std::endl;
        exit(0);
    }

    int start_year  = atoi(argv[1]);
    int end_year    = atoi(argv[2]);
    std::string metdata_prefix(argv[3]);
    std::string output_file_name(argv[4]);

    int years = end_year - start_year + 1;
    int days = 366;
    std::ofstream outf(output_file_name);
    outf << "cell_id\tyear\tmonth\tday\tvar\tvalue\n";

    for (int year = start_year; year <= end_year; year++) {
        std::cout << "year:" << year << std::endl;
        bool leapyear = LEAPYR(year);
        std::string netcdf_filename = metdata_prefix
                                      + "APHRO_MA_025deg_V1101."
                                      + std::to_string(year)
                                      + ".nc";
        int retval,ncid,daysid,latid,lontid,varid;
        size_t recs_days,nlat,nlont;
        if((retval = nc_open(netcdf_filename.c_str(), NC_NOWRITE, &ncid))) ERR(retval);
        if (retval = nc_inq_dimid(ncid,NDAYS_NAME,&daysid))      ERR(retval);
        if (retval = nc_inq_dimlen(ncid,daysid,&recs_days))      ERR(retval);
        if (retval = nc_inq_dimid(ncid,NLAT_NAME,&latid))        ERR(retval);
        if (retval = nc_inq_dimlen(ncid,latid,&nlat))            ERR(retval);
        if (retval = nc_inq_dimid(ncid,NLONT_NAME,&lontid))      ERR(retval);
        if (retval = nc_inq_dimlen(ncid,lontid,&nlont))          ERR(retval);

        int day_var_id,var_var_id,lat_var_id,lon_var_id;
        if (retval = nc_inq_varid(ncid,NLAT_NAME, &lat_var_id))   ERR(retval);
        if (retval = nc_inq_varid(ncid,NLONT_NAME,&lon_var_id))   ERR(retval);
        if (retval = nc_inq_varid(ncid,VAR_NAME,  &var_var_id))   ERR(retval);

        double *lat = alloc_1d_array<double>(nlat,"lat");
        double *lon = alloc_1d_array<double>(nlont,"lon");
        float *orig_data = alloc_1d_array<float>(recs_days*nlat*nlont,"orig_data");
        if ((retval = nc_get_var_double(ncid, lat_var_id, &lat[0]))) ERR(retval);
        if ((retval = nc_get_var_double(ncid, lon_var_id, &lon[0]))) ERR(retval);
        if ((retval = nc_get_var_float(ncid, var_var_id, &orig_data[0]))) ERR(retval);

        for (int day = 0; day < recs_days; day++) {
            int month = get_month(leapyear,day) + 1;                             //1-12
            int *mstartday = leapyear ? start_doy_leap : start_doy_nomal;        //1-
            int month_day = day + 1 - mstartday[month - 1] + 1;                  //1-
            EsriGridClass<float> outgrid;
            outgrid.setNcols(nlont);
            outgrid.setNrows(nlat);
            outgrid.setCellsize(0.25);
            outgrid.setNodataValue(-99.9);
            outgrid.setXll(lon[0] - 0.25/2.0);
            outgrid.setYll(lat[0] - 0.25/2.0);
            outgrid.AllocateMem();
            for (int ilat = 0; ilat < nlat; ilat++) {
                for (int ilon = 0; ilon < nlont; ilon++) {
                    size_t index = day * nlat * nlont + (nlat - 1 - ilat) * nlont + ilon;
                    outgrid.setValue(ilat,ilon,orig_data[index]);
                }
            }
            std::string outfilename = output_file_name
                                      + "y" + std::to_string(year)
                                      + "m" + std::to_string(month)
                                      + "d" + std::to_string(month_day)
                                      + ".asc";
            outgrid.writeAsciiGridFile(outfilename);
        }
    }

    curtime = localtime ( &_tm );
    std::cout << "Finished @ " << asctime(curtime) << std::endl;

    return 0;
}
