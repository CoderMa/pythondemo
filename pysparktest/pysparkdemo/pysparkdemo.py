from pyspark import SparkConf, SparkContext
# import os

# os.environ["PYSPARK_PYTHON"] = "C:\\sers\\test\\.conda\\envs\\pyspark_env\\python.exe"

if __name__ == '__main__':
    conf = SparkConf().setAppName("PYSPARKDEMO").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    # file_rdd = sc.textFile("D:\\workspace\\pythonlearning\\venv\\data\\input\\words.txt")
    file_rdd = sc.textFile("../data/input/words.txt")

    words_rdd = file_rdd.flatMap(lambda line: line.split(" "))

    word_with_one_rdd = words_rdd.map(lambda word: (word, 1))

    result_rdd = word_with_one_rdd.reduceByKey(lambda a, b: a + b)

    print(result_rdd.collect())
