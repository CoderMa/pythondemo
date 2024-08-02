from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, IntegerType, StructType
from pyspark.sql import functions as F

if __name__ == '__main__':
    spark = SparkSession.builder. \
        appName("wordcount").\
        master("local[*]"). \
        getOrCreate()

    sc = spark.sparkContext
    # SQL风格
    rdd = sc.textFile("../data/input/words.txt"). \
        flatMap(lambda x: x.split(" ")). \
        map(lambda x: [x])
    df = rdd.toDF(["word"])
    # 注册df为表格
    df.createTempView("words")
    spark.sql("SELECT word, COUNT(*) AS cnt FROM words GROUP BY word ORDER BY cnt DESC").show()

    # DSL风格
    df = spark.read.format("text").load("../data/input/words.txt")
    # withColumn方法，对已经存在的列进行操作，返回一个新的列，如果名字和老列相同那么替换，否则作为新列存在
    # df2 = df.withColumn("value", F.explode(F.split(df["value"], " "))).show()
    df2 = df.withColumn("value", F.explode(F.split(df["value"], " ")))
    df2.groupBy("value").\
        count().\
        withColumnRenamed("value", "word").\
        withColumnRenamed("count", "cnt").\
        orderBy("cnt", ascending=False).\
        show()
