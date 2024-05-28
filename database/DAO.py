from database.DB_connect import DBConnect
from model.DailySale import DailySale
from model.Product import Product
class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllSales():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from go_daily_sales gds  """

        cursor.execute(query)

        for row in cursor:
            result.append(DailySale(row["Retailer_code"], row["Product_number"], row["Order_method_code"], row["Date"], row["Quantity"], row["Unit_price"], row["Unit_sale_price"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllProducts():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from go_products"""

        cursor.execute(query)

        for row in cursor:
            result.append(Product(row["Product_number"], row["Product_line"], row["Product_type"], row["Product"],row["Product_brand"], row["Product_color"], row["Unit_cost"], row["Unit_price"]))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getSameDaySales(p1, p2, a):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = '''SELECT COUNT(DISTINCT s1.Date) as N 
                   FROM go_daily_sales s1, go_daily_sales s2
                   WHERE s1.Date = s2.Date
                   AND s1.Retailer_code = s2.Retailer_code
                   AND s1.Product_Number = %s 
                   AND s2.Product_Number = %s
                   AND YEAR(s1.Date) = %s'''
        cursor.execute(query, (p1.Product_number, p2.Product_number, str(a)))

        for row in cursor:
            result.append(row["N"])

        cursor.close()
        conn.close()
        return result
