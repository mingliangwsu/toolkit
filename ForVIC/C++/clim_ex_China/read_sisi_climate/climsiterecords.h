typedef struct ClimSiteRecords
{
   int id;                 //inner id
   int clim_id;            //the climate id in the climsite.txt file
   double lont;            //degree
   double lat;             //degree
   double elev;            //elevation of site (meter)
   int azoch_elev;
   int f_year;
   int f_mon;
   int t_year;
   int t_mon;
   double x_km;            //x coordinate (km)
   double y_km;            //y coordinate (km)
} ClimSiteRecords;
typedef struct ValidClimData
{
    int inner_id;
    double value;
} ValidClimData;
