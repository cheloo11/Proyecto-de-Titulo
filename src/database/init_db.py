import hashlib
import datetime
from database.db_manager import DBManager

def initialize_database():
    """Inicializa la base de datos completa con todas las tablas necesarias"""
    print("Inicializando base de datos...")
    
    db = DBManager()
    
    try:
        # ---------- TABLAS DE AUTENTICACIÓN ----------
        # Tabla de perfiles
        db.execute_query('''
        CREATE TABLE IF NOT EXISTS perfiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT
        )
        ''')
        print("Tabla 'perfiles' creada o ya existe.")
        
        # Tabla de usuarios
        db.execute_query('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            activo BOOLEAN DEFAULT 1,
            id_perfil INTEGER NOT NULL,
            last_login TIMESTAMP,
            FOREIGN KEY (id_perfil) REFERENCES perfiles(id)
        )
        ''')
        print("Tabla 'usuarios' creada o ya existe.")
        
        # ---------- TABLAS PRINCIPALES DEL SISTEMA ----------
        # Tabla de obras con el nuevo campo estado
        db.execute_query('''
        CREATE TABLE IF NOT EXISTS obras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            codigo TEXT UNIQUE,
            direccion TEXT,
            fecha_inicio DATE,
            fecha_fin DATE,
            jefe_responsable TEXT,
            estado TEXT DEFAULT 'activa'
        )
        ''')
        print("Tabla 'obras' creada o ya existe.")
        
        # Tabla de contratistas
        db.execute_query('''
        CREATE TABLE IF NOT EXISTS contratistas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            empresa TEXT,
            telefono TEXT,
            estado TEXT DEFAULT 'Activo'
        )
        ''')
        print("Tabla 'contratistas' creada o ya existe.")
        
        # Tabla de materiales
        db.execute_query('''
        CREATE TABLE IF NOT EXISTS materiales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            codigo_barra TEXT NOT NULL UNIQUE,
            cantidad REAL DEFAULT 0,
            unidad_medida TEXT,
            monto_unitario REAL
        )
        ''')
        print("Tabla 'materiales' creada o ya existe.")
        
        # ---------- TABLAS DE RELACIÓN Y OPERACIONES ----------
        # Tabla de movimientos
        db.execute_query('''
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_material INTEGER NOT NULL,
            id_obra INTEGER NOT NULL,
            id_usuario INTEGER NOT NULL,
            id_contratista INTEGER NOT NULL,
            tipo_movimiento TEXT NOT NULL CHECK(tipo_movimiento IN ('entrada', 'salida')),
            cantidad REAL NOT NULL CHECK(cantidad > 0),
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(id_contratista) REFERENCES contratistas(id),
            FOREIGN KEY(id_material) REFERENCES materiales(id),
            FOREIGN KEY(id_obra) REFERENCES obras(id),
            FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
        )
        ''')
        print("Tabla 'movimientos' creada o ya existe.")
        
        # Tabla de alertas
        db.execute_query('''
        CREATE TABLE IF NOT EXISTS alertas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_material INTEGER NOT NULL,
            id_obra INTEGER,
            id_usuario INTEGER,
            tipo_alerta TEXT NOT NULL,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(id_material) REFERENCES materiales(id),
            FOREIGN KEY(id_obra) REFERENCES obras(id),
            FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
        )
        ''')
        print("Tabla 'alertas' creada o ya existe.")
        
        # Tabla de bloqueos
        db.execute_query('''
        CREATE TABLE IF NOT EXISTS bloqueos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            motivo TEXT,
            fecha_bloqueo DATETIME DEFAULT CURRENT_TIMESTAMP,
            id_usuario INTEGER,
            desbloqueado BOOLEAN DEFAULT 0,
            fecha_desbloqueo DATETIME,
            FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
        )
        ''')
        print("Tabla 'bloqueos' creada o ya existe.")
        
        # Tabla de consumo estándar
        db.execute_query('''
        CREATE TABLE IF NOT EXISTS consumo_estandar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_material INTEGER NOT NULL,
            cantidar_estandar REAL NOT NULL,
            periodo TEXT,
            FOREIGN KEY(id_material) REFERENCES materiales(id)
        )
        ''')
        print("Tabla 'consumo_estandar' creada o ya existe.")
        
        # ---------- DATOS INICIALES ----------
        # Verificar si ya existen perfiles
        perfiles = db.fetch_all("SELECT COUNT(*) FROM perfiles")
        if perfiles and perfiles[0][0] == 0:
            # Insertar perfiles por defecto
            db.execute_query(
                'INSERT INTO perfiles (nombre, descripcion) VALUES (?, ?)', 
                ('Administrador', 'Acceso completo al sistema')
            )
            db.execute_query(
                'INSERT INTO perfiles (nombre, descripcion) VALUES (?, ?)', 
                ('Usuario', 'Acceso limitado al sistema')
            )
            print("Perfiles predeterminados creados.")
            
        # Verificar si ya existen usuarios
        usuarios = db.fetch_all("SELECT COUNT(*) FROM usuarios")
        if usuarios and usuarios[0][0] == 0:
            # Insertar usuario administrador por defecto
            admin_password_hash = hashlib.sha256("admin123".encode()).hexdigest()
            
            db.execute_query('''
            INSERT INTO usuarios (nombre, email, password_hash, id_perfil)
            VALUES (?, ?, ?, ?)
            ''', ('admin', 'admin@jminventory.com', admin_password_hash, 1))
            
            print("Usuario administrador por defecto creado:")
            print("  - Usuario: admin")
            print("  - Contraseña: admin123")
            
        # Verificar si ya existen contratistas
        contratistas = db.fetch_all("SELECT COUNT(*) FROM contratistas")
        if contratistas and contratistas[0][0] == 0:
            # Quitar la creación de contratista de ejemplo
            print("No existen contratistas en la base de datos.")

        # Tabla de control de versiones para futuras actualizaciones
        db.execute_query('''
        CREATE TABLE IF NOT EXISTS schema_version (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version TEXT NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Verificar si ya existe versión
        version = db.fetch_all("SELECT COUNT(*) FROM schema_version")
        if version and version[0][0] == 0:
            db.execute_query("INSERT INTO schema_version (version) VALUES ('1.0')")
            print("Versión de esquema registrada: 1.0")
        
        print("Base de datos inicializada correctamente.")
        
        # Verificar y añadir el campo estado si no existe
        try:
            db.fetch_one("SELECT estado FROM obras LIMIT 1")
            print("El campo 'estado' ya existe en la tabla obras.")
        except:
            # Si no existe, agregar el campo
            db.execute_query("ALTER TABLE obras ADD COLUMN estado TEXT DEFAULT 'activa'")
            print("Campo 'estado' añadido correctamente a la tabla obras.")
        
        # Verificar y añadir el campo 'codigo' si no existe en contratistas
        try:
            db.fetch_one("SELECT codigo FROM contratistas LIMIT 1")
            print("El campo 'codigo' ya existe en la tabla contratistas.")
        except Exception:
            db.execute_query("ALTER TABLE contratistas ADD COLUMN codigo TEXT")
            print("Campo 'codigo' añadido correctamente a la tabla contratistas.")
            # Crear índice único para el campo 'codigo'
            db.execute_query("CREATE UNIQUE INDEX IF NOT EXISTS idx_codigo_contratistas ON contratistas(codigo)")
            print("Índice único para 'codigo' creado en la tabla contratistas.")
        
        return True
        
    except Exception as e:
        print(f"Error al inicializar la base de datos: {str(e)}")
        return False
    finally:
        db.close()

def add_new_fields_to_materials():
    """Agrega nuevos campos a la tabla materiales si no existen"""
    print("Verificando y añadiendo nuevos campos a la tabla materiales...")
    
    db = DBManager()
    
    try:
        # Verificar si la columna stock_minimo ya existe
        try:
            db.fetch_one("SELECT stock_minimo FROM materiales LIMIT 1")
            print("El campo 'stock_minimo' ya existe en la tabla materiales.")
        except:
            # Si no existe, agregarla
            db.execute_query("ALTER TABLE materiales ADD COLUMN stock_minimo REAL DEFAULT 0")
            print("Campo 'stock_minimo' añadido correctamente a la tabla materiales.")
        
        return True
    except Exception as e:
        print(f"Error al modificar la tabla materiales: {str(e)}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    initialize_database()
    add_new_fields_to_materials()