from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, IntegerType, StructType
from pyspark.sql import functions as F

if __name__ == '__main__':
    spark = SparkSession.builder.\
        appName("movie").\
        master("local[*]").\
        config("spark.sql.shuffle.partitions", 2).\
        getOrCreate()

    sc = spark.sparkContext

    schema = StructType().add("user_id", StringType(), nullable=True).\
        add("movie_id", IntegerType(), nullable=True).\
        add("rank", IntegerType(), nullable=True).\
        add("ts", StringType(), nullable=True)

    df = spark.read.format("csv"). \
        option("sep", "\t"). \
        option("header", False). \
        option("encoding", "utf-8"). \
        schema(schema=schema). \
        load("../data/input/u.data")

    # Write into mysql db
    df.write.mode("overwrite").\
        format("jdbc").\
        option("url", "jdbc:mysql://192.168.146.128:3306/bigdata?useSSL=false&useUnicode=true").\
        option("dbtable", "movie_data").\
        option("user", "root").\
        option("password", "root123").\
        save()
    # Read from mysql db
    # df2 = spark.read.format("jdbc"). \
    #     option("url", "jdbc:mysql://localhost:3306/bigdata?useSSL=false&useUnicode=true"). \
    #     option("dbtable", "movie_data"). \
    #     option("user", "root"). \
    #     option("password", "root123").\
    #     load()
    # df2.printSchema()
    # df2.show()




