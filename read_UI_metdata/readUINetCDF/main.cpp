#include "et_functions.h"
#include "time_tools.h"
#include "UInetcdf_constants.h"
#include <iostream>
#include <fstream>
#include <math.h>
#include <sstream>
#include <time.h>
#include <omp.h>
#define MAX_DIM 1500
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
#ifndef HISTORICAL_MET
                  << " [gcm_model_name] "
                  << " [rcp] "
#endif
                  << std::endl;
        exit(0);
    }
#ifndef HISTORICAL_MET
    std::cout << "\nargv[1]:"    << argv[1]
              << "\nargv[2]:"    << argv[2]
              << "\nargv[3]:"    << argv[3]
              << "\nargv[4]:"    << argv[4]
              << "\nargv[5]:"    << argv[5]
              << "\nargv[6]:"    << argv[6]
              << "\nargv[7]:"    << argv[7]
              << std::endl;
#endif
    std::string selected_cell_name(argv[1]);
    int start_year  = atoi(argv[2]);
    int end_year    = atoi(argv[3]);
    std::string metdata_prefix(argv[4]);
    std::string output_file_name(argv[5]);
#ifndef HISTORICAL_MET
    std::string gcm_model_name(argv[6]);
    std::string rcp_name(argv[7]);
    int gcm_model_index = get_gcm_model_index(gcm_model_name);
    int maca_rcps_index = get_maca_rcp_index(rcp_name);
#endif
#ifdef HISTORICAL_MET
    int vars = his_VAR_COUNTS;                                                                   //pr,tmmx,tmmn,rmax,rmin,srad,vs
#else
    int vars = fut_VAR_COUNTS;
