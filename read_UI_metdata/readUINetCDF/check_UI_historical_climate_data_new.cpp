#include "et_functions.h"
#include "esrigridclass.h"
#include "time_tools.h"
#include "UInetcdf_constants.h"
#include <iostream>
#include <fstream>
#include <math.h>
#include <sstream>
#include <time.h>
#include <omp.h>
#include <netcdf.h>
#define MAX_DIM 1500
int main(int argc, char *argv[])
{
    std::cout << "Start...\n";
    time_t _tm = time(NULL );
    struct tm * curtime = localtime ( &_tm );
    std::cout << "current time: " << asctime(curtime) << std::endl;

    //data[var][year][day]
    if (argc < 5) {
        std::cerr << "Usage: " << argv[0]
                  << " [nc_file_name] "
                  << " [var_name] "
                  << " [output_file_name] "
                  << " [out_doy]"
                  << std::endl;
        exit(0);
    }
    std::string ncfilename(argv[1]);
    std::string varname(argv[2]);
    std::string output_file_name(argv[3]);
    int outdoy = atoi(argv[4]);

    int start_year  = 2000;
    int end_year    = 2000;
    int vars = 1;                                                                   //pr,tmmx,tmmn,rmax,rmin,srad,vs
    int years = end_year - start_year + 1;
    int days = 366;
    const int LATS = 585;
    const int LONS = 1386;
    const int DAYS = 366;
    const long total_rec = LATS * LONS * DAYS;
    int total_days = years * days;
    std::ofstream outf(output_file_name);
    outf << "var\tday\tvalue\n";
    EsriGridClass<float> grid[1];
    double cellsize = 1.0/24.0;
    for (int var = jc_his_PPT; var < 1; var++) {
        grid[var].setNcols(LONS);
        grid[var].setNrows(LATS);
        grid[var].setCellsize(cellsize);
        grid[var].setNodataValue(-9999.0);
        grid[var].setXll(-124.7722 - 0.5*cellsize);
        grid[var].setYll(25.06308 - 0.5*cellsize);
        grid[var].AllocateMem();
    }

  float *lat        = alloc_1d_array<float>(LATS,"lat");
  float *lon        = alloc_1d_array<float>(LONS,"lat");
  float *f          = alloc_1d_array<float>(LATS * LONS * DAYS,"f");

  int retval,ncid,daysid,latid,lonid,varid;
  size_t recs_days,nlat,nlont;
  if((retval = nc_open(ncfilename.c_str(), NC_NOWRITE, &ncid)))
      ERR(retval);
  size_t start[3];
  size_t count[3];

  if (retval = nc_inq_varid(ncid,"lat",&latid))   ERR(retval);
  if (retval = nc_inq_varid(ncid,"lon",&lonid))   ERR(retval);
  if ((retval = nc_get_var_float(ncid, latid, &lat[0]))) ERR(retval);
  if ((retval = nc_get_var_float(ncid, lonid, &lon[0]))) ERR(retval);
  //get day dimition information
  for (int var = 0; var < 1; var++) {
      if (retval = nc_inq_varid(ncid,varname.c_str(),&varid))   ERR(retval);
      //start[0] = 0;
      //start[1] = 0;
      //start[2] = 0;
      //count[0] = DAYS;
      //count[1] = LATS;
      //count[2] = LONS;
      if ((retval = nc_get_var_float(ncid, varid, &f[0]))) ERR(retval);
      for (long day = 0; day < DAYS; day++) {
          long rec = 0;
          for (int ilat = 0; ilat < LATS; ilat++) {
              for (int ilon = 0; ilon < LONS; ilon++) {
                  size_t index = day * LATS * LONS + ilat * LONS + ilon;
                  if (ilat == 200 && ilon == 200)
                          std::cerr << varname <<"\t"
                                    << "\tlat:" << lat[ilat]
                                    << "\tlon:" << lon[ilon]
                                    << "\tday:" << day
                                    << "\tvalue:" << f[index]
                                    << std::endl;

                  double addvalue = f[index];
                  if (day == (outdoy - 1))
                    grid[var].setValue(ilat,ilon,addvalue);
              } //lon
          } //lat
      } //day
  } //var
  nc_close(ncid);

  for (int var = 0; var < 1; var++) {
      grid[var].writeAsciiGridFile(output_file_name + "_grid.asc");
  }

    //Print out daily met data
    delete_1d_array(f);
    delete_1d_array(lat);
    delete_1d_array(lon);

    outf.close();
    curtime = localtime ( &_tm );
    std::cout << "Finished @ " << asctime(curtime) << std::endl;

    return 0;
}
