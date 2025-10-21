from models.movimiento_model import MovimientoModel
from controllers.material_controller import MaterialController


class MovimientoController:
    @staticmethod
    def registrar_salida(movimiento):
        """Registra una salida: valida stock, actualiza cantidad y crea el movimiento."""
        # Validar material y stock usando el controller
        material = MaterialController.get_by_id(movimiento["id_material"])
        if not material:
            return False, "Material no encontrado."

        # material es una tupla 
        try:
            cantidad_actual = material[4]
        except Exception:
            return False, "Formato de material inesperado."

        if movimiento["cantidad"] > cantidad_actual:
            return False, "No hay suficiente stock."

        nuevo_stock = cantidad_actual - movimiento["cantidad"]
        actualizado = MaterialController.update_cantidad(movimiento["id_material"], nuevo_stock)
        if not actualizado:
            return False, "No se pudo actualizar el stock."

        # Registrar movimiento
        registrado = MovimientoModel.insert_salida(movimiento)
        if registrado:
            return True, "Movimiento registrado correctamente."
        else:
            return False, "No se pudo registrar el movimiento."
            
    @staticmethod
    def get_all_movimientos():
        """
        Obtiene todos los movimientos y los formatea para la UI.
        
        Returns:
            list: Lista de diccionarios con los datos de los movimientos.
        """
        try:
            # Obtener datos del modelo
            movimientos_data = MovimientoModel.get_all()
            
            if not movimientos_data:
                return []
            
            # Convertir a lista de diccionarios
            movimientos = []
            for m in movimientos_data:
                # Formato esperado: 
                # id, tipo_movimiento, cantidad, fecha, material_codigo, material_nombre,
                # obra_codigo, obra_nombre, contratista_nombre
                movimientos.append({
                    "id": m[0],
                    "tipo_movimiento": m[1],
                    "cantidad": m[2],
                    "fecha": m[3],
                    "material_codigo": m[4],
                    "material_nombre": m[5],
                    "obra_codigo": m[6],
                    "obra_nombre": m[7],
                    "contratista_nombre": m[8],
                    "usuario_id": m[9] if len(m) > 9 else "N/A"
                })
            
            return movimientos
        except Exception as e:
            print(f"Error al obtener movimientos: {e}")
            return []