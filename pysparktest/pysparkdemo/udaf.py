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

    rdd = sc.parallelize([1, 2, 3, 4, 5, 6], 3)
    df = rdd.map(lambda x: [x]).toDF(["num"])

    # 折中方式是使用RDD的mapPartitions算子来完成聚合操作
    # 如果使用mapPartitons API 完成UDAF聚合，一定要单分区
    single_partition_rdd = df.rdd.repartition(1)

    def process(item):
        sum = 0
        for row in item:
            sum += row['num']

        return [sum]  # 一定要嵌套list, 因为mapPartitions方法要求的返回值是List对象


    print(single_partition_rdd.mapPartitions(process).collect())











