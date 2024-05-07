from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
import json
import mysql.connector



mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="vedang1234",
  database="Ecommerceplatform"
)

app = Flask(__name__)
api = Api(app)

def format(cursor):
    rows = cursor.fetchall()
    result = []
    for row in rows:
        d = {}
        for i, col in enumerate(cursor.description):
            d[col[0]] = row[i]
            result.append(d)
    json_result = json.dumps(result)
    return json_result

class Product(Resource):
    def get(self):
        print("In Product get: ")
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM Product")
        return format(mycursor)
    
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('productName', type=str)
        parser.add_argument('price', type=int)
        args = parser.parse_args()
        print(args)
        productName = args['productName']
        price = args['price']


        sql = "INSERT INTO Product(product_name, price) VALUES (%s, %s)"
        val = (productName,price)
        mycursor = mydb.cursor() 
        mycursor.execute(sql, val)
        mydb.commit()
        return format(mycursor)
    
    
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('productName', type=str)
        parser.add_argument('price', type=int)
        parser.add_argument('productID', type = int)
        args = parser.parse_args()
        print(args)
        productName = args['productName']
        price = args['price']
        productID = args['productID']

        mycursor = mydb.cursor()
        sql = "UPDATE Product SET product_name = %s, price = %s WHERE product_id = %s"
        val = (productName,price,productID)
        mycursor = mydb.cursor() 
        mycursor.execute(sql, val)
        mydb.commit()
        return format(mycursor)
    

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('productID', type=int)
        args = parser.parse_args()
        productID = args['productID']

        mycursor = mydb.cursor()
        sql = "DELETE FROM Product WHERE product_id = %s"
        val = (productID,)
        mycursor.execute(sql, val)
        mydb.commit()
        return format(mycursor)


class orders(Resource):
    def get(self):
        print("In orders get: ")
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM orders")
        return format(mycursor)
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('product_id', type=int)
        args = parser.parse_args()
        product_id = args['product_id']
        mycursor = mydb.cursor
        sql = "INSERT INTO orders (product_id) VALUES (%s)"
        val = (product_id,)
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        myresult = mycursor.fetchone()
        mydb.commit()
        print(myresult)
        return{'hello':'world'}
    
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('order_id', type=int)
        parser.add_argument('product_id', type=int)
        args = parser.parse_args()
        print(args)
        order_id = args['order_id']
        product_id = args['product_id']

        mycursor = mydb.cursor()
        sql = "UPDATE orders SET product_id = %s WHERE order_id = %s"
        val = (product_id,order_id)
        mycursor = mydb.cursor() 
        mycursor.execute(sql, val)
        myresult = mycursor.fetchone()
        mydb.commit()
        return format(mycursor)
    
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('order_id', type = int)
        args = parser.parse_args()
        print(args)
        order_id = args['order_id']

        mycursor = mydb.cursor()
        sql = "DELETE FROM orders WHERE order_id = %s"
        val = (order_id,)
        mycursor = mydb.cursor() 
        mycursor.execute(sql,val)
        mydb.commit()
        return format(mycursor)


class ProductList(Resource):
    def get(self,productID):
        print("In products get: ")
        mycursor = mydb.cursor()
        sql = "SELECT * FROM Product where product_id = %s"
        val = (productID,)
        mycursor.execute(sql,val)
        return format(mycursor)
    
class OrderList(Resource):
    def get(self,orderID):
        print("Orders are: ")
        mycursor = mydb.cursor()
        sql = "SELECT * FROM Product where product_id = %s"
        return format(mycursor)

api.add_resource(Product, '/products')
api.add_resource(orders, '/Order')
api.add_resource(ProductList, '/ProductList/<int:productID>')
api.add_resource(OrderList, '/OrderList/<int:orderID>')


if __name__ == '__main__':
    app.run(debug=True)






