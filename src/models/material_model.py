from database.db_manager import DBManager

class MaterialModel:
    """
    Modelo para acceso a datos de materiales.
    Este es el ÚNICO archivo que debe importar DBManager y usar SQL.
    """
    
    @staticmethod
    def get_all_materials():
        """Obtiene todos los materiales de la base de datos"""
        db = DBManager()
        try:
            query = """
            SELECT id, nombre, descripcion, codigo_barra, cantidad, unidad_medida, monto_unitario, stock_minimo, estado
            FROM materiales
            ORDER BY nombre
            """
            return db.fetch_all(query)
        except Exception as e:
            print(f"Error en Modelo al obtener materiales: {str(e)}")
            return []
        finally:
            db.close()
    
    @staticmethod
    def get_material_by_code(code):
        """Busca un material por su código de barras"""
        db = DBManager()
        try:
            query = """
            SELECT id, nombre, descripcion, codigo_barra, cantidad, unidad_medida, monto_unitario, stock_minimo, estado
            FROM materiales
            WHERE codigo_barra = ?
            """
            return db.fetch_one(query, (code,))
        except Exception as e:
            print(f"Error en Modelo al buscar por código: {str(e)}")
            return None
        finally:
            db.close()

    @staticmethod
    def get_by_id(material_id):
        """Obtiene un material por su ID"""
        db = DBManager()
        try:
            query = """
            SELECT id, nombre, descripcion, codigo_barra, cantidad, unidad_medida, monto_unitario, stock_minimo, estado
            FROM materiales
            WHERE id = ?
            """
            return db.fetch_one(query, (material_id,))
        except Exception as e:
            print(f"Error en Modelo al obtener por id: {str(e)}")
            return None
        finally:
            db.close()

    @staticmethod
    def add_material(nombre, descripcion, codigo_barra, cantidad, unidad_medida, monto_unitario, stock_minimo, estado):
        """Agrega un nuevo material a la base de datos"""
        db = DBManager()
        try:
            query = """
            INSERT INTO materiales (nombre, descripcion, codigo_barra, cantidad, unidad_medida, monto_unitario, stock_minimo, estado)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            db.execute_query(query, (nombre, descripcion, codigo_barra, cantidad, unidad_medida, monto_unitario, stock_minimo, estado))
            return True
        except Exception as e:
            print(f"Error en Modelo al agregar material: {str(e)}")
            return False
        finally:
            db.close()
    
    @staticmethod
    def update_material(id, nombre, descripcion, codigo_barra, cantidad, unidad_medida, monto_unitario, stock_minimo, estado):
        """Actualiza un material existente"""
        db = DBManager()
        try:
            query = """
            UPDATE materiales 
            SET nombre = ?, descripcion = ?, codigo_barra = ?, cantidad = ?, unidad_medida = ?, monto_unitario = ?, stock_minimo = ?, estado = ?
            WHERE id = ?
            """
            db.execute_query(query, (nombre, descripcion, codigo_barra, cantidad, unidad_medida, monto_unitario, stock_minimo, estado, id))
            return True
        except Exception as e:
            print(f"Error en Modelo al actualizar material: {str(e)}")
            return False
        finally:
            db.close()
    
    @staticmethod
    def delete_material(id):
        """Elimina un material por su ID"""
        db = DBManager()
        try:
            query = "DELETE FROM materiales WHERE id = ?"
            db.execute_query(query, (id,))
            return True
        except Exception as e:
            print(f"Error en Modelo al eliminar material: {str(e)}")
            return False
        finally:
            db.close()

    @staticmethod
    def update_cantidad(material_id, nueva_cantidad):
        """Actualiza únicamente la cantidad/stock de un material"""
        db = DBManager()
        try:
            query = "UPDATE materiales SET cantidad = ? WHERE id = ?"
            db.execute_query(query, (nueva_cantidad, material_id))
            return True
        except Exception as e:
            print(f"Error en Modelo al actualizar cantidad: {str(e)}")
            return False
        finally:
            db.close()

    @staticmethod
    def deactivate_material(id):
        """Desactiva un material por su ID (cambia estado a 'inactivo')"""
        db = DBManager()
        try:
            query = "UPDATE materiales SET estado = 'inactivo' WHERE id = ?"
            db.execute_query(query, (id,))
            return True
        except Exception as e:
            print(f"Error en Modelo al desactivar material: {str(e)}")
            return False
        finally:
            db.close()

    @staticmethod
    def search_materials(search_text):
        """Busca materiales por nombre, descripción o código de barras"""
        db = DBManager()
        try:
            query = """
            SELECT id, nombre, descripcion, codigo_barra, cantidad, unidad_medida, monto_unitario, stock_minimo, estado
            FROM materiales
            WHERE nombre LIKE ? OR descripcion LIKE ? OR codigo_barra LIKE ?
            """
            like_pattern = f"%{search_text}%"
            return db.fetch_all(query, (like_pattern, like_pattern, like_pattern))
        except Exception as e:
            print(f"Error en Modelo al buscar materiales: {str(e)}")
            return []
        finally:
            db.close()