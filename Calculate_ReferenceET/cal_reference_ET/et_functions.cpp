//Attribute VB_Name = "PM_ET_Calculations"
//170908 Mingliang Liu converted the VB code from Claudio Stockle.
#include <math.h>
#include <algorithm>
#include "et_functions.h"
//______________________________________________________________________________
double calc_SatVP(const double T)
{   //T: (°C)
    return 0.6108 * exp(17.27 * T / (T + 237.3));                                //(kPa)
}
//______________________________________________________________________________
double calc_VP(const double esTmax, const double esTmin, const double RHmax,
  const double RHmin)
{   //RHmax, RHmin:(%) esTmax, esTmin: SatVP from Tmax and Tmin (kPa)
    return (esTmin * RHmax / 100.0 + esTmax * RHmin / 100.0) / 2.0;              //(kPa)
}
//______________________________________________________________________________
double calc_VPD(const double esTmax, const double esTmin, const double ea)
{
    return (esTmax + esTmin) / 2.0 - ea;                                         //(kPa)
}
//______________________________________________________________________________
double f_arccos(const double x)
{
    return atan(-x / sqrt(-x * x + 1.0)) + 2.0 * atan(1.0);
}
//______________________________________________________________________________
double calc_PotRad(const double Lat, const int DOY)
{
    const double Pi = 3.14159;
    const double Solar_Constant = 118.08;
    double Lat_Rad = Lat * Pi / 180.0;
    double doy_sun_radians = 2.0 * Pi * (double)DOY / 365.0;
    double dr = 1.0 + 0.033 * cos(doy_sun_radians);
    double SolDec = 0.409 * sin(doy_sun_radians - 1.39);
    double SunsetHourAngle = f_arccos(-tan(Lat_Rad) * tan(SolDec));
    double Term = SunsetHourAngle * sin(Lat_Rad) * sin(SolDec)
                  + cos(Lat_Rad) * cos(SolDec) * sin(SunsetHourAngle);
    return Solar_Constant * dr * Term / Pi;                                      //(MJ/m2/day)
}
//______________________________________________________________________________
double calc_NetRad(const double ER, const double Rs, const double ea,
  const double Tmax, const double Tmin)
{   //Calculate shortwave net radiation
    //ER: (MJ/m2/day) potential solar radiation
    //Rs: (MJ/m2/day) shortwave radiation
    //ea: (kPa) daily average vapor pressure
    const double albedo = 0.23;
    double Rns = (1.0 - albedo) * Rs;
    //Calculate cloud factor
    double F_Cloud = 1.35 * (Rs / (ER * 0.75)) - 0.35;
    //Calculate humidity factor
    double F_Hum = (0.34 - 0.14 * sqrt(ea));
    //Calculate Isothermal LW net radiation
    double LWR = 4.903e-9 * (pow(Tmax + 273.0, 4) + pow(Tmin + 273.0, 4)) / 2.0;
    double Rnl = LWR * F_Cloud * F_Hum;
    return Rns - Rnl;                                                            //(MJ/m2/day)
}
//______________________________________________________________________________
double calc_AeroRes(const double Uz, const double z, const double crop_height)
{   //Uz: (m/s) z: (m) screen hight
    //CropHeight (m) 0.12m for short grass 0.5m for Alfalfa
    double U2 = 0;
    if (is_approximately<double>(z, 2)) U2 = Uz;
    else U2 = Uz * (4.87 / (log(67.8 * z - 5.42)));
    U2 = U2 * 86400.0;                                                           //Convert to m/day
    const double d = crop_height * 0.667;                                         //0.08;
    const double zom = crop_height * 0.123;                                      //0.01476;
    const double zoh = crop_height * 0.0123;                                     //0.001476;
    const double zm = 2.0;
    const double zh = 2.0;
    const double VK = 0.41;
    double Term1 = log((zm - d) / zom);
    double term2 = log((zh - d) / zoh);
    return Term1 * term2 / (VK * VK * U2);                                       //(day/m)
}
//______________________________________________________________________________
double calc_DT(const double Tmean, const double esTmean)
{   //esTmean: (kPa) sat vapor pressure estimated from Tmean
    return 4098.0 * esTmean / pow(Tmean + 237.3, 2);                             //(kPa/°C)
}
//______________________________________________________________________________
double calc_Lambda(const double Tmean)
{
    return 2.501 - 0.002361 * Tmean;                                             //(MJ/kg)
}
//______________________________________________________________________________
double calc_Gamma(const double Lambda, const double Elev)
{   //Psychrometric constant
    const double Cp = 0.001013;
    double P = 101.3 * pow((293.0 - 0.0065 * Elev) / 293.0, 5.26);
    return Cp * P / (0.622 * Lambda);                                            //(kPa/°C)
}
//______________________________________________________________________________
double calc_ETRadTerm(const double Delta, const double Gamma,
  const double Lambda, const double Rn, const double rc, const double ra)
{   //Delta:(kPa/°C) Rn: ((MJ/m2/day)) net radiation
    double ETRadTerm = Delta * Rn / (Delta + Gamma * (1.0 + rc / ra));
    return ETRadTerm / Lambda;                                                   //(mm)
}
//______________________________________________________________________________
double calc_ETAeroTerm(const double Delta, const double Gamma,
  const double Lambda, const double rc, const double ra, const double VPD,
  const double Tmean, const double Elev)
{
    const double Cp = 0.001013;
    double P = 101.3 * pow((293.0 - 0.0065 * Elev) / 293.0, 5.26);
    double Tkv = 1.01 * (Tmean + 273.0);
    double AirDensity = 3.486 * P / Tkv;
    double VolHeatCap = Cp * AirDensity;
    double ETAeroTerm = (VolHeatCap * VPD / ra) /
                        (Delta + Gamma * (1.0 + rc / ra));
    return ETAeroTerm / Lambda;                                                  //(mm)
}
//______________________________________________________________________________
double calc_RHtoDP(const double Tair, const double RH)
{
    double es = 0.6108 * exp(17.27 * Tair / (Tair + 237.3));
    double ea = es * RH / 100.0;
    return (237.3 * log(ea / 0.6108)) / (17.27 - log(ea / 0.6108));
}
//______________________________________________________________________________
double calc_referenceET_PM(const double lat, const double altitude,
  const double screen_height, const double crop_height, const double canopy_resistance,
  const int DOY, double tmax, double tmin,
  double rs, double rhmax, double rhmin, double uz,
  double &et_aero_term, double &et_rad_term)
{   //lat: (degree); screen_height: (m); tmax, tmin: (°C); rs: (MJ/m2/day)
    //rhmax, rhmin: (%); uz: (m/s)
    //canopy_resistance 70s/m for short grass  45s/m for alfalfa
    //crop_height 0.12 for short grass  0.5 for alfalfa
    if (tmax < tmin)   std::swap<double>(tmax,tmin);
    if (rhmax < rhmin) std::swap<double>(rhmax,rhmin);
    if (uz < 0) uz = 0;
    if (rs < 0) rs = 0;
    double Tmean    = (tmax + tmin) / 2.0;
    double esTmean  = calc_SatVP(Tmean);
    double esTmax   = calc_SatVP(tmax);
    double esTmin   = calc_SatVP(tmin);
    double delta    = calc_DT(Tmean, esTmean);
    double lambda   = calc_Lambda(Tmean);
    double gamma    = calc_Gamma(lambda,altitude);
    double rc       = canopy_resistance / 86400.0;                                            //(day/m)
    double ra       = calc_AeroRes(uz, screen_height, crop_height);                           //(day/m)
    double ea       = calc_VP(esTmax, esTmin, rhmax, rhmin);
    double vpd      = calc_VPD(esTmax, esTmin, ea);
    et_aero_term = calc_ETAeroTerm(delta, gamma, lambda, rc, ra, vpd,
                                   Tmean, altitude);
    double er       = calc_PotRad(lat, DOY);
    double rn       = calc_NetRad(er, rs, ea, tmax, tmin);
    et_rad_term  = calc_ETRadTerm(delta, gamma, lambda, rn, rc, ra);
    return et_aero_term + et_rad_term;
}
//______________________________________________________________________________
double calc_referenceET_PT(const double lat, const double altitude,
  const double screen_height, const double crop_height, const double canopy_resistance,
  const int DOY, double tmax, double tmin,
  double rs, double rhmax, double rhmin, double uz)                              //Priestley Taylor
{   //lat: (degree); screen_height: (m); tmax, tmin: (°C); rs: (MJ/m2/day)
    //rhmax, rhmin: (%); uz: (m/s)
    //canopy_resistance 70s/m for short grass  45s/m for alfalfa

    const double alpha = 1.26;
    if (tmax < tmin)   std::swap<double>(tmax,tmin);
    if (rhmax < rhmin) std::swap<double>(rhmax,rhmin);
    if (uz < 0) uz = 0;
    if (rs < 0) rs = 0;
    double Tmean    = (tmax + tmin) / 2.0;
    double esTmean  = calc_SatVP(Tmean);
    double esTmax   = calc_SatVP(tmax);
    double esTmin   = calc_SatVP(tmin);
    double delta    = calc_DT(Tmean, esTmean);
    double lambda   = calc_Lambda(Tmean);
    double gamma    = calc_Gamma(lambda,altitude);
    double rc       = canopy_resistance / 86400.0;                                            //(day/m)
    double ra       = calc_AeroRes(uz, screen_height, crop_height);                           //(day/m)
    double ea       = calc_VP(esTmax, esTmin, rhmax, rhmin);
    double er       = calc_PotRad(lat, DOY);
    double rn       = calc_NetRad(er, rs, ea, tmax, tmin);
    double et_rad_term  = calc_ETRadTerm(delta, gamma, lambda, rn, rc, ra);
    return alpha * et_rad_term;                                                  //(mm)
}
//______________________________________________________________________________
double calc_referenceET_PT_from_RadTerm(const double rad_term)                   //Priestley Taylor
{   //rad_term: from PM method
    const double alpha = 1.26;
    return alpha * rad_term;                                                     //(mm)
}
