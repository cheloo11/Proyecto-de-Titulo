from src.database.db_manager import DBManager

def add_observaciones_to_movimientos():
    """Añade el campo 'observaciones' a la tabla movimientos si no existe"""
    print("Verificando y añadiendo el campo 'observaciones' a la tabla movimientos...")
    
    db = DBManager()
    
    try:
        # Verificar si la columna observaciones ya existe
        try:
            db.fetch_one("SELECT observaciones FROM movimientos LIMIT 1")
            print("El campo 'observaciones' ya existe en la tabla movimientos.")
        except:
            # Si no existe, agregarla
            db.execute_query("ALTER TABLE movimientos ADD COLUMN observaciones TEXT DEFAULT ''")
            print("Campo 'observaciones' añadido correctamente a la tabla movimientos.")
        
        return True
    except Exception as e:
        print(f"Error al modificar la tabla movimientos: {str(e)}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    add_observaciones_to_movimientos()