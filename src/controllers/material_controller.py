# Importa la CLASE Modelo, NO el DBManager
from models.material_model import MaterialModel

class MaterialController:
    """
    Controlador para materiales.
    Actúa como intermediario entre la Vista y el Modelo.
    NO contiene SQL.
    """
    
    @staticmethod
    def get_all_materials():
        """Obtiene todos los materiales (formateados como dict)"""
        try:
            # 1. Llama al Modelo
            rows = MaterialModel.get_all_materials()
            
            # 2. Formatea los datos para la Vista (tu lógica original)
            materials = []
            for row in rows:
                materials.append({
                    "id": row[0],
                    "nombre": row[1],
                    "descripcion": row[2],
                    "codigo_barra": row[3],
                    "cantidad": row[4],
                    "unidad_medida": row[5],
                    "monto_unitario": row[6],
                    "stock_minimo": row[7],
                    "estado": row[8]
                })
            return materials
        except Exception as e:
            print(f"Error en Controller al obtener materiales: {str(e)}")
            return []
    
    @staticmethod
    def get_material_by_code(code):
        """Busca un material por código (formateado como dict)"""
        try:
            # 1. Llama al Modelo
            row = MaterialModel.get_material_by_code(code)
            
            # 2. Formatea los datos (tu lógica original)
            if row:
                return {
                    "id": row[0],
                    "nombre": row[1],
                    "descripcion": row[2],
                    "codigo_barra": row[3],
                    "cantidad": row[4],
                    "unidad_medida": row[5],
                    "monto_unitario": row[6],
                    "stock_minimo": row[7],
                    "estado": row[8]
                }
            else:
                return None
        except Exception as e:
            print(f"Error en Controller al buscar por código: {str(e)}")
            return None
    
    @staticmethod
    def add_material(nombre, descripcion, codigo_barra, cantidad, unidad_medida, monto_unitario, stock_minimo=0, estado='activo'):
        """Pide al Modelo agregar un material y devuelve un mensaje"""
        try:
            # 1. Llama al Modelo
            success = MaterialModel.add_material(
                nombre, descripcion, codigo_barra, cantidad, 
                unidad_medida, monto_unitario, stock_minimo, estado
            )
            
            # 2. Formatea la respuesta (tu lógica original)
            if success:
                return True, "Material agregado correctamente"
            else:
                return False, "Error desde el Modelo al agregar material"
        except Exception as e:
            print(f"Error en Controller al agregar material: {str(e)}")
            return False, f"Error en Controller al agregar material: {str(e)}"
    
    @staticmethod
    def update_material(id, nombre, descripcion, codigo_barra, cantidad, unidad_medida, monto_unitario, stock_minimo, estado):
        """Pide al Modelo actualizar un material y devuelve un mensaje"""
        try:
            # 1. Llama al Modelo
            success = MaterialModel.update_material(
                id, nombre, descripcion, codigo_barra, cantidad, 
                unidad_medida, monto_unitario, stock_minimo, estado
            )
            
            # 2. Formatea la respuesta (tu lógica original)
            if success:
                return True, "Material actualizado correctamente"
            else:
                return False, "Error desde el Modelo al actualizar material"
        except Exception as e:
            print(f"Error en Controller al actualizar material: {str(e)}")
            return False, f"Error en Controller al actualizar material: {str(e)}"
    
    @staticmethod
    def delete_material(id):
        """Pide al Modelo eliminar un material y devuelve un mensaje"""
        try:
            # 1. Llama al Modelo
            success = MaterialModel.delete_material(id)
            
            # 2. Formatea la respuesta (tu lógica original)
            if success:
                return True, "Material eliminado correctamente"
            else:
                return False, "Error desde el Modelo al eliminar material"
        except Exception as e:
            print(f"Error en Controller al eliminar material: {str(e)}")
            return False, f"Error en Controller al eliminar material: {str(e)}"

    @staticmethod
    def get_by_id(material_id):
        """Obtiene un material por id (devuelve tupla cruda)"""
        try:
            # Esta función ya era correcta, solo llamaba al Modelo
            return MaterialModel.get_by_id(material_id)
        except Exception as e:
            print(f"Error en Controller get_by_id: {e}")
            return None

    @staticmethod
    def update_cantidad(material_id, nueva_cantidad):
        """Pide al Modelo actualizar solo la cantidad (devuelve True/False)"""
        try:
            # Esta función ya era correcta
            return MaterialModel.update_cantidad(material_id, nueva_cantidad)
        except Exception as e:
            print(f"Error en Controller update_cantidad: {e}")
            return False

    @staticmethod
    def deactivate_material(id):
        """Pide al Modelo desactivar un material y devuelve un mensaje"""
        try:
            # Esta función ya era correcta
            success = MaterialModel.deactivate_material(id)
            if success:
                return True, "Material desactivado correctamente"
            else:
                return False, "Error al desactivar material"
        except Exception as e:
            print(f"Error al desactivar material: {str(e)}")
            return False, f"Error al desactivar material: {str(e)}"

    @staticmethod
    def search_materials(search_text):
        """Busca materiales y los formatea como dict"""
        try:
            # 1. Llama al Modelo
            rows = MaterialModel.search_materials(search_text)
            
            # 2. Formatea los datos (tu lógica original)
            materials = []
            for row in rows:
                materials.append({
                    "id": row[0],
                    "nombre": row[1],
                    "descripcion": row[2],
                    "codigo_barra": row[3],
                    "cantidad": row[4],
                    "unidad_medida": row[5],
                    "monto_unitario": row[6],
                    "stock_minimo": row[7],
                    "estado": row[8]
                })
            return materials
        except Exception as e:
            print(f"Error en Controller al buscar materiales: {str(e)}")
            return []