#endif
    int years = end_year - start_year + 1;
    int days = 366;
    std::ofstream outf(output_file_name);
    //outf << "cell_id\tlat\tlon\tyear\tmonth\tday\tvar\tvalue\n";
    outf << "cell_id\tyear\tmonth\tday\tvar\tvalue\n";






  double ***data    = alloc_3d_array<double>(vars,years,days,"data");
  double *temp_data = (double *)malloc(5 * days * sizeof(double));
  float *f          = (float *) malloc(5 * days * sizeof(float));
  double *d         = (double *) malloc(5 * days * sizeof(double));
  float  *fdim      = (float *)  malloc(MAX_DIM * sizeof(float));
  double *ddim      = (double *) malloc(MAX_DIM * sizeof(double));
  /*double *pm_day      = (double *) malloc(days * sizeof(double));
  double *pt_day      = (double *) malloc(days * sizeof(double));
  double *ppt_day      = (double *) malloc(days * sizeof(double));
  double *tmax_day      = (double *) malloc(days * sizeof(double));
  double *tmin_day      = (double *) malloc(days * sizeof(double));
  double *srad_day      = (double *) malloc(days * sizeof(double));
  double *rhmax_day      = (double *) malloc(days * sizeof(double));
  double *rhmin_day      = (double *) malloc(days * sizeof(double));
  double *uaz_day      = (double *) malloc(days * sizeof(double));
  double *vaz_day      = (double *) malloc(days * sizeof(double));
  double *uz_day      = (double *) malloc(days * sizeof(double));
  */


  double output_data[month_counts][output_var_type_counts];

  //begin cell loops
  std::ifstream selected_cell(selected_cell_name);
  std::string line;
 while (std::getline(selected_cell, line)) {
  std::istringstream iss(line);
  if (line[0] >= '0' && line[0] <= '9') {
   int cell_id;
   double lat;
   double lon;
   double elev;
   double screen_height = 10.;
   if (iss >> cell_id >> lon >> lat >> elev) {
    //double ***data = alloc_3d_array<double>(vars,years,days,"data");
    std::cout << "cell_id:" << cell_id
              << "\tlat:" << lat
              << "\tlon:" << lon
              << std::endl;
    int var_index = 0;
    for (int var = PPT; var < VAR_COUNTS; var++) {
#ifdef HISTORICAL_MET
        if (var != UAS) {
#endif
            //std::cout << "Start reading var:"
            //          << varfile_prefix[var]
            //          << std::endl;
#ifdef HISTORICAL_MET
            for (int year = start_year; year <= end_year; year++) {
                //double *temp_data = (double *)malloc(days * sizeof(double));
                std::string netcdf_filename =
                    get_historical_netcdf_file_name(metdata_prefix,var,year);
                //std::cout << "netcdf_file:" << netcdf_filename << std::endl;
                int start_day,end_day;
                bool success = get_data_from_UI_netcdf(netcdf_filename,var,lat,
                                 lon,start_day,end_day,temp_data,f,d,fdim,ddim);
                if (success) {
                    for(int day = 0; day <= (end_day - start_day); day++) {
                        if (var == his_TMAX || var == his_TMIN) {
                            temp_data[day] -= 273.15;
                        }
                        data[var_index][year-start_year][day] = temp_data[day];
                    }
                } else {
                    std::cerr << "Error: Cannot find the met data for "
                              << "\tlat:" << lat
                              << "\tlon:" << lon
                              << "\t@"    << year
                              << std::endl;
                }
                //free(temp_data);
            }  //year
#else
            for (int period = 0; period < maca_rcps_periods[maca_rcps_index];
                 period++) {
                int p_start_year = get_maca_period_start_year(period,
                                     maca_rcps_index);
                int p_end_year   = get_maca_period_end_year(period,
                                     maca_rcps_index);
                int days = get_days_between_year_with_leaps(p_start_year,
                                                            p_end_year);
                //double *temp_data = (double *)malloc(days * sizeof(double));
                //check if need read netcdf file coverring this time period
                if ((p_start_year >= start_year && p_start_year <= end_year)
                    || (p_end_year   >= start_year && p_end_year <= end_year)
                    || (p_start_year <= start_year && p_end_year >= end_year)) {
                    /*std::cout << "\tp_start_year:"
                              << p_start_year
                              << "\tp_end_year:"
                              << p_end_year
                              << "\tdays:"
                              << days
                              << std::endl;
                              */
                    std::string netcdf_filename =
                            get_maca_netcdf_file_name(metdata_prefix,var,
                              gcm_model_index,maca_rcps_index,p_start_year,
                              p_end_year);
                    /*std::cout << "netcdf_filename:"
                              << netcdf_filename
                              << std::endl;*/
                    int start_day,end_day;
                    bool success = get_data_from_UI_netcdf(netcdf_filename,var,lat,
                                     lon,start_day,end_day,temp_data,f,d,fdim,ddim);
                    if (success) {
                        int year_t = p_start_year;
                        int day_t  = 0;
                        for(int day = start_day; day <= end_day; day++) {
                            if (var == fut_TMAX || var == fut_TMIN) {
                                temp_data[day-start_day] -= 273.15;
                            }
                            int ydays = LEAPYR(year_t) ? 366 : 365;
                            if (day_t == ydays) {                                //start new year
                                day_t = 0;
                                year_t++;
                            }
                            data[var_index][year_t-start_year][day_t] =
                                                       temp_data[day-start_day];
                            day_t++;
                        }
                    } else {
                        std::cerr << "Error: Cannot find the met data for "
                                  << "\tlat:"   << lat
                                  << "\tlon:"   << lon
                                  << "\tgcm:" << gcm_model_name[gcm_model_index]
                                  << "\trcp:" << maca_rcps_name[maca_rcps_index]
                                  << "\ts_year:" << p_start_year
                                  << "\te_year:" << p_end_year
                                  << std::endl;
                    }
                }
                //free(temp_data);
            }
#endif
            var_index++;
#ifdef HISTORICAL_MET
        } //if
#endif
    } //var
    //Print out daily met data
#ifdef PRINT_DAILY_MET
    for (int var = 0; var < vars; var++) {
        var_name global_var_name = get_global_var_name(var);
        if (global_var_name != UAS && global_var_name != VAS) {
        for (int year = start_year; year <= end_year; year++) {
            bool leap_year = LEAPYR(year);
            int days = leap_year ? 366 : 365;
            for (int day = 0; day < days; day++) {
                double outvalue = data[var][year-start_year][day];
                outf << lat     << "\t"
                     << lon     << "\t"
                     << year    << "\t"
                     << "\t"
                     << day     << "\t"
                     << out_met_varname[global_var_name] << "\t"
                     << outvalue
                     << std::endl;
            } //day
        } //year
        } //if
    } //var
#endif
    //Calculate PET and statistic
    //double output_data[month_counts][output_var_type_counts];
    for (int year = start_year; year <= end_year; year++) {
        bool leap_year = LEAPYR(year);
        int days = leap_year ? 366 : 365;
        //double output_data[month_counts][output_var_type_counts];
        #pragma omp parallel for
        for (int mon = JAN; mon < month_counts; mon++) {
            for (int var = OUT_PPT; var < output_var_type_counts; var++) {
                output_data[mon][var] = 0;
            }
        }

        int *mon_days = leap_year ? monthdays_leap : monthdays_normal;
#pragma omp parallel for
        for (int day = 0; day < days; day++) {
#ifdef HISTORICAL_MET
            double ppt/*_day[day]*/      = data[his_PPT][year-start_year][day];
            double tmax/*_day[day]*/     = data[his_TMAX][year-start_year][day];
            double tmin/*_day[day]*/     = data[his_TMIN][year-start_year][day];
            double srad/*_day[day]*/     = data[his_SRAD][year-start_year][day] * 0.0864;
            double rhmax/*_day[day]*/    = data[his_RHMAX][year-start_year][day];
            double rhmin/*_day[day]*/    = data[his_RHMIN][year-start_year][day];
            double uz/*_day[day]*/       = data[his_VAS][year-start_year][day];
#else
            double ppt/*_day[day]*/      = data[fut_PPT][year-start_year][day];
            double tmax/*_day[day]*/     = data[fut_TMAX][year-start_year][day];
            double tmin/*_day[day]*/     = data[fut_TMIN][year-start_year][day];
            double srad/*_day[day]*/     = data[fut_SRAD][year-start_year][day] * 0.0864;
            double rhmax/*_day[day]*/    = data[fut_RHMAX][year-start_year][day];
            double rhmin/*_day[day]*/    = data[fut_RHMIN][year-start_year][day];
            double uaz/*_day[day]*/      = data[fut_UAS][year-start_year][day];
            double vaz/*_day[day]*/      = data[fut_VAS][year-start_year][day];
            double uz/*_day[day]*/       = sqrt(uaz/*_day[day]*/ * uaz/*_day[day]*/ +
                                     vaz/*_day[day]*/ * vaz/*_day[day]*/);
#endif
            double aero_term;
            double rad_term;
            double pm/*_day[day]*/ = calc_referenceET_PM(lat,elev,screen_height,day+1,
                              tmax/*_day[day]*/,tmin/*_day[day]*/,srad/*_day[day]*/,
                              rhmax/*_day[day]*/,rhmin/*_day[day]*/,uz/*_day[day]*/,
                              aero_term,rad_term);
            double pt/*_day[day]*/ = calc_referenceET_PT_from_RadTerm(rad_term);
            //double tavg = (tmin + tmax) / 2.0;
            //double rhum = (rhmax + rhmin) / 2.0;
        //} //day
        //for (int day = 0; day < days; day++) {
//#pragma omp critical
            //{
            month which_month = get_month(leap_year,day);
            //make statistics
            for (int s = 0; s < month_counts; s++) {
                if (s == ANN || s == which_month) {
                    double mday = (double)mon_days[s];
                    output_data[s][OUT_PPT]   += ppt/*_day[day]*/    / mday;
                    //output_data[s][OUT_TAVG]  += tavg   / mday;
                    output_data[s][OUT_TMAX]  += tmax/*_day[day]*/   / mday;
                    output_data[s][OUT_TMIN]  += tmin/*_day[day]*/   / mday;
                    //output_data[s][OUT_RHUM]  += rhum   / mday;
                    output_data[s][OUT_RHMAX] += rhmax/*_day[day]*/  / mday;
                    output_data[s][OUT_RHMIN] += rhmin/*_day[day]*/  / mday;
                    output_data[s][OUT_WIND]  += uz/*_day[day]*/     / mday;
                    output_data[s][OUT_SRAD]  += srad/*_day[day]*/   / mday;
                    output_data[s][OUT_PT]    += pt/*_day[day]*/ / mday;
                    output_data[s][OUT_PM]    += pm/*_day[day]*/ / mday;
                }
            } //s
            //}
#ifdef PRINT_DAILY_MET
            outf << lat     << "\t"
                 << lon     << "\t"
                 << year    << "\t"
                 << "\t"
                 << day     << "\t"
                 << "Tavg"  << "\t"
                 << (tmax + tmin) / 2.0 << "\t"
                 << std::endl;
            outf << lat     << "\t"
                 << lon     << "\t"
                 << year    << "\t"
                 << "\t"
                 << day     << "\t"
                 << "Wind"  << "\t"
                 << uz << "\t"
                 << std::endl;
            outf << lat     << "\t"
                 << lon     << "\t"
                 << year    << "\t"
                 << "\t"
                 << day     << "\t"
                 << "rhum"  << "\t"
                 << (rhmax + rhmin) / 2.0 << "\t"
                 << std::endl;
            outf << lat     << "\t"
                 << lon     << "\t"
                 << year    << "\t"
                 << "\t"
                 << day     << "\t"
                 << "PM_pet" << "\t"
                 << pm_pet
                 << std::endl;
            outf << lat     << "\t"
                 << lon     << "\t"
                 << year    << "\t"
                 << "\t"
                 << day     << "\t"
                 << "PT_pet" << "\t"
                 << pt_pet
                 << std::endl;
#endif
        } //day
        //Print out monthly and annual outputs
        for (int mon = JAN; mon < month_counts; mon++) {
            for (int var = OUT_PPT; var < output_var_type_counts; var++) {
                if (var != OUT_TAVG && var != OUT_RHUM)
                outf << cell_id                     << "\t"
                     //<< lat                         << "\t"
                     //<< lon                         << "\t"
                     << year                        << "\t"
                     << mon                         << "\t"
                     << "\t"
                     << output_var_type_name[var]   << "\t"
                     << output_data[mon][var]
                     << std::endl;
            }
        }
    } //year

    //delete_3d_array(data,vars,years);


   } //if
  } //if
 } //while
    delete_3d_array(data,vars,years);
    free(temp_data);
    free(f);
    free(d);
    free(fdim);
    free(ddim);
    /*free(pm_day);
    free(pt_day);
    free(ppt_day);
    free(tmax_day);
    free(tmin_day);
    free(srad_day);
    free(rhmax_day);
    free(rhmin_day);
    free(uaz_day);
    free(vaz_day);
    free(uz_day);*/


    outf.close();
    selected_cell.close();
    curtime = localtime ( &_tm );
    std::cout << "Finished @ " << asctime(curtime) << std::endl;

    return 0;
}
