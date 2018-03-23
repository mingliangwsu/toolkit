#include <iostream>
#include "reference_ET_functions.h"
#define xPENMON_MONTEITH
#define xRADIATION_METHOD
#define FAO_Blaney_Criddle_METHOD
#define xCALC_ET0_FROM_FUNCTION_WITH_WEATHER_INPUT

int main(int argc, char *argv[])
{
    //Testing Penmon-Monteith equation
    double lat = 40;                                                             //(°N)
    double elev = 3000;                                                          //(ft)
    int doy = 201;                                                               //day of year
    double tmax = 94;                                                            //(°F)
    double tmin = 66;                                                            //(°F)
    double td   = 62;                                                            //(°F) dew temperature
    double rmax = 88;                                                            //(%) relative humidity
    double rmin = 34;                                                            //(%) relative humidity
    double Rs   = 695;                                                           //(langs/d)
    double Uz   = 350;                                                           //(miles/d)
    double t_yesterday = 86;
    double t_2_days_ago = 83;
    double t_3_days_ago = 77;

    const double hc = 5;                                                         //(inch) reference crop height
    const double Zw = 6.6;                                                       //(ft) height of wind speed measurement
    const double Zp = 4.9;                                                       //(ft) height of air temperature measurement
    const double rc = 1.22;                                                      //(days/mile) reference crop

    double ET0;
    double albedo = -1.0;                                                        //negtive means does not provide and will be calculated

#ifndef CALC_ET0_FROM_FUNCTION_WITH_WEATHER_INPUT
    double tp = (t_yesterday + t_2_days_ago + t_3_days_ago) / 3.0;

    double e0_tmax = CalcSatVapPressure(tmax);
    double e0_tmin = CalcSatVapPressure(tmin);
    double ez0 = (e0_tmax + e0_tmin) / 2.0;

    double tavg = (tmax + tmin) / 2.0;
    double delta = CalcSlopeOfVapPresCurve(tavg);                                //∆, for average temp (mb/°F)
    double lamta = CalcHeatOfVapWater(tavg);                                     //Heat of vaporization (λ) (lang/in)
    double BP = CalcBP(elev);                                                    //Barometric pressure (BP) (mb)
    double gamma = CalcPsychrometricConstant(BP,lamta);                          //(mb/°F)
    double G = CalcSoilHeatFlux(tavg,tp);                                        //Soil heat flux (lang/d)
    double ed = CalcSatVapPressure(td);                                          //saturation vapor pressure at the mean dew point temperature (mb)
    double emitence = CalcNetAtmosEmittance(doy,ed);
    double Rbo = CalcNetOutLongwRadiationClearday(tmax,tmin,emitence);           //(lang/d) The net outgoing longwave radiation on a clear day
    double Rso = CalcClearskySolarRadiation(lat,elev,doy);                       //(lang/d) the amount of incident solar radiation on a clear day
    double Rb = CalcNetOutLongwRadiation(Rs,Rso,Rbo);                            //(lang/d) The net outgoing longwave radiation
    if (albedo < 0) albedo = CalcRefgrassAlbedo(Rs, Rb, lat, doy);
    double Rn = CalcNetRadiation(Rs,Rb,albedo);                         //(land/d) net radiation for reference grass
    double ra = CalcAerodynamicResistance(Zw,Zp,hc,Uz);                          //(d/mi)
    double gamma_adj = CalcPsychrometricConstantAdjust(gamma,rc,ra);
    double coef_vap = CalcCoefTermHumidity(tavg);
#ifdef PENMON_MONTEITH
    ET0 = CalcPenmonMonteithET(lamta,delta,gamma,gamma_adj,Rn,G,
            coef_vap,ez0,ed,ra);
#endif //PENMON_MONTEITH
#ifdef RADIATION_METHOD
    double U = 260; //(mi/d)
    double Ur = 2.0;
    double Ud = 24.0 * CalcDaytimeWind(U, Ur);
    double RHa = 61; //(%)
    double br = CalcAdjBr(RHa,Ud);
    lamta = 1484;
    delta = 0.97;
    gamma = 0.34;
    Rs = 650;
    ET0 = CalcRadiationMethodET(lamta,delta,gamma,Rs,br);
#endif //RADIATION_METHOD

#ifdef FAO_Blaney_Criddle_METHOD
    double rhmin = 35;
    lat = 38;
    elev = 2600;
    double ratio = 0.74;                                                         //the mean ratio of actual to possible sun-shine hours (n/N)
    tavg = 74.5;
    double Ud = 346;
    ET0 = CalcFAOBlaneyCriddleET(lat,elev,doy,tavg,rhmin,Ud,ratio);
#endif

#else //CALC_ET0_FROM_FUNCTION_WITH_WEATHER_INPUT
#ifdef PENMON_MONTEITH
    ET0 = CalcPenmonMonteithETFromWeather(lat,elev,doy,
            tmax,tmin,td,rmax,rmin,Rs,Uz,
            t_yesterday,t_2_days_ago,t_3_days_ago,
            hc,Zw,Zp,rc,albedo);
#endif //PENMON_MONTEITH
#endif //CALC_ET0_FROM_FUNCTION_WITH_WEATHER_INPUT

    std::clog << "ET0:" << ET0 << std::endl;
    return 0;
}
