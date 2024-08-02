from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, IntegerType, StructType
from pyspark.sql import functions as F

if __name__ == '__main__':
    spark = SparkSession.builder. \
        appName("movie").\
        master("local[*]"). \
        config("spark.sql.shuffle.partitions", 2).\
        getOrCreate()

    # sc = spark.sparkContext
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

    # 1.用户平均分
    df.groupBy("user_id").\
        avg("rank").\
        withColumnRenamed("avg(rank)", "avg_rank").\
        withColumn("avg_rank", F.round("avg_rank", 2)).\
        orderBy("avg_rank", ascending=False).\
        show()

    # 2.电影的平均分查询
    df.createTempView("movie")
    spark.sql("SELECT movie_id, ROUND(AVG(rank), 2) AS avg_rank FROM movie GROUP BY movie_id ORDER BY avg_rank DESC").show()

    # 3.查询大于平均分的电影的数量
    print("大于平均分的电影有：", df.where(df["rank"] > df.select(F.avg(df["rank"])).first()["avg(rank)"]).count())

    # 4.查询高分电影中（>3）打分次数最多的用户，以及此人打分的平均分
    # 先找出这个人
    user_id = df.where("rank > 3").\
        groupBy("user_id").\
        count().\
        withColumnRenamed("count", "cnt").\
        orderBy("cnt", ascending=False).\
        limit(1).\
        first()["user_id"]
    # 计算这个人的打分平均分
    df.filter(df["user_id"] == user_id).\
        select(F.round(F.avg("rank"), 2)).show()

    # 查询每个用户的平均打分， 最低打分， 最高打分
    df.groupBy("user_id").\
        agg(
          F.round(F.avg("rank"), 2).alias("avg_rank"),
          F.min("rank").alias("min_rank"),
          F.max("rank").alias("max_rank")
        ).show()

    # 查询评分超过100次的电影的平均分 排名 top10
    df.groupBy("movie_id").\
        agg(
          F.count("movie_id").alias("cnt"),
          F.round(F.avg("rank"), 2).alias("avg_rank")
        ).where("cnt > 100").\
        orderBy("avg_rank", ascending=False).\
        limit(10).\
        show()

"""
1. agg: 它是GroupedData对象的API, 作用是在里面可以写多个聚合
2. alias: 它是Column对象的API, 可以针对一个列进行改名
3. withColumnRenamed: 它是DataFrame的API, 可以对DF中的列进行改名， 一次改一个列， 改多个列可以链式调用
"""