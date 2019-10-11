#include "time_tools.h"

#include <iostream>
#include <math.h>
#include <netcdf.h>
#include <sstream>
#include <string>
#include <vector>
int monthdays_normal[13]    = {31,28,31,30,31,30,31,31,30,31,30,31,365};
int monthdays_leap[13]      = {31,29,31,30,31,30,31,31,30,31,30,31,366};
int start_doy_nomal[12]     = {1,32,60,91,121,152,182,213,244,274,305,335};
int start_doy_leap[12]      = {1,32,61,92,122,153,183,214,245,275,306,336};

/****from year,mon,day converted to days since 1900-01-01****/
/****from year,mon,day converted to days since 1900-01-01****/
//leap years
int get_indays_leap_years(const int year,const int mon,const int day){
   //mon:1-12 day:1-31
   int *monthdays;
   int inday = 0;
   if(year<1900) return inday;
   for (int i = 1900; i < year; i++) {
      if(LEAPYR(i)) inday += 366;
      else inday += 365;
   }
   if(LEAPYR(year)) monthdays = monthdays_leap;
   else monthdays = monthdays_normal;
   if (year < 1900 || mon < 1 || mon > 12 || day < 1 || day > monthdays[mon-1]) {
      std::cerr<<"Wrong input date!!!\n";
      exit(0);
   }
   for (int i = 1; i < mon; i++) {
      inday += monthdays[i-1];
   }
   inday += (day-1);
   return inday;
};
//______________________________________________________________________________
int get_start_lat_or_lont(float *lxxt,int ndim,float inlxxt){
  int start = -9999;
  int i;
  bool descending = lxxt[0] > lxxt[1] ? true : false;
  for (i = 0; i < ndim; i++) {
    if ((inlxxt <= lxxt[i] && !descending) || (inlxxt >= lxxt[i] && descending)) {
      start = i-1;
      return (i == 0) ? 0 : start;
    }
  }
  if(start == -9999) return -1;
};
//______________________________________________________________________________
//no leap years
int get_indays(int year,int mon,int day){
    int inday=0;
    int i;
    if(year<1900) return inday;
    for(i=1900;i<year;i++){
        inday += 365;
    }
    monthdays_normal[1] = 28;
    for(i=1;i<mon;i++){
        inday += monthdays_normal[i-1];
    }
    inday += (day-1);
    return inday;
};
//______________________________________________________________________________
void cal_year_day(int days,int *year, int *yearday){
    //days: days since 1900-1-1 from 1

    int syear = 1900;
    while (days > 0) {
        int yrday = LEAPYR(syear) ? 366 : 365;
        days -= yrday;
        syear++;
    }
    *year = syear - 1;
    *yearday = days + (LEAPYR(*year) ? 366 : 365);
}
//______________________________________________________________________________
int get_days_between_year_with_leaps(int start_year, int end_year)
{   //including end_years; if equal, return the days of that year
    int days = 0;
    if (end_year < start_year) std::swap<int>(start_year,end_year);
    for (int year = start_year; year <= end_year; year++) {
        days += LEAPYR(year) ? 366 : 365;
    }
    return days;
}
//______________________________________________________________________________
month get_month(const bool leapyear,const int doy_from_0)
{
    int *p;
    int doy = doy_from_0 + 1;
    month month_index = JAN;
    if (leapyear) p = start_doy_leap;
    else          p = start_doy_nomal;
    if (doy >= p[JAN] && doy <= (p[FEB] - 1)) month_index = JAN;
    else if (doy >= p[FEB] && doy <= (p[MAR] - 1)) month_index = FEB;
    else if (doy >= p[MAR] && doy <= (p[APR] - 1)) month_index = MAR;
    else if (doy >= p[APR] && doy <= (p[MAY] - 1)) month_index = APR;
    else if (doy >= p[MAY] && doy <= (p[JUN] - 1)) month_index = MAY;
    else if (doy >= p[JUN] && doy <= (p[JUL] - 1)) month_index = JUN;
    else if (doy >= p[JUL] && doy <= (p[AUG] - 1)) month_index = JUL;
    else if (doy >= p[AUG] && doy <= (p[SEP] - 1)) month_index = AUG;
    else if (doy >= p[SEP] && doy <= (p[OCT] - 1)) month_index = SEP;
    else if (doy >= p[OCT] && doy <= (p[NOV] - 1)) month_index = OCT;
    else if (doy >= p[NOV] && doy <= (p[DEC] - 1)) month_index = NOV;
    else month_index = DEC;
    return month_index;
}


