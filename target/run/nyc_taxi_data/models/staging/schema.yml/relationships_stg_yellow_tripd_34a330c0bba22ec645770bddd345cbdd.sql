select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

with child as (
    select Pickup_locationid as from_field
    from `halogen-byte-339200`.`de_staging`.`stg_yellow_tripdata`
    where Pickup_locationid is not null
),

parent as (
    select locationid as to_field
    from `halogen-byte-339200`.`de_staging`.`taxi_zone_lookup`
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null



      
    ) dbt_internal_test