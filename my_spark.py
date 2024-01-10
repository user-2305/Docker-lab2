from pyspark.sql import SparkSession
from pyspark.sql.functions import mean, round

spark = SparkSession.builder.master('spark://spark-master:7077').appName("HousePrice").getOrCreate()

db_url = "jdbc:postgresql://db:5432/mydb"
con_props = {
    "user": "myuser",
    "password": "mypassword",
    "driver": "org.postgresql.Driver"
}

df = spark.read.jdbc(url=db_url, table="houseprices", properties=con_props)

query_result = df.filter(df["property_type"].isin('House', 'Flat')). \
    groupBy('city', 'location', 'bedrooms').agg(round(mean("price"), 2).alias("AVG Price")). \
    orderBy(["city", "location", "bedrooms","AVG Price"], ascending=[False, False, False, True])

query_result.show()

spark.stop()