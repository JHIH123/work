from django.db import models

# Create your models here.

# 文字紀錄類別（資料庫）
class Place(models.Model):
    # 店名
    name = models.CharField(max_length=25, null=True)
    # 營業時間
    time = models.CharField(max_length=35, null=True)
    # 地址
    address = models.CharField(max_length=65, null=True)
    # 詳細網址
    url = models.CharField(max_length=100, null=True)
    # 電話
    phone = models.CharField(max_length=20, null=True)
    # 葷/素食
    food = models.CharField(max_length=10, null=True)
    # 資料記載時間
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.name

# 圖片紀錄類別
class Photo(models.Model):
    # 照片名稱
    name = models.CharField(max_length=255)
    # 照片我們會使用ImageField這個欄位，upload_to是表示檔案要儲存在哪個資料夾
    file = models.ImageField(upload_to='photos')
    # 外键，指向 Place 模型
    place = models.ForeignKey(Place, related_name='photos', help_text="The place that this photo come from.", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
