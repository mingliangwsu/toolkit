#ifndef ET_FUNCTIONS_H
#define ET_FUNCTIONS_H
template <typename T> inline
bool is_approximately(const T &value,const T &target,const T &tolerance=0.0000001) //170614_141222
{
   T abs_diff = (target - value);
   if (abs_diff < 0.0) abs_diff = -abs_diff;
   bool it_is = (abs_diff <= tolerance) ;
   return it_is;
//170614 return ((value) <= ((target) +(tolerance))) && ((value) >= ((target) - (tolerance))); //170614
}
double calc_SatVP(const double T);
double calc_VP(const double esTmax, const double esTmin, const double RHmax,
  const double RHmin);
double calc_VPD(const double esTmax, const double esTmin, const double ea);
double f_arccos(const double x);
double calc_PotRad(const double Lat, const int DOY);
double calc_NetRad(const double ER, const double Rs, const double ea,
  const double Tmax, const double Tmin);
double calc_AeroRes(const double Uz, const double z);
double calc_DT(const double Tmean, const double esTmean);
double calc_Lambda(const double Tmean);
double calc_Gamma(const double Lambda, const double Elev);
double calc_ETRadTerm(const double Delta, const double Gamma,
  const double Lambda, const double Rn, const double rc, const double ra);
double calc_ETAeroTerm(const double Delta, const double Gamma,
  const double Lambda, const double rc, const double ra, const double VPD,
  const double Tmean, const double Elev);
double calc_RHtoDP(const double Tair, const double RH);
double calc_referenceET_PM(const double lat, const double altitude,
  const double screen_height, const int DOY, double tmax, double tmin,
  double rs, double rhmax, double rhmin, double uz,
  double &et_aero_term, double &et_rad_term);
double calc_referenceET_PT(const double lat, const double altitude,
  const double screen_height, const int DOY, double tmax, double tmin,
  double rs, double rhmax, double rhmin, double uz);
double calc_referenceET_PT_from_RadTerm(const double rad_term);
#endif // ET_FUNCTIONS_H
