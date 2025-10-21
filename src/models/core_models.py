class Usuario:
    """Modelo simple para usuarios."""
    def __init__(self, id, nombre, email, contrasena, activo, id_perfil):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.contrasena = contrasena
        self.activo = activo
        self.id_perfil = id_perfil

class Perfil:
    """Modelo simple para perfiles de usuario."""
    def __init__(self, id, nombre_rol, permisos):
        self.id = id
        self.nombre_rol = nombre_rol
        self.permisos = permisos

class Contratista:
    """Modelo simple para contratistas."""
    def __init__(self, id, nombre, contacto, telefono):
        self.id = id
        self.nombre = nombre
        self.contacto = contacto
        self.telefono = telefono

class Obra:
    """Modelo simple para obras."""
    def __init__(self, id, nombre, codigo, direccion, fecha_inicio, fecha_fin, jefe_responsable):
        self.id = id
        self.nombre = nombre
        self.codigo = codigo
        self.direccion = direccion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.jefe_responsable = jefe_responsable

class Movimiento:
    """Modelo simple para movimientos de materiales."""
    def __init__(self, id, id_material, id_obra, id_usuario, id_contratista, tipo_movimiento, cantidad, fecha, estado, fecha_modificacion):
        self.id = id
        self.id_material = id_material
        self.id_obra = id_obra
        self.id_usuario = id_usuario
        self.id_contratista = id_contratista
        self.tipo_movimiento = tipo_movimiento
        self.cantidad = cantidad
        self.fecha = fecha
        self.estado = estado
        self.fecha_modificacion = fecha_modificacion

class Alerta:
    """Modelo simple para alertas."""
    def __init__(self, id, id_material, id_obra, id_usuario, tipo_alerta, mensaje, fecha):
        self.id = id
        self.id_material = id_material
        self.id_obra = id_obra
        self.id_usuario = id_usuario
        self.tipo_alerta = tipo_alerta
        self.mensaje = mensaje
        self.fecha = fecha

class Bloqueo:
    """Modelo simple para bloqueos del sistema."""
    def __init__(self, id, motivo, fecha_bloqueo, id_usuario, desbloqueado, fecha_desbloqueo):
        self.id = id
        self.motivo = motivo
        self.fecha_bloqueo = fecha_bloqueo
        self.id_usuario = id_usuario
        self.desbloqueado = desbloqueado
        self.fecha_desbloqueo = fecha_desbloqueo

class ConsumoEstandar:
    """Modelo simple para consumo estándar de materiales."""
    def __init__(self, id, id_material, cantidad_estandar, periodo):
        self.id = id
        self.id_material = id_material
        self.cantidad_estandar = cantidad_estandar
        self.periodo = periodo
