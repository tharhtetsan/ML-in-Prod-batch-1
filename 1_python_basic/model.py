import numpy as np

class Categories:
    def __init__(self,created_date,cat_id, cat_name):
        self.created_date = created_date
        self.id = cat_id
        self.name = cat_name



class Item:
    def __init__(self,created_date :str,item_id:str,name : str, qr_code : str,price:int,buying_price:int, category :Categories):
        self.created_date = created_date
        self.name = name
        self.id =  item_id
        self.qr_code=  qr_code
        self.price = price
        self.buying_price = buying_price
        self.category = category
        
    
    def getProfit(self):
        return int(self.price - self.buying_price)

    

class SaleItem:
    def __init__(self,customer_id :str,created_date :str,item: Item):
        self.item = item
        self.created_date = created_date
        self.customer_id = customer_id
    

    def getCategoryAndProfit(self):
    
        
        return self.item.category.name,self.item.name,self.item.getProfit()    
        

        


    
