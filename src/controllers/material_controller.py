from database.db_manager import DBManager

class MaterialController:
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
            rows = db.fetch_all(query)
            # Convertir cada tupla en un diccionario
            materials = []
            for row in rows:
                materials.append({
                    "id": row[0],
                    "nombre": row[1],
                    "descripcion": row[2],
                    "codigo": row[3],
                    "stock": row[4],
                    "unidad_medida": row[5],
                    "precio": row[6],
                    "stock_min": row[7]
                })
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
            SELECT id, nombre, descripcion, codigo_barra, cantidad, unidad_medida, monto_unitario, stock_minimo
            FROM materiales
            WHERE codigo_barra = ?
            """
            row = db.fetch_one(query, (code,))
            if row:
                return {
                    "id": row[0],
                    "nombre": row[1],
                    "descripcion": row[2],
                    "codigo": row[3],
                    "stock": row[4],
                    "unidad_medida": row[5],
                    "precio": row[6],
                    "stock_min": row[7]
                }
            else:
                return None
        except Exception as e:
            print(f"Error al buscar material por código: {str(e)}")
            return None
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
            return True, "Material agregado correctamente"
        except Exception as e:
            print(f"Error al agregar material: {str(e)}")
            return False, f"Error al agregar material: {str(e)}"
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
            db.execute_query(query, (nombre, descripcion, codigo_barra, cantidad, unidad_medida, monto_unitario, stock_minimo, id))
            return True, "Material actualizado correctamente"
        except Exception as e:
            print(f"Error al actualizar material: {str(e)}")
            return False, f"Error al actualizar material: {str(e)}"
        finally:
            db.close()
    
    @staticmethod
    def delete_material(id):
        """Elimina un material por su ID"""
        db = DBManager()
        try:
            query = "DELETE FROM materiales WHERE id = ?"
            db.execute_query(query, (id,))
            return True, "Material eliminado correctamente"
        except Exception as e:
            print(f"Error al eliminar material: {str(e)}")
            return False, f"Error al eliminar material: {str(e)}"
        finally:
            db.close()

    @staticmethod
    def get_by_id(material_id):
        """Wrapper para obtener material por id"""
        db_rows = None
        try:
            from models.material_model import MaterialModel
            return MaterialModel.get_by_id(material_id)
        except Exception as e:
            print(f"Error en controller get_by_id: {e}")
            return None

    @staticmethod
    def update_cantidad(material_id, nueva_cantidad):
        """Wrapper para actualizar solo la cantidad del material"""
        try:
            from models.material_model import MaterialModel
            return MaterialModel.update_cantidad(material_id, nueva_cantidad)
        except Exception as e:
            print(f"Error en controller update_cantidad: {e}")
            return False