#ifndef UINETCDF_CONSTANTS_H
#define UINETCDF_CONSTANTS_H
#include <string>
/* Handle errors by printing an error message and exiting with a
 * non-zero status. */
#define ERR(e) {printf("Error: %s\n", nc_strerror(e)); return false;}
#ifdef HISTORICAL_MET
#define NDAYS_NAME "day"
#else
#define NDAYS_NAME "time"
#endif
#define NLAT_NAME "lat"
#define NLONT_NAME "lon"
enum var_name {PPT,
               TMAX,
               TMIN,
               UAS,
               VAS,
               SRAD,
               RHMAX,
               RHMIN,
               VAR_COUNTS};
enum var_dimention_type {LAT_LON_DAY,
                         DAY_LAT_LON,
                         DAY_LON_LAT,
                         VAR_DIMENTION_TYPE_COUNTS};
enum output_var_type {OUT_PPT,
                      OUT_TAVG,
                      OUT_TMAX,
                      OUT_TMIN,
                      OUT_RHUM,
                      OUT_RHMAX,
                      OUT_RHMIN,
                      OUT_WIND,
                      OUT_SRAD,
                      OUT_PT,
                      OUT_PM,
                      output_var_type_counts};
enum season {SPRING,
             SUMMER,
             FALL,
             WINTER,
             ANNUAL,
             season_counts};
enum month {JAN,
            FEB,
            MAR,
            APR,
            MAY,
            JUN,
            JUL,
            AUG,
            SEP,
            OCT,
            NOV,
            DEC,
            ANN,
            month_counts};
#ifdef HISTORICAL_MET
enum his_var {his_PPT,
              his_TMAX,
              his_TMIN,
              his_VAS,
              his_SRAD,
              his_RHMAX,
              his_RHMIN,
              his_VAR_COUNTS};
enum jc_his_var {jc_his_PPT,
              jc_his_TMAX,
              jc_his_TMIN,
              jc_his_VAS,
              jc_his_SRAD,
              jc_his_RHMAX,
              jc_his_RHMIN,
              jc_his_TDEW,
              jc_his_VAR_COUNTS};
#else
enum future_var {fut_PPT,
                 fut_TMAX,
                 fut_TMIN,
                 fut_UAS,
                 fut_VAS,
                 fut_SRAD,
                 fut_RHMAX,
                 fut_RHMIN,
                 fut_VAR_COUNTS};
enum gcm_model {bcc_csm1_1,
                BNU_ESM,
                CanESM2,
                CNRM_CM5,
                CSIRO_Mk3_6_0,
                GFDL_ESM2G,
                GFDL_ESM2M,
                HadGEM2_CC365,
                HadGEM2_ES365,
                inmcm4,
                IPSL_CM5A_LR,
                IPSL_CM5A_MR,
                IPSL_CM5B_LR,
                MIROC5,
                MIROC_ESM_CHEM,
                MIROC_ESM,
                MRI_CGCM3,
                gcm_model_counts};
enum maca_rcps {historical,
                rcp45,
                rcp85,
                maca_rcps_counts};
#endif
#endif // UINETCDF_CONSTANTS_H
