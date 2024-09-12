from database.DB_connect import DBConnect
from model.prodotto import Prodotto
from model.vendita import Vendita


class DAO():

    @staticmethod
    def get_all_vendite():
        cnx = DBConnect.get_connection()
        result = []

        cursor = cnx.cursor(dictionary=True)
        query = """select distinct gds.*
                    from go_sales.go_daily_sales gds """

        cursor.execute(query)

        for row in cursor:
            result.append(Vendita(**row))

        cursor.close()
        cnx.close()

        return result



    @staticmethod
    def get_all_prodotti():
        cnx = DBConnect.get_connection()
        result = []

        cursor = cnx.cursor(dictionary=True)
        query = """select distinct gp.*
                    from go_sales.go_products gp """

        cursor.execute(query)

        for row in cursor:
            result.append(Prodotto(row["Product_number"], row["Product_line"], row["Product_type"], row["Product"],row["Product_brand"], row["Product_color"], row["Unit_cost"], row["Unit_price"]))

        cursor.close()
        cnx.close()

        return result

    @staticmethod
    def get_vendite_stesso_gg(n1: Prodotto, n2: Prodotto, anno):
        cnx = DBConnect.get_connection()
        result = []

        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT COUNT(DISTINCT s1.Date) as N 
                   FROM go_daily_sales s1, go_daily_sales s2
                   WHERE s1.Date = s2.Date
                   AND s1.Retailer_code = s2.Retailer_code
                   AND s1.Product_Number = %s 
                   AND s2.Product_Number = %s
                   AND YEAR(s1.Date) = %s"""

        cursor.execute(query, (n1.Product_number, n2.Product_number, str(anno),))

        for row in cursor:
            result.append(row["N"])

        cursor.close()
        cnx.close()

        return result
