from database.DB_connect import DBConnect
from model.airport import Airport
from model.arco import Arco


class DAO():

    @staticmethod
    def getAllNodes(nMin,idMapAirports):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        #conto prima il numero di voli che fa una compagnia
        #e da quello poi conto quante compagnie partono da quell'areoporto
        #a noi servono solo quelli con + di 5 compagnie(having)
        query = """SELECT t.ID, COUNT(*) AS N
FROM (
    SELECT a.ID, f.AIRLINE_ID
    FROM airports a, flights f
    WHERE a.ID = f.ORIGIN_AIRPORT_ID OR a.ID = f.DESTINATION_AIRPORT_ID
    GROUP BY a.ID, f.AIRLINE_ID
) t
GROUP BY t.ID
HAVING N >= 5
ORDER BY N ASC

        """

        cursor.execute(query,(nMin,))

        for row in cursor:#ci serve s
            result.append(idMapAirports[row["ID"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from airports a order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(idMapAirports):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        # conto prima il numero di voli che fa una compagnia
        # e da quello poi conto quante compagnie partono da quell'areoporto
        # a noi servono solo quelli con + di 5 compagnie(having)
        query = """select f.ORIGIN_AIRPORT_ID as aP, f.DESTINATION_AIRPORT_ID as aD, count(*) as Peso
from flights f
group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID
order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID
        """

        cursor.execute(query)

        for row in cursor:  # ci serve s
            result.append(Arco(idMapAirports[row["aP"]],idMapAirports[row["aD"]], row["Peso"] ))

        cursor.close()
        conn.close()
        return result
