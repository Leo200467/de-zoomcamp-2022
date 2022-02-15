select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

select *
from `halogen-byte-339200`.`de_staging`.`stg_green_tripdata`
where tripid is null



      
    ) dbt_internal_test