#include <math.h>
#include "reference_ET_functions.h"

//Functions to calculate reference ET based on Ntional Engineering Handbook
//part 623


double CalcCoefTermHumidity(const double temperature)
{
    //temperature (°F)
    //output:
    //0.622 K1λρ/BP
    return 82.0 - 0.186 * temperature;                                           //Eq. 2-41
}
//______________________________________________________________________________
double CalcSlopeOfVapPresCurve(const double temperature)
{
    //temperature (°F)
    //output:
    //∆: slope of vapor pressure curve (mb/°F)
    return 0.051 * pow((164.8 + temperature) / 157.0, 7.0);                      //Eq. 2-16
}
//______________________________________________________________________________
double CalcHeatOfVapWater(const double temperature)
{
    //temperature (°F)
    //output:
    //λ: heat of vaporization of water (langs/in)
    return 1543.0 - 0.796 * temperature;                                         //Eq. 2-19
}
//______________________________________________________________________________
double CalcBP(const double elev)
{
    //elev: elevation above sea level (ft)
    //output:
    //BP: barometric pressure (mb)
    return 1013 * pow(1.0 - elev / 145350.0, 5.26);                              //Eq. 2-10
}
//______________________________________________________________________________
double CalcPsychrometricConstant(const double bp,
                                 const double heat_of_vap_of_water)
{
    //bp:mean barometric pressure (mb)
    //heat_of_vap_of_water: λ: heat of vaporization (lang/in of water)
    //output:
    //γ: psychrometric constant (mb/°F)
    return Specific_Heat_Dry_Air * bp / (0.622 * heat_of_vap_of_water);          //Eq. 2-18
}
//______________________________________________________________________________
double CalcSoilHeatFlux(const double t_current_day, const double t_p3days)
{
    //t_current_day: Ta = average air temperature for the current day (°F)
    //t_p3days: Tp = mean air temperature for the preceding three days (°F)
    //output:
    //G: soil heat flux (lang/d)
    const double Cs = 5.0;                                                       // Wright (1982). an empirical specific heat coefficient for the soil (lang/°F/d)
    return Cs * (t_current_day - t_p3days);                                      //Eq. 2-36
}
//______________________________________________________________________________
double CalcNetAtmosEmittance(const int doy, const double ed)
{
    //doy: day of year (1-365)
    //ed: saturation vapor pressure at the mean dew point temperature (mb)
    //output:
    //ε′ = the net atmospheric emittance
    double a1 = 0.26 + 0.1 * exp(-pow(0.0154*(-170.0 + 0.986*(double)doy),2.0)); //factor to account for the change of emissivity because of day length:
                                                                                 //Eq. 2-34 note: different from Fig. 2-16
    return a1 - 0.044 * sqrt(ed);                                                //Eq. 2-33
}
//______________________________________________________________________________
double CalcSatVapPressure(const double temperature)
{
    //temperature: air temperature (°F)
    //output:
    //e° = saturated vapor pressure (mb)
    return pow((164.8 + temperature) / 157.0, 8.0);                              //Eq. 2-11
}
//______________________________________________________________________________
double CalcNetOutLongwRadiationClearday(const double tmax, const double tmin,
                                        const double net_atm_emittance)
{
    //tmax: daily maximum temperature (°F)
    //tmin: daily minimum temperature (°F)
    //net_atm_emittance: ε′ = net atmospheric emittance
    //output:
    //Rbo: The net outgoing longwave radiation on a clear day (lang/day)
    double Ts_4 = (pow(5./9.*tmax + 255.4, 4.0) + pow(5./9.*tmin + 255.4, 4.0))
                  / 2.0;                                                         //Eq. 2-32
                                                                                 //Ts: effective absolute temperature of the earth’s surface (°K)
    return net_atm_emittance * Stephan_Boltzman_Constant * Ts_4;                 //Eq. 2-31
}
//______________________________________________________________________________
double CalcClearskySolarRadiation(const double lat, const double elev,
                                  const int doy)
{
    //lat: latitude (°N)
    //elev: elevation above sea level (ft)
    //doy = day of the year (1–365)
    //output:
   //Rso: clear sky solar radiation (lang/day)
    double A = 753.6 - 6.53 * lat + 0.0057 * elev;
    double B = -7.1 + 6.40 * lat + 0.0030 * elev;
    return A + B * cos(0.9863 * ((double)doy - 170.0) * PI / 180.0);             //Eq. 2-29
}
//______________________________________________________________________________
double CalcSolarRadiation(const int bright_sunshine_hours,
                          const int maximum_sunshine_hours,
                          const double clear_sky_radiation)
{
    //bright_sunshine_hours: actual bright sunshine hours (n)
    //maximum_sunshine_hours: maximum possible sunshine hours per day (N)
    //clear_sky_radiation: clear sky solar radiation (lang/day)
    //output:
    //Rs: incoming solar radiation (lang/d)
    return (0.25 + 0.5 * bright_sunshine_hours / maximum_sunshine_hours)
            * clear_sky_radiation;                                               //Eq. 2-35 Doorenbos and Pruitt (1977)
}
//______________________________________________________________________________
double CalcNetOutLongwRadiation(const double Rs, const double Rso,
                                const double Rbo)
{
    //Rs: incoming solar radiation (lang/d)
    //Rso: the amount of incident solar radiation on a clear day (lang/day)
    //Rbo: the net outgoing longwave radiation on a clear day (lang/d)
    //output:
    //Rb: The net outgoing longwave radiation (lang/d)
    double a, b;
    if (Rs / Rso > 0.7) {
        a = 1.126;
        b = -0.07;
    } else {
        a = 1.017;
        b = -0.06;
    }
    return (a * Rs / Rso + b) * Rbo;                                             //Eq. 2-28
}
//______________________________________________________________________________
double CalcSolarDeclinationAngle(const int doy)
{
    //doy = day of the year (1–365)
    //output:
    //θd = solar declination angle (degrees)
    return RADIANS_TO_DEGREES(asin(0.39795 * cos(
             DEGREES_TO_RADIANS(0.98563 * ((double)doy - 173.0)))));             //solar declination angle (degrees)
                                                                                 //Eq. 2-27
}
//______________________________________________________________________________
double CalcRefgrassAlbedo(const double Rs, const double Rb,
                          const double lat, const int doy)
{
    //Rs: incoming solar radiation (lang/d)
    //Rb: net outgoing longwave radiation (lang/d)
    //lat: latitude (°N)
    //doy = day of the year (1–365)
    //output:
    //albedo: the mean daytime albedo for a grass reference crop
    double theta_d = CalcSolarDeclinationAngle(doy);                             //solar declination angle (degrees)
    double theta_m = RADIANS_TO_DEGREES(asin(
                          sin(DEGREES_TO_RADIANS(theta_d))
                           * sin(DEGREES_TO_RADIANS(lat)) +
                          cos(DEGREES_TO_RADIANS(theta_d))
                           * cos(DEGREES_TO_RADIANS(lat))
                                            ));                                  //solar altitude at solar noon (degrees)
                                                                                 //Eq. 2-26
    double albedo = 0.108 + 0.000939 * theta_m + 0.257 * exp(-theta_m / 57.3);   //Eq. 2.25
    return albedo;
}
//______________________________________________________________________________
double CalcNetRadiation(const double Rs, const double Rb, const double albedo)
{
    //Rs: incoming solar radiation (lang/d)
    //Rb: net outgoing longwave radiation (lang/d)
    //albedo: the mean daytime albedo
    //doy = day of the year (1–365)
    //output:
    //Rn: net radiation (lang/d)
    return (1.0 - albedo) * Rs - Rb;                                             //Eq. 2-24
}
//______________________________________________________________________________
double CalcAerodynamicResistance(const double Zw, const double Zp,
                                 const double hc, const double Uz)
{
    //Zw = the height of wind speed measurement (ft)
    //Zp = the height of the humidity (psychrometer) and temperature measurements (ft)
    //hc: the height of the crop(inch). 5 inch for reference crop
    //Uz = the daily wind run at height Zw (mi/d)
    //output:
    //ra: aerodynamic resistance to sensible heat and vapor transfer (d/mi)
    return log(97.56 * Zw / hc - 5.42) * log(975.6 * Zp / hc - 54.2)
             / (0.168 * Uz);                                                     //Eq. 2-45
}
//______________________________________________________________________________
double CalcPsychrometricConstantAdjust(const double gamma, const double rc,
                                       const double ra)
{
    //gamma: γ psychrometric constant (mb/°F)
    //rc: surface resistance to vapor transport (d/mi)
    //ra: aerodynamic resistance to sensible heat and vapor transfer (d/mi)
    //output:
    //γ*: for Penmon_Monteith method (mb/°F)
    return gamma * (1.0 + rc / ra);                                              //Eq. 2-39
}
//______________________________________________________________________________
double CalcPenmonMonteithET(const double lamta,
                               const double delta,
                               const double gamma,
                               const double gamma_adj,
                               const double Rn,
                               const double G,
                               const double coef_vap,
                               const double ez0,
                               const double ez,
                               const double ra)
{
    //lamta: λ = heat of vaporization of water (lang/in)
    //delta: ∆ = slope of the vapor pressure curve (mb/°F)
    //gamma: γ (psychrometric constant) (mb/°F)
    //gamma_adj: γ* adjusted γ (psychrometric constant) from ra and rc (mb/°F)
    //Rn = net radiation (lang/d)
    //G = soil heat flux (lang/d)
    //coef_vap: 0.622K1λρ/BP
    //ezo = average saturated vapor pressure (mb)
    //ez = actual vapor pressure (mb)
    //ra = aerodynamic resistance to sensible heat and vapor transfer (d/mi)
    //output:
    //ETo = the evapotranspiration rate for a grass reference crop (in/d)
    return (1.0 / lamta) * (((delta / (delta + gamma_adj)) * (Rn - G))
                            + ((gamma / (delta + gamma_adj)) * coef_vap
                               * (ez0 - ez) / ra)
                           );                                                    //Eq.2-38
}
//______________________________________________________________________________
double CalcPenmonMonteithETFromWeather(const double lat,
                                          const double elev,
                                          const int doy,
                                          const double tmax,
                                          const double tmin,
                                          const double td,
                                          const double rmax,
                                          const double rmin,
                                          const double Rs,
                                          const double Uz,
                                          const double t_yesterday,
                                          const double t_2_days_ago,
                                          const double t_3_days_ago,
                                          const double hc,
                                          const double Zw,
                                          const double Zp,
                                          const double rc,
                                          double &albedo)
{
    //lat                                                                        //(°N)
    //elev                                                                       //(ft)
    //doy                                                                        //day of year
    //tmax                                                                       //(°F)
    //tmin                                                                       //(°F)
    //td                                                                         //(°F) dew temperature
    //rmax                                                                       //(%) relative humidity
    //rmin                                                                       //(%) relative humidity
    //Rs                                                                         //(langs/d)
    //Uz                                                                         //(miles/d)
    //hc                                                                         //(inch) reference crop height
    //Zw                                                                         //(ft) height of wind speed measurement
    //Zp                                                                         //(ft) height of air temperature measurement
    //rc                                                                         //(days/mile)
    //output:
    //ETo = the evapotranspiration rate for a grass reference crop (in/d)

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
    double Rn = CalcNetRadiation(Rs,Rb,albedo);                                  //(land/d) net radiation for reference grass
    double ra = CalcAerodynamicResistance(Zw,Zp,hc,Uz);                          //(d/mi)
    double gamma_adj = CalcPsychrometricConstantAdjust(gamma,rc,ra);
    double coef_vap = CalcCoefTermHumidity(tavg);
    double ET0 = CalcPenmonMonteithET(lamta,delta,gamma,gamma_adj,Rn,G,
                                      coef_vap,ez0,ed,ra);
    return ET0;
}
//______________________________________________________________________________
double CalcAdjBr(const double RHa, const double Ud)
{
    //RHa = average relative humidity (%)
    //Ud  = average daytime wind speed (mi/d)
    //output:
    //br: adjustment factor depending on the average relative humidity and daytime wind speed
    //for Radiation method of reference ET Doorenbos and Pruitt (1977)
    return 1.06 - 0.0013 * RHa + 8.38e-4 * Ud - 3.73e-6 * RHa * Ud
             - 0.315e-4 * RHa * RHa - 3.82e-7 * Ud *Ud;                          //Table 2-13
}
//______________________________________________________________________________
double CalcDaytimeWind(const double U, const double Ur)
{
    //U = daily wind run (mi/d)
    //Ur = ratio of daytime to nighttime wind speeds
    //output
    //Ud = daytime wind speed (mi/hr)
    return U * Ur / (12.0 * (1.0 + Ur));                                         //Eq. 2-23
}
//______________________________________________________________________________
double CalcRadiationMethodET(const double lamta,
                             const double delta,
                             const double gamma,
                             const double Rs,
                             const double br)
{
    //lamta: λ = heat of vaporization of water (lang/in)
    //delta: ∆ = slope of the vapor pressure curve (mb/°F)
    //gamma: γ (psychrometric constant) (mb/°F)
    //Rs = incoming solar radiation (lang/d)
    //br = adjustment factor depending on the average relative humidity and daytime wind speed
    //output:
    //ETo = the evapotranspiration rate for a grass reference crop (in/d)
    //The radiation method from Doorenbos and Pruitt (1977)
    //mainly for arid climates
    return -0.012 + (delta / (delta + gamma)) * br * Rs / lamta;                 //Eq.2-49
}
//______________________________________________________________________________
double CalcMeanDailyPercentAnnDaytime(const int doy, const double lat)
{
    //doy: day of yeay (1-365)
    //lat: latitude (°N)
    //output:
    //p: mean daily percent of annual daytime hours
    double theta_d = CalcSolarDeclinationAngle(doy);
    double theta_d_rad = DEGREES_TO_RADIANS(theta_d);
    double lat_rad = DEGREES_TO_RADIANS(lat);
    double temp = -sin(theta_d_rad) * sin(lat_rad) /
                  (cos(theta_d_rad) * cos(lat_rad));
    return 0.00304 * RADIANS_TO_DEGREES(acos(temp));                             //Eq. 2-53
}
//______________________________________________________________________________
double CalcFAOBlaneyCriddleET(const double lat,
                               const double elev,
                               const int doy,
                               const double tavg,
                               const double rhmin,
                               const double Ud,
                               const double ratio_act_to_pot_sunshine)
{
    //Jensen, et al.(1990) found that the version of the Blaney-Criddle
    //method developed by Doorenbos and Pruitt (1977) was the most accurate
    //temperature-based method evaluated for estimating crop ETo.
    //FAO-Blaney-Criddle method

    //elev = elevation above sea level (ft).
    //lat: latitude (°N)
    //doy: day of yeay (1-365)
    //tavg: Average daily temperature (°F)
    //rhmin: Mean minimum relative humidity (%)
    //Ud: Mean daytime wind speed at 2 meters above the ground (mi/d)
    //output:
    //ETo = the evapotranspiration rate for a grass reference crop (in/d)
    double p = CalcMeanDailyPercentAnnDaytime(doy,lat);
    double ce = 0.01 + 3.049e-7 * elev;                                          //adjustment factor based on elevation above sea level
    double at = 3.937 * (0.0043 * rhmin - ratio_act_to_pot_sunshine - 1.41);     //at & bt: adjustment factors based on the climate of the region
    double bn = 0.82 - 0.0041 * rhmin + 1.07 * ratio_act_to_pot_sunshine
                - 0.006 * rhmin * ratio_act_to_pot_sunshine;                     //Table 2-16
    double bu = (1.23 * Ud - 0.0112 * rhmin * Ud) / 1000.0;
    double bt = bn + bu;                                                         //E1. 2-51
    return ce * (at + bt * p * tavg);                                            //Eq. 2-50
}
//______________________________________________________________________________
double CalcTAW(const double Rd, const double theta_fc, const double theta_pwp)
{
    //θfc  = volumetric water content at field capacity (%)
    //θpwp = volumetric water content at the permanent wilting point (%)
    //Rd   = root zone depth (in)
    //output:
    //The total available soil water (TAW) (in)
    return Rd * (theta_fc - theta_pwp) / 100.0;                                  //Eq. 2-58
}
//______________________________________________________________________________
double CalcAW(const double Rd, const double theta, const double theta_pwp)
{
    //θv = current volumetric water content (%)
    //θpwp = volumetric water content at the permanent wilting point (%)
    //Rd   = root zone depth (in)
    //output:
    //AW = available soil water (in)
    return Rd * (theta - theta_pwp) / 100.0;                                     //Eq. 2-59
}
//______________________________________________________________________________
double CalcASW(const double AW, const double TAW)
{
    //AW  = available soil water (in)
    //TAW = The total available soil water (in)
    //output:
    //ASW: The percent of the total available water that is stored in the root zone
    return (AW / TAW) * 100.0;                                                   //Eq. 2-60
}
//______________________________________________________________________________
double CalcWaterStressFactor(const double ASW, const double ASWc)
{
    //ASW: The percent of the total available water that is stored in the root zone
    //ASWc: The critical value of ASW
    //output:
    //Ks = stress factor to reduce water use for stressed crops
    return ASW < ASWc ? (ASW / ASWc) : 1.0;                                      //Eq. 2-61
}
//______________________________________________________________________________
double CalcWetSoilEvapFactor(const double Fw, const double Kcb,
                             const int elap_wet_days, const int drying_days)
{
    //Fw = the fraction of the soil surface wetted
    //t  = elapsed time since wetting, days
    //td = days required for the soil surface to dry
    //Kcb: basal crop coefficient
    //output:
    //Kw: The wet soil evaporation factor Wright (1981)
    double ft = 1.0 - sqrt(elap_wet_days / drying_days);                         //wet soil evaporation decay function
    if (ft < 0.0) ft = 0.0;
    return Kcb < 1.0 ? (Fw * (1.0 - Kcb) * ft) : 0.0;                            //Eq. 2-62
}
//______________________________________________________________________________
double CalcTotalWetSoilEvap(const double Pf, const double Fw,
                            const double Kcb_avg, const double ET0_avg)
{
    //Pf  = wet soil persistence factor. Hill, et al. (1983) = sum f(t) wet soil evaporation decay function (Table 2-29)
    //Fw  = the fraction of the soil surface wetted
    //Kcb = the average basal crop coefficient during the drying period
    //ETo = the average daily reference crop evapotranspiration during the drying period (in/d)
    //output:
    //Ews: The total wet soil evaporation from a wetting event (in)
    return Kcb_avg < 1 ? (Pf * Fw * (1 - Kcb_avg) * ET0_avg) : 0.0;              //Eq. 2-63
}
//______________________________________________________________________________
double CalcAverageWetSoilEvapFactor(const int Rf, const int td)
{
    //Rf = recurrence interval of wetting days
    //td = drying time for the respective soil
    //i  = days since wetting
    //output:
    //Af = the average wet soil evaporation factor
    double Af = 0;
    for (int i = 0; i < Rf; i++) {
        if (i <= td)
            Af += (1.0 - sqrt((double)i / (double)td)) / (double)Rf;             //Table 2-30
    }
}
//______________________________________________________________________________
double CalcAvgCropCoef(const double Ks_avg, const double Kcb_avg,
                       const double Fw, const double Af)
{
    //Ks: stress factor to reduce water use for stressed crops
    //Kcb: basal crop coefficient
    //Fw: the fraction of the soil surface wetted
    //Af: the average wet soil evaporation factor
    //avg: the average value of each parameter over the calculation period.
    //output:
    //Ka: The average crop coefficient
    return Ks_avg * Kcb_avg + Fw * (1.0 - (Kcb_avg > 1.0 ? 1.0 : Kcb_avg)) * Af; //Eq. 2-66
}
//______________________________________________________________________________
double CalcAvgCropCoefNongrowingSeason(const int fp, const double ET0)
{
    //fp = interval between significant rains or irrigations (days)
    //ETo = average reference crop evapotranspiration for the period (in/d)
    //output:
    //Ka = average crop coefficient during the nongrowing season                 //Eq.2-67 Doorenbos and Pruitt (1977)
    if (fp < 4)
        return (1.286 - 0.27 * (double)fp) *
                 exp((0.254 - 1.07 * log((double)fp)) * ET0);
    else
        return 2.0 * pow((double)fp, -0.49) *
                 exp((-0.51 - 1.02 * log((double)fp)) * ET0);
}
//______________________________________________________________________________
double CalcFractionGrowingSeason(const double gddi, const double gddm)
{
    //GDDi = cumulative growing degree days on day i
    //GDDm = cumulative growing degree days needed for maturity
    //output:
    //Fs: the fraction of the growing season
    return gddi > gddm ? 1.0 : (gddi / gddm);                                    //Eq.2-68
}
//______________________________________________________________________________
double CalcAvgMonthlyEffectivePrecipitation(const double D,
                                            const double Pt, const double ETc)
{

    //D = the usable soil water storage (in)
    //Pt = monthly mean precipitation (in)
    //ETc = average monthly crop evapotranspiration (in)
    //output:
    //Pe = average monthly effective monthly precipita-tion (in)
    double SF = 0.531747 + 0.295164*D - 0.057697*D*D + 0.003804*D*D*D;           //Eq. 2-85 soil water storage factor
    double Pe = SF * (0.70917 * pow(Pt, 0.82416) - 0.11556)
                  * pow(10.0, 0.02426 * ETc);                                    //Eq.2-84
    if (Pe < 0) Pe = 0;
    double minp = Pt < ETc ? Pt : ETc;
    return Pe > minp ? minp : Pe;
}
