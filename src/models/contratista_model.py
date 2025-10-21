from database.db_manager import DBManager

class ContratistaModel:
    @staticmethod
    def get_all():
        db = DBManager()
        try:
            rows = db.fetch_all("SELECT id, codigo, nombre, empresa, telefono, estado FROM contratistas ORDER BY nombre")
            return rows
        finally:
            db.close()

    @staticmethod
    def get_by_code(codigo):
        db = DBManager()
        try:
            row = db.fetch_one("SELECT id, codigo, nombre, empresa, telefono, estado FROM contratistas WHERE codigo = ?", (codigo,))
            return row
        finally:
            db.close()

    @staticmethod
    def add(codigo, nombre, empresa, telefono, estado="Activo"):
        db = DBManager()
        try:
            db.execute_query(
                "INSERT INTO contratistas (codigo, nombre, empresa, telefono, estado) VALUES (?, ?, ?, ?, ?)",
                (codigo, nombre, empresa, telefono, estado)
            )
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            db.close()

    @staticmethod
    def update(id, nombre, empresa, telefono, estado):
        db = DBManager()
        try:
            db.execute_query(
                "UPDATE contratistas SET nombre=?, empresa=?, telefono=?, estado=? WHERE id=?",
                (nombre, empresa, telefono, estado, id)
            )
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            db.close()

    @staticmethod
    def delete(id):
        db = DBManager()
        try:
            db.execute_query("DELETE FROM contratistas WHERE id=?", (id,))
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            db.close()