### CREATING EXTERNAL TABLE WITH ALL FHV DATA FROM 2019

```
CREATE OR REPLACE EXTERNAL TABLE `halogen-byte-339200.FHV_Data_2019.external_fhv_data_2019`

OPTIONS (
  format = 'parquet',
  uris = ['gs://dtc_data_lake_halogen-byte-339200/raw/fhv_tripdata_2019/fhv_tripdata_2019-*.parquet']
);
```

### Question 1: What is count for fhv vehicles data for year 2019

```
SELECT COUNT(1)  
FROM `halogen-byte-339200.FHV_Data_2019.external_fhv_data_2019` LIMIT 10
```

### Question 2: How many distinct dispatching_base_num we have in fhv for 2019

```
SELECT COUNT(DISTINCT dispatching_base_num)  
FROM `halogen-byte-339200.FHV_Data_2019.external_fhv_data_2019` LIMIT 10
```

### Question 3: Best strategy to optimise if query always filter by dropoff_datetime and order by dispatching_base_num

Dispatching_base_num is a string that will be used in clustering.

If query is allways filtered by dropoff_datetime, which format is datetime, a time-unit column.
Second step would be partitioning by dropoff_datetime, as is a time-unit column. 

### Question 4: What is the count, estimated and actual data processed for query which counts trip between 2019/01/01 and 2019/03/31 for dispatching_base_num B00987, B02060, B02279

```
CREATE OR REPLACE TABLE halogen-byte-339200.FHV_Data_2019.fhv_2019_tripdata_partitoned_clustered
CLUSTER BY dispatching_base_num AS 
PARTITION BY DATE(pickup_datetime)
SELECT * 
FROM `halogen-byte-339200.FHV_Data_2019.external_fhv_data_2019` 
WHERE dispatching_base_num = 'B00987' OR 
      dispatching_base_num = 'B02060' OR 
      dispatching_base_num = 'B02279';
```

### Question 5: What will be the best partitioning or clustering strategy when filtering on dispatching_base_num and SR_Flag

The dispatching_base_num column is a string and SR_Flag is a integer column. 
Filtered queries works better when using clustering, so the best strategy would be clustering both columns.

### Question 6: What improvements can be seen by partitioning and clustering for data size less than 1 GB

No improvements and also can be worse due to metadata. 

### Question 7: In which format does BigQuery save data

Columnar data format

#### Sources:
- [DTalks-DataEng-Data Warehouse](https://docs.google.com/presentation/d/1a3ZoBAXFk8-EhUsd7rAZd-5p_HpltkzSeujjRGB2TAI/edit#slide=id.g10c8bcef47f_0_9) 
- [DE-Zoomcamp 3.1.2 - Partitioning and Clustering](https://www.youtube.com/watch?v=-CqXf7vhhDs&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=26&ab_channel=DataTalksClub)
- [DE-Zoomcamp 3.1.3 - Best Pratices](https://www.youtube.com/watch?v=k81mLJVX08w&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=27&ab_channel=DataTalksClub)
