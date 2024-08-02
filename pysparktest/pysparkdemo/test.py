from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, IntegerType, StructType
from pyspark.sql import functions as F
import pandas as pd
from operator import add

if __name__ == '__main__':
    # conf = SparkConf().setAppName("test").setMaster("local[*]")
    # sc = SparkContext(conf=conf)
    spark = SparkSession.builder. \
        appName("test"). \
        master("local[*]"). \
        getOrCreate()

    sc = spark.sparkContext

    rdd = sc.parallelize([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    print(rdd.getNumPartitions())
    result_rdd = rdd.map(lambda x: x * 10)
    print(result_rdd.collect())

    # SparkSQL的HelloWorld
    df = spark.read.csv("../data/input/scores.txt", sep=",", header=False)
    # 只传列名，类型靠推断， 是否为空时true
    df2 = df.toDF("id", "name", "score")

    df2.printSchema()
    df2.show()

    schema = StructType(). \
        add("id", StringType(), nullable=True). \
        add("name", StringType(), nullable=True). \
        add("score", IntegerType(), nullable=True)

    file_rdd = sc.textFile("../data/input/scores.txt"). \
        map(lambda x: x.split(",")). \
        map(lambda x: (x[0], x[1], int(x[2])))

    # 传入完整的Schema描述对象StructType
    df3 = file_rdd.toDF(schema=schema)
    df3.printSchema()
    df3.show()

    df2.createTempView("score")

    # SQL 风格
    spark.sql("""SELECT * FROM score WHERE name='语文' LIMIT 5""").show()

    # DSL风格
    df2.where("name='语文'").limit(5).show()

    # 基于Pandas的DataFrame构建SparkSQL的DataFrame对象
    pdf = pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["ZhangSan", "LiSi", "WangWu"],
        "age": [21, 22, 23]
    })

    # 将pandas的df对象转换成Spark的df
    df4 = spark.createDataFrame(pdf)
    df4.printSchema()
    df4.show()

    # 构建StructType, text数据源， 读取数据的特点是：将一整行只作为一个列读取，默认列名是value， 类型是String
    schema2 = StructType().add("data", StringType(), nullable=True)
    df4 = spark.read.format("text"). \
        schema(schema=schema2). \
        load("../data/input/scores.txt")

    df4.printSchema()
    df4.show()

    # 读取json数据源
    df5 = spark.read.format("json"). \
        load("../data/input/people.json")

    # JSON类型一般不用写schema, json自带有schema信息，列名和列类型（int/string）
    df5.printSchema()
    df5.show()

    # 读取csv数据源
    df6 = spark.read.format("csv"). \
        option("sep", ";"). \
        option("header", True). \
        option("encoding", "utf-8"). \
        schema("name STRING, age INT, job String"). \
        load("../data/input/people.csv")
    df6.printSchema()
    df6.show()

    # 读取parquet数据源, parquet自带schema， 直接load啥也不需要了
    df7 = spark.read.format("parquet").\
        load("../data/input/movie.parquet")
    df7.printSchema()
    df7.show()

    '''
    DataFrame支持两种风格进行编程
    DSL语法风格：领域特定语言，其实就是指DataFrame的特有API, DSL风格意思就是以调用API的方式来处理Data 比如：df.where().limit()
    SQL语法风格: 就是使用SQL语句处理DataFrame的数据。比如：spark.sql("SELECT * FROM XXX")
    '''
    df8 = spark.read.format("csv"). \
        schema("id INT, subject STRING, score INT"). \
        load("../data/input/scores.txt")
    # Column对象的获取
    id_column = df8["id"]
    subject_column = df8["subject"]
    # DSL风格
    df8.select(["id", "subject"]).show()
    df8.select("id", "subject").show()
    df8.select(id_column, subject_column).show()
    df8.select([id_column, subject_column]).show()

    # filter API
    df8.filter("score < 99").show()
    df8.filter(df8["score"] < 99).show()

    # where API
    df8.where("score < 99").show()
    df8.where(df8["score"] < 99).show()

    # groupBy API, df.groupBy 的返回值是GroupedData对象不是DataFrame, 它是一个有分组关系的数据结构，有一些API供我们对分组做聚合。
    # SQL: group by 后接上聚合; sum, avg, count, min, max
    # GroupedData类似于SQL分组后的数据结构， 同样有上述5种聚合方法。
    # GroupedData调用聚合方法后返回值依旧是DataFrame
    # GroupedData只是一个中转的对象，最终还是要获得DataFrame的结果
    df8.groupBy("subject").count().show()
    df8.groupBy(df8["subject"]).count().show()

    # SQL风格语法，注册DataFrame成为表
    df8.createTempView("scores")
    df8.createOrReplaceTempView("scores2")
    # 注册全局临时视图， 全局临时视图在使用的时候需要在前面加上global_temp. 前缀
    df8.createGlobalTempView("scores3")

    spark.sql("SELECT subject, COUNT(*) AS cnt FROM scores GROUP BY subject").show()
    spark.sql("SELECT subject, COUNT(*) AS cnt FROM scores2 GROUP BY subject").show()
    spark.sql("SELECT subject, COUNT(*) AS cnt FROM global_temp.scores3 GROUP BY subject").show()


