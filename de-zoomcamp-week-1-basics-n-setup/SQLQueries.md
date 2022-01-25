
## Question 3: Count records *
### How many taxi trips were there on January 15?

SELECT 
    CAST(tpep_pickup_datetime as DATE), 
    COUNT(1)

FROM 
    ny_taxi_data

WHERE 
    CAST(tpep_pickup_datetime as DATE) = '2021-01-15' 

GROUP BY 
    CAST(tpep_pickup_datetime as DATE)


## Question 4: Largest tip for each day *
### On which day it was the largest tip in January? (note: it's not a typo, it's "tip", not "trip")

SELECT 
	CAST(tpep_pickup_datetime AS date), 
	COUNT(1), 
	MAX(tip_amount)

FROM 
	ny_taxi_data

GROUP BY 
	CAST(tpep_pickup_datetime AS date)

ORDER BY 
	MAX(tip_amount) DESC


## Question 5: Most popular destination *
### What was the most popular destination for passengers picked up in central park on January 14? Enter the zone name (not id). If the zone name is unknown (missing), write "Unknown"

SELECT
	COUNT(ntd."DOLocationID") AS dropoff_location_count,
	zdo."Zone"

FROM
	ny_taxi_data ntd,
	zones zpu,
	zones zdo

WHERE
	"PULocationID" = 43 AND 
	CAST(tpep_pickup_datetime AS DATE) = '2021-01-14' AND
	ntd."PULocationID" = zpu."LocationID" AND
	ntd."DOLocationID" = zdo."LocationID"

GROUP BY 
	zdo."Zone"

ORDER BY
	dropoff_location_count DESC

LIMIT(10)

## Question 6: Most expensive route *
### What's the pickup-dropoff pair with the largest average price for a ride (calculated based on total_amount)? Enter two zone names separated by a slashFor example:"Jamaica Bay / Clinton East"If any of the zone names are unknown (missing), write "Unknown". For example, "Unknown / Clinton East".

SELECT
	AVG(ntd."total_amount") AS avg_pricing,
	CONCAT(zpu."Zone", ' / ', zdo."Zone") AS route

FROM
	ny_taxi_data ntd LEFT JOIN 
	zones zpu ON 
	ntd."PULocationID" = zpu."LocationID" LEFT JOIN
	zones zdo ON 
	ntd."DOLocationID" = zdo."LocationID"

GROUP BY
	route

ORDER BY
	avg_pricing DESC

LIMIT(10)
