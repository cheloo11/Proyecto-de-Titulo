from models.obra_model import ObraModel

class ObraController:
    """Controlador para la lógica de negocio de obras"""
    
    @staticmethod
    def get_all_obras():
        """Obtiene todas las obras con formato para mostrar en la UI"""
        obras_data = ObraModel.get_all_obras()
        formatted_obras = []
        
        for obra in obras_data:
            # Extraer datos de la obra 
            id, nombre, codigo, direccion, fecha_inicio, fecha_fin, jefe_responsable, estado = obra
            
            # Crear una representación formateada para la UI
            formatted_obra = {
                "id": id,
                "codigo": codigo,
                "nombre": nombre,
                "direccion": direccion,
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
                "jefe_responsable": jefe_responsable,
                "estado": estado or "activa" 
            }
            
            formatted_obras.append(formatted_obra)
        
        return formatted_obras
    
    @staticmethod
    def get_obra_by_code(code):
        """Busca una obra por su código y la formatea para la UI"""
        obra = ObraModel.get_obra_by_code(code)
        
        if not obra:
            return None
            
        # Extraer datos de la obra (ahora incluye estado)
        id, nombre, codigo, direccion, fecha_inicio, fecha_fin, jefe_responsable, estado = obra
        
        # Crear diccionario con datos formateados
        obra_data = {
            "id": id,
            "codigo": codigo,
            "nombre": nombre,
            "direccion": direccion,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "jefe_responsable": jefe_responsable,
            "estado": estado or "activa" 
        }
        
        return obra_data
    
    @staticmethod
    def add_obra(nombre, codigo, direccion, fecha_inicio, fecha_fin, jefe_responsable, estado="activa"):
        """Valida y agrega una nueva obra"""
        # Validación básica
        if not nombre or not codigo or not direccion:
            return False, "El nombre, código y dirección son obligatorios"
            
        if ObraModel.get_obra_by_code(codigo):
            return False, f"Ya existe una obra con el código {codigo}"
        
        # Intentar agregar la obra
        success = ObraModel.add_obra(
            nombre, codigo, direccion, fecha_inicio, fecha_fin, jefe_responsable, estado
        )
        
        if success:
            return True, "Obra agregada correctamente"
        else:
            return False, "Error al agregar la obra"
    
    @staticmethod
    def update_obra(id, nombre, direccion, fecha_inicio, fecha_fin, jefe_responsable, estado):
        """Valida y actualiza una obra existente"""
        # Validación básica
        if not nombre or not direccion:
            return False, "El nombre y la dirección son obligatorios"
        
        # Intentar actualizar
        success = ObraModel.update_obra(
            id, nombre, direccion, fecha_inicio, fecha_fin, jefe_responsable, estado
        )
        
        if success:
            return True, "Obra actualizada correctamente"
        else:
            return False, "Error al actualizar la obra"
    
    @staticmethod
    def delete_obra(id):
        """Elimina una obra por su ID"""
        success = ObraModel.delete_obra(id)
        
        if success:
            return True, "Obra eliminada correctamente"
        else:
            return False, "Error al eliminar la obra"