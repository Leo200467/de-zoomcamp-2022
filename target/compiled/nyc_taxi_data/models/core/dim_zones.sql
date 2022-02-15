


select 
    locationid, 
    borough, 
    zone, 
    replace(service_zone,'Boro','Green') as service_zone
from `halogen-byte-339200`.`de_staging`.`taxi_zone_lookup`