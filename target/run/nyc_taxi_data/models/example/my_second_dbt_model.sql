

  create or replace view `halogen-byte-339200`.`dbt_lcardoso`.`my_second_dbt_model`
  OPTIONS()
  as -- Use the `ref` function to select from other models

select *
from `halogen-byte-339200`.`dbt_lcardoso`.`my_first_dbt_model`
where id = 1;

