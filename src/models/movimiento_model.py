from database.db_manager import DBManager

class MovimientoModel:
    @staticmethod
    def insert_salida(movimiento):
        """
        Inserta un registro de salida de material en la base de datos.
        
        Args:
            movimiento: Diccionario con los datos del movimiento
                - id_material: ID del material
                - id_obra: ID de la obra
                - id_usuario: ID del usuario que registra el movimiento
                - id_contratista: ID del contratista
                - tipo_movimiento: Tipo de movimiento ('salida')
                - cantidad: Cantidad de material
                - fecha: Fecha del movimiento
                - observaciones: Observaciones del movimiento (opcional)
                
        Returns:
            bool: True si se registró correctamente, False en caso contrario
        """
        db = DBManager()
        try:
            db.execute_query(
                """INSERT INTO movimientos 
                   (id_material, id_obra, id_usuario, id_contratista, tipo_movimiento, cantidad, fecha, observaciones) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    movimiento["id_material"],
                    movimiento["id_obra"],
                    movimiento["id_usuario"],
                    movimiento["id_contratista"],
                    movimiento["tipo_movimiento"],
                    movimiento["cantidad"],
                    movimiento["fecha"],
                    movimiento.get("observaciones", "")
                )
            )
            return True
        except Exception as e:
            print(f"Error al registrar movimiento: {e}")
            return False
        finally:
            db.close()
    
    @staticmethod
    def get_all():
        """
        Obtiene todos los movimientos de la base de datos.
        
        Returns:
            list: Lista de tuplas con los datos de los movimientos
        """
        db = DBManager()
        try:
            return db.fetch_all("""
                SELECT m.id, m.tipo_movimiento, m.cantidad, m.fecha, 
                       mat.codigo_barra, mat.nombre,
                       o.codigo, o.nombre,
                       c.nombre, m.id_usuario, m.observaciones
                FROM movimientos m
                JOIN materiales mat ON m.id_material = mat.id
                JOIN obras o ON m.id_obra = o.id
                JOIN contratistas c ON m.id_contratista = c.id
                ORDER BY m.fecha DESC
            """)
        finally:
            db.close()