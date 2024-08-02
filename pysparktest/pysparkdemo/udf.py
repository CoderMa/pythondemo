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
    rdd = sc.parallelize([1, 2, 3, 4, 5, 6, 7]).map(lambda x: [x])
    df = rdd.toDF(["num"])
    df.printSchema()

    def num_ride_10(data):
        return data * 10
    # 参数1： 注册的UDF的名称，这个udf名称仅可以用于SQL风格
    # 返回值对象： 这是一个UDF对象，仅可以用于DSL风格
    # 当前这种方式定义的UDF，可以通过参数1的名称用于SQL风格， 通过返回值对象用于DSL风格
    udf2 = spark.udf.register("udf1", num_ride_10, IntegerType())

    # SQL风格使用
    # selectExpr 以SELECT的表达式执行， 表达式SQL风格的表达式（字符串）
    # select方法，接受普通的字符串字段名，或者返回值是Column对象的计算
    df.selectExpr("udf1(num)").show()

    # DSL 风格使用
    # 返回值UDF对象如果作为方法使用， 传入的参数一定是Column对象
    df.select(udf2(df['num'])).show()

    # 方式2注册,仅能用于DSL风格
    udf3 = F.udf(num_ride_10, IntegerType())
    df.select(udf3(df["num"])).show()








