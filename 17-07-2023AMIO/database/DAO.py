from database.DB_connect import DBConnect
from model.prodotto import Prodotto


class DAO():


    @staticmethod
    def getAllBrands():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct gp.Product_brand 
                    from go_products gp 
                    order by gp.Product_brand  asc"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row["Product_brand"])

        cursor.close()
        cnx.close()
        return res



    @staticmethod
    def getNodes(brand):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select gp.*
                    from go_products gp 
                    where gp.Product_brand = %s"""
        cursor.execute(query, (brand,))

        res = []
        for row in cursor:
            res.append(Prodotto(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getEdges(anno,brand,mapP):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select ds1.Product_number as id1, ds2.Product_number as id2 
                    from go_daily_sales ds1, go_daily_sales ds2, go_products p, go_products p2
                    where ds1.Product_number<ds2.Product_number 
                    and year(ds2.`Date`) =%s  and  year(ds2.`Date`)= year(ds1.`Date`)
                    and ds2.Retailer_code = ds1.Retailer_code
                    and ds2.`Date`= ds1.`Date`
                    and p.Product_brand = %s and p2.Product_brand =  p.Product_brand
                    and p.Product_number =  ds1.Product_number and p2.Product_number =  ds2.Product_number
                    group by ds1.Product_number, ds2.Product_number"""
        cursor.execute(query, (anno, brand))

        res = []
        for row in cursor:
                res.append((mapP[row["id1"]],mapP[row["id2"]]))

        cursor.close()
        cnx.close()
        return res



    @staticmethod
    def getPeso1(y,n1,n2,mapP):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select ds1.Product_number as id1, ds2.Product_number as id2, count(distinct ds2.Retailer_code) as weight
                    from go_daily_sales ds1, go_daily_sales ds2
                    where ds1.Product_number=%s and ds2.Product_number= %s
                    and ds2.Retailer_code = ds1.Retailer_code
                    and year(ds2.`Date`) =%s  and  year(ds2.`Date`)= year(ds1.`Date`)
                    and ds2.`Date`= ds1.`Date`
                    group by  ds1.Product_number, ds2.Product_number"""
        cursor.execute(query, (n1.Product_number,n2.Product_number,y))

        res = []
        for row in cursor:
            #if row["id1"] in mapP.keys() and row["id2"] in mapP.keys():
            res.append((n1,n2, row["weight"]))

        cursor.close()
        cnx.close()
        return res



    @staticmethod
    def getEdges_con_peso(y,brand,mapP): #altro
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select ds1.Product_number as id1, ds2.Product_number as id2, ds2.Retailer_code, ds2.`Date`, count(distinct ds2.Retailer_code) as weight
                    from go_daily_sales ds1, go_daily_sales ds2, go_products p, go_products p2
                    where ds1.Product_number<ds2.Product_number 
                    and year(ds2.`Date`) =%s  and  year(ds2.`Date`)= year(ds1.`Date`)
                    and ds2.Retailer_code = ds1.Retailer_code
                    and ds2.`Date`= ds1.`Date`
                    and p.Product_brand = %s and p2.Product_brand =  p.Product_brand
                    and p.Product_number =  ds1.Product_number and p2.Product_number =  ds2.Product_number
                    group by ds1.Product_number, ds2.Product_number"""
        cursor.execute(query, (y, brand))

        res = []
        for row in cursor:
            #if row["id1"] in mapP.keys() and row["id2"] in mapP.keys():
            res.append((mapP[row["id1"]],mapP[row["id2"]], row["weight"]))

        cursor.close()
        cnx.close()
        return res

