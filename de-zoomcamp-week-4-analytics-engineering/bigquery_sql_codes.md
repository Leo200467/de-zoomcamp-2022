### Question 1: What is the count of records in the model fact_trips after running all models with the test run variable disabled and filtering for 2019 and 2020 data only (pickup datetime)

```
SELECT COUNT(pickup_datetime) 
FROM `halogen-byte-339200.de_prod.fact_trips` 
WHERE pickup_datetime BETWEEN '2019-01-01' AND '2020-12-31' 
LIMIT 1000
```

#### Result: 61.567.786

### Question 2: What is the distribution between service type filtering by years 2019 and 2020 data as done in the videos . (Yellow/Green)

```
Proportion - yellow-> 56100630, green -> 6304783;
```

### Question 3: the count of records in the model stg_fhv_tripdata

```
SELECT COUNT(1) 
FROM `halogen-byte-339200.de_staging.stg_fhv_tripdata_2019` 
LIMIT 10
```

#### Result: 42.032.656

### Question 4: What is the count of records in the model fact_fhv_trips after running all dependencies with the test run variable disabled

```
SELECT COUNT(1)
FROM `halogen-byte-339200.de_staging.fhv_fact_trips`
LIMIT 1000
```

#### Result: 22.667.698

### Question 5: What is the month with the biggest amount of rides after building a tile for the fact_fhv_trips table 

```
SELECT 
    DATE_TRUNC(dropoff_datetime, month) as yyyymm,
    COUNT(1) 
FROM `halogen-byte-339200.de_staging.fhv_fact_trips` 
GROUP BY yyyymm 
ORDER BY yyyymm ASC 
LIMIT 1000 
```

Result: 

| Row | DATE (YYYY-MM-DD)       | COUNT    |
|-----|-------------------------|----------|
| 1   | 2019-01-01 00:00:00 UTC | 19838719 |
| 2   | 2019-02-01 00:00:00 UTC |   195572 |
| 3   | 2019-03-01 00:00:00 UTC |   105060 |
| 4   | 2019-04-01 00:00:00 UTC |   237803 |
| 5   | 2019-05-01 00:00:00 UTC |   242833 |
