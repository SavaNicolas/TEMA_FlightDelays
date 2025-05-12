from database.DB_connect import DBConnect
from model.airport import Airport


class DAO():

    @staticmethod
    def getAllNodes(nMin,idMapAirports):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        #conto prima il numero di voli che fa una compagnia
        #e da quello poi conto quante compagnie partono da quell'areoporto
        #a noi servono solo quelli con + di 5 compagnie(having)
        query = """SELECT t.ID, t.IATA_CODE, COUNT(*) AS N
FROM (
    SELECT a.ID, a.IATA_CODE, f.AIRLINE_ID, COUNT(*)
    FROM airports a, flights f
    WHERE a.ID = f.ORIGIN_AIRPORT_ID OR a.ID = f.DESTINATION_AIRPORT_ID
    GROUP BY a.ID, a.IATA_CODE, f.AIRLINE_ID
) t
GROUP BY t.ID, t.IATA_CODE
HAVING N >= %s
ORDER BY N ASC;

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