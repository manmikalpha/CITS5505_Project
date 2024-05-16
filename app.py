# # app.py
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# import os




# # from flask import Flask

# # app = Flask(__name__)

# # @app.route('/')
# # def hello_world():
# #     return 'Hello, World!'

# # if __name__ == '__main__':
# #     app.run()




# app = Flask(__name__)

# # with app.app_context():
# #     # 你可以在這裡進行你的操作，比如數據庫查詢、操作 session 等
# #     # 這裡的代碼將在應用的上下文中執行
# #     # 例如:
# #     print("We are inside the application context.")


# # 設置數據庫 URI
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
# # 繼續編輯 app.py
# class Image(db.Model):
#     __tablename__ = 'images'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     data = db.Column(db.LargeBinary, nullable=False)

# # 創建數據庫表
# with app.app_context():
#     db.create_all()

# # 繼續編輯 app.py
# def insert_image(image_path, image_name):
#     with open(image_path, 'rb') as file:
#         blob_data = file.read()
#     image = Image(name=image_name, data=blob_data)
#     db.session.add(image)
#     db.session.commit()

# # 繼續編輯 app.py
# def bulk_insert_images(directory_path):
#     # 獲取目錄中所有文件的列表
#     files = os.listdir(directory_path)
    
#     # 計數器，確保只上傳 16 張圖片
#     count = 0
    
#     for file_name in files:
#         # 構建文件完整路徑
#         file_path = os.path.join(directory_path, file_name)
        
#         # 檢查文件是否為圖片
#         if os.path.isfile(file_path) and file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
#             # 插入圖片到資料庫
#             insert_image(file_path, file_name)
#             count += 1
            
#             # 如果已經插入了 16 張圖片，停止插入
#             if count >= 16:
#                 break

# # 設定目錄路徑
# # directory_path = './group_project/ruth_5505/images'
# directory_path = '../images'

# @app.route('/some_route')
# def some_view_function():
#     directory_path = '../images'
#     with app.app_context():
#         bulk_insert_images(directory_path)
#     return 'Images Inserted'


# # 執行批量插入
# bulk_insert_images(directory_path)
# @app.route('/')
# def index():
#     # return 'ssssssssssssssssssss'
#     images = Image.query.all()
#     return f'{len(images)} images uploaded.'

# # def hello_world():
# #     return 'Hello, World!'

# if __name__ == '__main__':
#     app.run(debug=True)




from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# 设置数据库 URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 定义 Image 模型
class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)

# 创建数据库表
with app.app_context():
    db.create_all()

def insert_image(image_path, image_name):
    with open(image_path, 'rb') as file:
        blob_data = file.read()
    image = Image(name=image_name, data=blob_data)
    db.session.add(image)
    db.session.commit()

def bulk_insert_images(directory_path):
    files = os.listdir(directory_path)
    count = 0
    for file_name in files:
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path) and file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            insert_image(file_path, file_name)
            count += 1
            if count >= 16:
                break

@app.route('/upload_images')
def upload_images():
    directory_path = '../images'
    bulk_insert_images(directory_path)
    return 'Images Inserted'

@app.route('/')
def index():
    images = Image.query.all()
    return f'{len(images)} images uploaded.'

if __name__ == '__main__':
    app.run(debug=True)
