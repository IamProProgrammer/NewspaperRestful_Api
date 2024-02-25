import sqlite3
from newspaper import Article
import  newspaper

def get_all(query):
    conn = sqlite3.connect("data/newsdb")
    #Lấy dữ liệu lên
    data = conn.execute(query).fetchall()

    conn.close()

    return data

def get_news_by_id (news_id):
    conn = sqlite3.connect("data/newsdb")
    sql = '''
    SELECT N.subject, N.description, N.image, N.original_url, C.name, C.url
    FROM news N INNER JOIN category C ON N.category_id=C.id 
    WHERE N.id=?
    '''
    news = conn.execute(sql, (news_id)).fetchall()
    conn.close()

    return  news

def add_comment(news_id, content):
    conn = sqlite3.connect('data/newsdb')
    sql = '''
        INSERT INTO comment(content, news_id) VALUES (?,?)
    '''
    conn.execute(sql, (content, news_id))
    conn.commit()
    conn.close()

def add_news(conn, url, category_id):
    sql = '''
    INSERT INTO news (subject, description, image, original_url, category_id)
    VALUES (?, ?, ?, ?, ?)
    '''

    article = Article(url)
    article.download() #Phương thức này tải nội dung của bài viết từ đường link đã cung cấp. Nó lấy nội dung HTML trang web để sau này có thể được phân tích
    article.parse() #Phương thức này phân tích nội dung đã tải về của bài viết. Trích xuất các thông tin như tiêu đề, tác giả, ngày xuất bản và nội dung chính của bài viết từ mã HTML

    conn.execute(sql, (article.title, article.text, article.top_img, article.url, category_id))
    conn.commit()

def get_news_url():
    cats = get_all("SELECT * FROM category")
    conn = sqlite3.connect("data/newsdb")
    for cat in cats:
        cat_id = cat[0]
        url = cat[2]
        cat_paper = newspaper.build(url)
        for article in cat_paper.articles:
            try:
                print("===", article.url)
                add_news(conn, article.url, cat_id)
            except Exception as ex:
                print("ERROR: " + str(ex))
                pass
    conn.close()

if __name__ == "__main__":
    get_news_url()