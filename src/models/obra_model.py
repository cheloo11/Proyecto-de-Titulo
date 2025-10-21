from database.db_manager import DBManager

class ObraModel:
    """Modelo para acceso a datos de obras"""
    
    @staticmethod
    def get_all_obras():
        """Obtiene todas las obras de la base de datos"""
        db = DBManager()
        try:
            query = """
            SELECT id, nombre, codigo, direccion, fecha_inicio, fecha_fin, jefe_responsable, estado
            FROM obras
            ORDER BY nombre
            """
            obras = db.fetch_all(query)
            return obras
        except Exception as e:
            print(f"Error al obtener obras: {str(e)}")
            return []
        finally:
            db.close()
    
    @staticmethod
    def get_obra_by_code(code):
        """Busca una obra por su código"""
        db = DBManager()
        try:
            query = """
            SELECT id, nombre, codigo, direccion, fecha_inicio, fecha_fin, jefe_responsable, estado
            FROM obras
            WHERE codigo = ?
            """
            obra = db.fetch_one(query, (code,))
            return obra
        except Exception as e:
            print(f"Error al buscar obra por código: {str(e)}")
            return None
        finally:
            db.close()
    
    @staticmethod
    def add_obra(nombre, codigo, direccion, fecha_inicio, fecha_fin, jefe_responsable, estado="activa"):
        """Agrega una nueva obra a la base de datos"""
        db = DBManager()
        try:
            query = """
            INSERT INTO obras (nombre, codigo, direccion, fecha_inicio, fecha_fin, jefe_responsable, estado)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            db.execute_query(query, (nombre, codigo, direccion, fecha_inicio, fecha_fin, jefe_responsable, estado))
            return True
        except Exception as e:
            print(f"Error al agregar obra: {str(e)}")
            return False
        finally:
            db.close()
    
    @staticmethod
    def update_obra(id, nombre, direccion, fecha_inicio, fecha_fin, jefe_responsable, estado):
        """Actualiza una obra existente"""
        db = DBManager()
        try:
            query = """
            UPDATE obras 
            SET nombre = ?, direccion = ?, fecha_inicio = ?, fecha_fin = ?, jefe_responsable = ?, estado = ?
            WHERE id = ?
            """
            db.execute_query(query, (nombre, direccion, fecha_inicio, fecha_fin, jefe_responsable, estado, id))
            return True
        except Exception as e:
            print(f"Error al actualizar obra: {str(e)}")
            return False
        finally:
            db.close()
    
    @staticmethod
    def delete_obra(id):
        """Elimina una obra por su ID"""
        db = DBManager()
        try:
            query = "DELETE FROM obras WHERE id = ?"
            db.execute_query(query, (id,))
            return True
        except Exception as e:
            print(f"Error al eliminar obra: {str(e)}")
            return False
        finally:
            db.close()