from typing import List


class FDataBase:
    """Класс с методами для работы с тремя таблицами, person, position и departments"""

    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor()

    def getPosition(self) -> List:
        """Получить список всех должностей"""
        try:
            self.__cursor.execute("SELECT * FROM position")
            res = self.__cursor.fetchall()
            if res:
                return res
        except:
            print('ОШИБОЧКА')
        return []

    def getPersons(self) -> List:
        """Получить список всех сотрудников"""
        try:
            self.__cursor.execute("SELECT * FROM person")
            res = self.__cursor.fetchall()
            if res:
                return res
        except:
            print('Ошибочка!')
        return []

    def addPerson(self, username: str, dep_id: int, pos_id: int) -> bool:
        """Метод для добавления сотрудника в базу данных"""
        try:
            self.__cursor.execute("INSERT INTO person  VALUES (NULL, ?, ?, ?)", (username, dep_id, pos_id))
            self.__db.commit()
            return True
        except:
            print("Ошибочка")
        return False

    def getPerson(self, user) -> List:
        """Выбрать сотрудника из базы данных"""
        try:
            self.__cursor.execute(f"SELECT * FROM person WHERE name = '{user}'")
            res = self.__cursor.fetchone()
            if res:
                return res
        except:
            print("Ошибка")
        return []

    def getDepartments(self) -> List:
        """Получить список всех отделов"""
        try:
            self.__cursor.execute("SELECT * FROM depart")
            res = self.__cursor.fetchall()
            if res:
                return res
        except:
            print('Ошибка')
        return []

    def getDepartment(self, dep_id: int) -> List:
        """Получить название отдела по id_par отдела"""
        try:
            self.__cursor.execute(f"SELECT * FROM depart WHERE id = {dep_id}")
            res = self.__cursor.fetchone()
            if res:
                return res
        except:
            print('Ошибка')
        return []

    def getDepartmentChild(self, dep_id: int) -> List:
        """Получить название отделов детей по id родителя"""
        try:
            self.__cursor.execute(f"SELECT * FROM depart WHERE parent = {dep_id}")
            res = self.__cursor.fetchall()
            if res:
                return res
        except:
            print('Ошибка')
        return []

    def addDepartment(self, title: str, par_id: int) -> None:
        """Метод для добавления отдела в базу данных"""
        try:
            self.__cursor.execute("INSERT INTO depart VALUES (NULL, ?, ?)", (title, par_id))
            self.__db.commit()
        except:
            print('Ошибка')

    def getPersonPosition(self, pos_id: int) -> str:
        """Получить название должности из таблицы position по id"""
        try:
            self.__cursor.execute(f"SELECT * FROM position WHERE position.id = {pos_id} LIMIT 1")
            res = self.__cursor.fetchall()
            if res:
                return res
        except:
            print("ОШибка")

    def getPersonDepartments(self, dep_id: int) -> str:
        """Получить название отдела из таблицы depart"""
        try:
            self.__cursor.execute(f"SELECT * FROM depart WHERE depart.id = {dep_id} LIMIT 1")
            res = self.__cursor.fetchall()
            if res:
                return res
        except:
            print("ОШибка")

    def getDepartmentId(self, dep_title: str) -> str:
        """Получить id отдела по имени"""
        try:
            self.__cursor.execute(f"SELECT * FROM depart WHERE depart.title = '{dep_title}'")
            res = self.__cursor.fetchone()
            if res:
                return res
        except:
            print("ОШибка")

    def updatePerson(self, pk: int, username: str, pos: int, dep: int) -> None:
        """Метод обновения данных сотрудника"""
        try:
            sql = f"UPDATE person SET name = '{username}', department_id = {dep}, position_id = {pos} WHERE id = {pk}"
            self.__cursor.execute(sql)
            self.__db.commit()
        except:
            print("Ошибка!")

    def deletePerson(self, username) -> None:
        """Метод для удаления сотрудника"""
        try:
            self.__cursor.execute(f"DELETE FROM person WHERE name = '{username}'")
            self.__db.commit()
        except:
            print("Ошибка при удалении")

    def getPersonsFromDepartments(self, dep_id: int) -> List:
        try:
            self.__cursor.execute(f'SELECT * FROM person WHERE department_id = {dep_id}')
            res = self.__cursor.fetchall()
            if res:
                return res
        except:
            print('Ошибка')
        return []

    def updateDepartment(self, pk: int, dep_title: str, par_id: int) -> None:
        """Метод обновения данных отдела"""
        try:
            sql = f"UPDATE depart SET title = '{dep_title}', parent = {par_id} WHERE id = {pk}"
            self.__cursor.execute(sql)
            self.__db.commit()
        except:
            print("Ошибка!")