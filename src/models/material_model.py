from database.db_manager import DBManager

class MaterialModel:
    """Modelo para acceso a datos de materiales"""
    
    @staticmethod
    def get_all_materials():
        """Obtiene todos los materiales de la base de datos"""
        db = DBManager()
        try:
            query = """
            SELECT id, nombre, descripcion, codigo_barra, cantidad, unidad_medida, monto_unitario, stock_minimo 
            FROM materiales
            ORDER BY nombre
            """
            materials = db.fetch_all(query)
            return materials
        except Exception as e:
            print(f"Error al obtener materiales: {str(e)}")
            return []
        finally:
            db.close()
    
    @staticmethod
    def get_material_by_code(code):
        """Busca un material por su código de barras"""
        db = DBManager()
        try:
            query = """
            SELECT id, nombre, descripcion, codigo_barra, cantidad, unidad_medida, monto_unitario 
            FROM materiales
            WHERE codigo_barra = ?
            """
            material = db.fetch_one(query, (code,))
            return material
        except Exception as e:
            print(f"Error al buscar material por código: {str(e)}")
            return None
        finally:
            db.close()

    @staticmethod
    def get_by_id(material_id):
        """Obtiene un material por su ID"""
        db = DBManager()
        try:
            query = """
            SELECT id, nombre, descripcion, codigo_barra, cantidad, unidad_medida, monto_unitario, stock_minimo
            FROM materiales
            WHERE id = ?
            """
            return db.fetch_one(query, (material_id,))
        except Exception as e:
            print(f"Error al obtener material por id: {str(e)}")
            return None
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
            print(f"Error al actualizar cantidad: {str(e)}")
            return False
        finally:
            db.close()
    
    @staticmethod
    def add_material(nombre, descripcion, codigo_barra, cantidad, unidad_medida, monto_unitario, stock_minimo=0):
        """Agrega un nuevo material a la base de datos"""
        db = DBManager()
        try:
            query = """
            INSERT INTO materiales (nombre, descripcion, codigo_barra, cantidad, unidad_medida, monto_unitario, stock_minimo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            db.execute_query(query, (nombre, descripcion, codigo_barra, cantidad, unidad_medida, monto_unitario, stock_minimo))
            return True
        except Exception as e:
            print(f"Error al agregar material: {str(e)}")
            return False
        finally:
            db.close()
    
    @staticmethod
    def update_material(id, nombre, descripcion, codigo_barra, cantidad, unidad_medida, monto_unitario, stock_minimo):
        """Actualiza un material existente"""
        db = DBManager()
        try:
            query = """
            UPDATE materiales 
            SET nombre = ?, descripcion = ?, codigo_barra = ?, cantidad = ?, unidad_medida = ?, monto_unitario = ?, stock_minimo = ?
            WHERE id = ?
            """
            db.execute_query(query, (nombre, descripcion, codigo_barra, cantidad, unidad_medida, monto_unitario, id, stock_minimo))
            return True
        except Exception as e:
            print(f"Error al actualizar material: {str(e)}")
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
            print(f"Error al eliminar material: {str(e)}")
            return False
        finally:
            db.close()