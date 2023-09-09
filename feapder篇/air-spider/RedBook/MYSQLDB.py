from feapder.db.mysqldb import MysqlDB

##############################################################################
# SQL语句
# 创建笔记表
create_note_table_sql = '''
    CREATE TABLE IF NOT EXISTS note (
        note_id varchar(255) PRIMARY KEY,
        note_type varchar(255),
        display_title TEXT,
        note_cover TEXT,
        liked_count INTEGER,
        user_name varchar(255),
        user_id varchar(255),
        avatar TEXT
    )
'''
create_note_comment_table_sql = '''
    CREATE TABLE IF NOT EXISTS comment (
        comment_id varchar(255) PRIMARY KEY,
        note_id varchar(255),
        target_comment varchar(255),
        content TEXT,
        like_count varchar(100),
        user_name varchar(255),
        user_id varchar(255)
    )
'''
##############################################################################

if __name__ == '__main__':
    db = MysqlDB()
    # 创建note表
    # db.execute(create_note_table_sql)
    # 创建评论表
    db.execute(create_note_comment_table_sql)