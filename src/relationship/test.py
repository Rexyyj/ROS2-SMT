from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

df1 = spark.read.load(  "./edges.csv",\
                        format = "csv",\
                        header = True,\
                        inferSchema = True,
                        sep = ' ')
df1.show()