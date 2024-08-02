import string
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

    rdd = sc.parallelize([[1], [2], [3]])
    df = rdd.toDF(["num"])
    df.printSchema()

    # 注册UDF执行函数定义
    def split_process(num):
        return {"number": num, "letter": string.ascii_letters[num]}

    struct_type = StructType().add("number", IntegerType(), nullable=True). \
        add("letter", StringType(), nullable=True)

    # 方式1构建UDF
    udf2 = spark.udf.register("udf1", split_process, struct_type)
    # SQL风格
    df.selectExpr("udf1(num)").show()
    # DSL风格
    df.select(udf2(df["num"])).show()

    # 方式2构建UDF
    udf3 = F.udf(split_process, struct_type)
    df.select(udf3(df["num"])).show(truncate=False)










