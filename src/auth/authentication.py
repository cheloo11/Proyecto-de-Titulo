import hashlib
import datetime
from database.db_manager import DBManager
from PyQt6.QtWidgets import QMessageBox

class AuthService:
    @staticmethod
    def authenticate_user(username, password):
        """Autentica al usuario contra la base de datos"""
        try:
            db = DBManager()
            
            # Generar hash de la contraseña
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # Consulta para verificar credenciales por nombre de usuario
            query = '''
            SELECT u.id, u.nombre, u.email, u.id_perfil, p.nombre as perfil_nombre
            FROM usuarios u
            JOIN perfiles p ON u.id_perfil = p.id
            WHERE u.nombre = ? AND u.password_hash = ? AND u.activo = 1
            '''
            
            user = db.fetch_one(query, (username, password_hash))
            
            if user:
                # Actualizar último login
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                update_query = 'UPDATE usuarios SET last_login = ? WHERE id = ?'
                db.execute_query(update_query, (now, user[0]))
                
                # Crear datos del usuario
                result = {
                    "id": user[0],
                    "nombre": user[1],
                    "email": user[2],
                    "id_perfil": user[3],
                    "perfil": user[4],
                    "autenticado": True
                }
                
                return result
            else:
                return {"autenticado": False}
                
        except Exception as e:
            return {"autenticado": False, "error": str(e)}
        finally:
            if 'db' in locals():
                db.close()