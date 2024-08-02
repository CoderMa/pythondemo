from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, IntegerType, ArrayType, StructType
from pyspark.sql import functions as F

if __name__ == '__main__':
    spark = SparkSession.builder.\
        appName("movie").\
        master("local[*]").\
        config("spark.sql.shuffle.partitions", 2).\
        getOrCreate()

    sc = spark.sparkContext

    rdd = sc.parallelize([["hadoop spark flink"], ["hadoop flink java"]])
    df = rdd.toDF(["line"])
    df.printSchema()

    # 注册UDF执行函数定义
    def split_line(data):
        return data.split(" ")

    # 方式1构建UDF
    udf2 = spark.udf.register("udf1", split_line, ArrayType(StringType()))
    # SQL风格
    df.createTempView("lines")
    spark.sql("SELECT udf1(line) FROM lines").show(truncate=False)

    # DSL风格
    df.select(udf2(df["line"])).show()

    # 方式2构建UDF
    udf3 = F.udf(split_line, ArrayType(StringType()))
    df.select(udf3(df["line"])).show(truncate=False)










