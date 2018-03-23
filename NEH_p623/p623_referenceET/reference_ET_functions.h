#ifndef REFERENCE_ET_FUNCTIONS
#define REFERENCE_ET_FUNCTIONS
const double Specific_Heat_Dry_Air = 0.339;                                      //(lang/in/°F)
const double Stephan_Boltzman_Constant = 11.71e-8;                               //(lang/(day °K4))
const double PI = 3.14159265;
#define DEGREES_TO_RADIANS(degree) (degree * PI / 180.0)
#define RADIANS_TO_DEGREES(radians) (radians * 180.0 / PI)
double CalcCoefTermHumidity(const double temperature);
double CalcSlopeOfVapPresCurve(const double temperature);
double CalcHeatOfVapWater(const double temperature);
double CalcBP(const double elev);
double CalcPsychrometricConstant(const double bp,
                                 const double heat_of_vap_of_water);
double CalcSoilHeatFlux(const double t_current_day, const double t_p3days);
double CalcNetAtmosEmittance(const int doy, const double ed);
double CalcSatVapPressure(const double temperature);
double CalcNetOutLongwRadiationClearday(const double tmax, const double tmin,
                                        const double net_atm_emittance);
double CalcClearskySolarRadiation(const double lat, const double elev,
                                  const int doy);
double CalcSolarRadiation(const int bright_sunshine_hours,
                          const int maximum_sunshine_hours,
                          const double clear_sky_radiation);
double CalcNetOutLongwRadiation(const double Rs, const double Rso,
                                const double Rbo);
double CalcSolarDeclinationAngle(const int doy);
double CalcRefgrassAlbedo(const double Rs, const double Rb,
                          const double lat, const int doy);
double CalcNetRadiation(const double Rs, const double Rb, const double albedo);
double CalcAerodynamicResistance(const double Zw, const double Zp,
                                 const double hc, const double Uz);
double CalcPsychrometricConstantAdjust(const double gamma, const double rc,
                                       const double ra);
double CalcPenmonMonteithET(const double lamta,
                               const double delta,
                               const double gamma,
                               const double gamma_adj,
                               const double Rn,
                               const double G,
                               const double coef_vap,
                               const double ez0,
                               const double ez,
                               const double ra);
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
                                          double &albedo);
double CalcAdjBr(const double RHa, const double Ud);
double CalcDaytimeWind(const double U, const double Ur);
double CalcRadiationMethodET(const double lamta,
                             const double delta,
                             const double gamma,
                             const double Rs,
                             const double br);
double CalcFAOBlaneyCriddleET(const double lat,
                               const double elev,
                               const int doy,
                               const double tavg,
                               const double rhmin,
                               const double Ud,
                               const double ratio_act_to_pot_sunshine);
#endif
