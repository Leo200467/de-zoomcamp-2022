
    
    

with child as (
    select dropoff_locationid as from_field
    from `halogen-byte-339200`.`de_staging`.`stg_yellow_tripdata`
    where dropoff_locationid is not null
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


