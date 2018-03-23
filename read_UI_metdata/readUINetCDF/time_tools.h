#ifndef TIME_TOOLS_H
#define TIME_TOOLS_H
#include "UInetcdf_constants.h"
#include <algorithm>
#include <iostream>
#include <iterator>
#include <vector>
#ifndef _LEAPYR
#define LEAPYR(y) (!((y)%400) || (!((y)%4) && ((y)%100)))
#endif
extern int monthdays_normal[13];
extern int monthdays_leap[13];
extern int start_doy_nomal[12];
extern int start_doy_leap[12];
extern std::string out_met_varname[];
extern std::string output_var_type_name[];
#ifdef HISTORICAL_MET
extern std::string varfile_prefix[] ;
extern std::string varname[];
extern std::string jc_varname[];
#else
extern std::string varfile_prefix[];
extern std::string varname[];
extern std::string gcm_name[];
extern std::string maca_rcps_name[];
extern int maca_rcps_periods[];
#endif
void cal_year_day(int days,int *year, int *yearday);
//_____________________________________________________________________________
template <class T>
T *lower_bound(T *left, T *right, T val) {
    while (left < right) {
        T *middle = left + (right - left) / 2;
        if (*middle < val)
            left = middle + 1;
        else
            right = middle;
    }
    return left;
}
//______________________________________________________________________________
template <class T>
T *upper_bound(T *left, T *right, T val) {
    while (left < right) {
        T *middle = left + (right - left) / 2;
        if (val < *middle)
            right = middle;
        else
            left = middle + 1;
    }
    return left;
}
template <typename T>
bool find_bound_in_sorted_array(const T value[], const T target, const int size,
    int& left, int& right)
{
    left = 0;
    right = size - 1;
    bool inc = value[1] > value[0];
    T min = inc ? value[0] : value[size - 1];
    T max = inc ? value[size - 1] : value[0];
    if (target < min || target > max) return false;
    if (inc) {
        while ((value[left] < value[right]) && ((right - left) != 1)) {
            int middle = left + (right - left) / 2;
            if (target >= value[middle])
                left = middle;
            else
                right = middle;
        }
    } else {
        while ((value[left] > value[right]) && ((right - left) != 1)) {
            int middle = left + (right - left) / 2;
            if (target >= value[middle])
                right = middle;
            else
                left = middle;
        }
    }
    return true;
}
//______________________________________________________________________________
template <typename T>
int find_closest_index_from_sorted_array(const T value[], const T target,
  const int size, const T tol)
{
    int left = -1;
    int right = -1;
    bool find = find_bound_in_sorted_array<T>(value, target, size, left, right);
    if (!find) {
        if (fabs(value[0] - target) <= tol) return 0;
        else if (fabs(value[size - 1] - target) <= tol) return size - 1;
        else return -1;
    } else {
        if ((fabs(value[left] - target)) <= (fabs(value[right] - target))) return left;
        else return right;
    }
}
#ifndef PUBTOOLS_H
#ifndef CHINA_CLIMATE_INTERPOLATION
template <class array_type> array_type *alloc_1d_array(int rows, const char* varname)
{
    array_type *pdata = new array_type[rows];
    return pdata;
}
//______________________________________________________________________________
template <class array_type>
void delete_1d_array(array_type *p)
{
    delete[] p;
}
//______________________________________________________________________________
template <class array_type>
void delete_2d_array(array_type **p,int rows)
{
    for (int i = 0; i < rows; i++)
        delete[] p[i];
    delete[] p;
}
//______________________________________________________________________________
template <class array_type>
void delete_3d_array(array_type ***p,int d1,int d2)
{
    for (int i = 0; i<d1; i++) {
        for (int j = 0; j<d2; j++) {
            delete[] p[i][j];
        }
        delete[] p[i];
    }
    delete[] p;
}
//______________________________________________________________________________
template <class array_type>
void delete_4d_array(array_type ***p,int d1,int d2,int d3)
{
    for (int i = 0; i < d1; i++) {
        for (int j = 0; j < d2; j++) {
            for (int k = 0; k < d3; k++) {
                delete[] p[i][j][k];
            }
            delete[] p[i][j];
        }
        delete[] p[i];
    }
    delete[] p;
}
//______________________________________________________________________________
template <class array_type> array_type **alloc_2d_array(int rows, int columns, const char* varname)
{
    array_type **pdata = new array_type*[rows];
    for (int i = 0; i < rows; i++) {
        pdata[i] = new array_type[columns];
    }
    return pdata;
}
//______________________________________________________________________________
template <class array_type> array_type ***alloc_3d_array(int d1, int d2, int d3, const char* varname)
{
    array_type ***pdata = new array_type**[d1];
    for (int i = 0; i < d1; i++) {
        pdata[i] = new array_type*[d2];
        for (int j = 0; j < d2; j++) {
            pdata[i][j] = new array_type[d3];
       }
    }
    return pdata;
}
//______________________________________________________________________________
template <class array_type> array_type ****alloc_4d_array(int d1, int d2, int d3, int d4, const char* varname)
{
    array_type ****pdata = new array_type ***[d1];
    for (int i = 0; i < d1; i++) {
        pdata[i] = new array_type **[d2];
        for (int j = 0; j < d2; j++) {
            pdata[i][j] = new array_type *[d3];
            for (int k = 0; k < d3; k++) {
                pdata[i][j][k] = new array_type[d4];
            }
        }
    }
    return pdata;
}
#endif
#endif
int get_days_between_year_with_leaps(int start_year, int end_year);
month get_month(const bool leapyear,const int doy_from_0);
season get_season(const bool leapyear,const int doy);
#ifdef HISTORICAL_MET
std::string get_historical_netcdf_file_name(const std::string prefix,
  const int var_type, const int year);
#else
std::string get_maca_netcdf_file_name(const std::string prefix,
  const int var_type, const int gcm_model_index, const int rcp_index,
  const int start_year, const int end_year);
#endif
bool get_data_from_UI_netcdf(const std::string ncfilename, const int var_type,
  const double lat, const double lon, int& start_day, int& end_day,
  double *data, float *f, double *d, float *fdim, double *ddim);
var_name get_global_var_name(const int var_index);
#ifndef HISTORICAL_MET
int get_maca_period_start_year(const int period_index, const int rcp_type_index);
int get_maca_period_end_year(const int period_index, const int rcp_type_index);
int get_gcm_model_index(std::string gcm_model_name);
int get_maca_rcp_index(std::string rcp_name);
#endif //HISTORICAL_MET
#endif // TIME_TOOLS_H
