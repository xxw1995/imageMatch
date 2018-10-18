## 自建图像检索引擎

-   可选的检索方法
    -  颜色直方图(效果较差):采用annoy算法加速向量比较过程
    -  pHash(快)
-   特征提取&读入DB脚本

<br>

## Usage:
-    在当前文件夹下创建一个mysql_config.py的文件, 其中应包含
    
    DB_name="XXXX"
    DB_addr="XXXX"
    DB_user="XXXX"
    DB_passwod="XXXX"
-   使用readData.py 进行数据库的构建操作
-   (服务器上)使用match.py 进行查询，输入当前文件夹下的文件名，本地读取，提取特征，由服务器进行检索，最终返回服务器数据库中最匹配的MATCH_ITEM_NUM条数据(config.py)



***
NOTE: 这个图像检索是多媒体的作业，我在颜色直方图基础上，为了提高效率和精度将他进行了扩充, 添加了pHash的检索和聚类优化，
形成了这样的一个简单的检索方案