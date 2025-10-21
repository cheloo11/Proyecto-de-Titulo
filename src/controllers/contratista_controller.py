from models.contratista_model import ContratistaModel

class ContratistaController:
    @staticmethod
    def get_all():
        rows = ContratistaModel.get_all()
        return [
            {
                "id": r[0],
                "codigo": r[1],
                "nombre": r[2],
                "empresa": r[3],
                "telefono": r[4],
                "estado": r[5]
            }
            for r in rows
        ]

    @staticmethod
    def get_by_code(codigo):
        r = ContratistaModel.get_by_code(codigo)
        if r:
            return {
                "id": r[0],
                "codigo": r[1],
                "nombre": r[2],
                "empresa": r[3],
                "telefono": r[4],
                "estado": r[5]
            }
        return None

    @staticmethod
    def add(codigo, nombre, empresa, telefono, estado="Activo"):
        return ContratistaModel.add(codigo, nombre, empresa, telefono, estado)

    @staticmethod
    def update(id, nombre, empresa, telefono, estado):
        return ContratistaModel.update(id, nombre, empresa, telefono, estado)

    @staticmethod
    def delete(id):
        return ContratistaModel.delete(id)