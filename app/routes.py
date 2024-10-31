from fastapi import APIRouter, HTTPException
from app.models import EmployeeCreate, Employee, AreaCreate, Area, HorarioCreate, Horario, AsignacionCreate, Asignacion, TrenCreate, Tren, RutaCreate, Ruta, TrenRutaCreate
from app.database import get_db_connection
from typing import List

router = APIRouter()

# Rutas para áreas
@router.post("/areas/", response_model=Area, tags=["Áreas"])
def create_area(area: AreaCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO areas (nombre_area)
        VALUES (%s)
        """
        cursor.execute(query, (area.nombre_area,))
        conn.commit()
        
        area_id = cursor.lastrowid
        return Area(area_id=area_id, **area.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/areas/bulk/", response_model=List[Area], tags=["Áreas"])
def create_areas_bulk(areas: List[AreaCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO areas (nombre_area)
        VALUES (%s)
        """
        values = [(a.nombre_area,) for a in areas]
        
        cursor.executemany(query, values)
        conn.commit()
        
        cursor.execute("SELECT LAST_INSERT_ID()")
        last_id = cursor.fetchone()[0]
        
        area_ids = range(last_id - len(areas) + 1, last_id + 1)
        
        return [Area(area_id=oid, **a.dict()) for oid, a in zip(area_ids, areas)]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/areas/", response_model=List[Area], tags=["Áreas"])
def list_areas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM areas"
        cursor.execute(query)
        areas = cursor.fetchall()
        return [Area(**area) for area in areas]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Rutas para empleados
@router.post("/empleados/", response_model=Employee, tags=["Empleados"])
def create_employee(employee: EmployeeCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO empleados (nombre, apellido, cargo, area_id)
        VALUES (%s, %s, %s, %s)
        """
        values = (employee.nombre, employee.apellido, employee.cargo, employee.area_id)
        
        cursor.execute(query, values)
        conn.commit()
        
        codigo_empleado = cursor.lastrowid
        return Employee(codigo_empleado=codigo_empleado, **employee.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/empleados/bulk/", response_model=List[Employee], tags=["Empleados"])
def create_employees_bulk(employees: List[EmployeeCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO empleados (nombre, apellido, cargo, area_id)
        VALUES (%s, %s, %s, %s)
        """
        values = [(e.nombre, e.apellido, e.cargo, e.area_id) for e in employees]
        
        cursor.executemany(query, values)
        conn.commit()
        
        # Obtener los IDs de los empleados insertados
        cursor.execute("SELECT LAST_INSERT_ID()")
        last_id = cursor.fetchone()[0]

        employee_ids = range(last_id - len(employees) + 1, last_id + 1)
        
        return [Employee(codigo_empleado=oid, **e.dict()) for oid, e in zip(employee_ids, employees)]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/empleados/", response_model=List[Employee], tags=["Empleados"])
def list_employees():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM empleados"
        cursor.execute(query)
        employees = cursor.fetchall()
        return [Employee(**employee) for employee in employees]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Rutas para horarios
@router.post("/horarios/", response_model=Horario, tags=["Horarios"])
def create_horario(horario: HorarioCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO horarios (hora_entrada, hora_salida)
        VALUES (%s, %s)
        """
        values = (horario.hora_entrada, horario.hora_salida)
        
        cursor.execute(query, values)
        conn.commit()
        
        horario_id = cursor.lastrowid
        return Horario(horario_id=horario_id, **horario.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/horarios/bulk/", response_model=List[Horario], tags=["Horarios"])
def create_horarios_bulk(horarios: List[HorarioCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO horarios (hora_entrada, hora_salida)
        VALUES (%s, %s)
        """
        values = [(h.hora_entrada, h.hora_salida) for h in horarios]
        
        cursor.executemany(query, values)
        conn.commit()
        
        cursor.execute("SELECT LAST_INSERT_ID()")
        last_id = cursor.fetchone()[0]
        
        horario_ids = range(last_id - len(horarios) + 1, last_id + 1)
        
        return [Horario(horario_id=oid, **h.dict()) for oid, h in zip(horario_ids, horarios)]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/horarios/", response_model=List[Horario], tags=["Horarios"])
def list_horarios():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM horarios"
        cursor.execute(query)
        horarios = cursor.fetchall()
        return [Horario(**horario) for horario in horarios]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Rutas para trenes
@router.post("/trenes/", response_model=Tren, tags=["Trenes"])
def create_tren(tren: TrenCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO trenes (nombre_tren, capacidad)
        VALUES (%s, %s)
        """
        values = (tren.nombre_tren, tren.capacidad)
        
        cursor.execute(query, values)
        conn.commit()
        
        tren_id = cursor.lastrowid
        return Tren(tren_id=tren_id, **tren.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/trenes/bulk/", response_model=List[Tren], tags=["Trenes"])
def create_trenes_bulk(trenes: List[TrenCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO trenes (nombre_tren, capacidad)
        VALUES (%s, %s)
        """
        values = [(t.nombre_tren, t.capacidad) for t in trenes]
        
        cursor.executemany(query, values)
        conn.commit()
        
        cursor.execute("SELECT LAST_INSERT_ID()")
        last_id = cursor.fetchone()[0]
        
        tren_ids = range(last_id - len(trenes) + 1, last_id + 1)
        
        return [Tren(tren_id=oid, **t.dict()) for oid, t in zip(tren_ids, trenes)]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/trenes/", response_model=List[Tren], tags=["Trenes"])
def list_trenes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM trenes"
        cursor.execute(query)
        trenes = cursor.fetchall()
        return [Tren(**tren) for tren in trenes]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Rutas para rutas
@router.post("/rutas/", response_model=Ruta, tags=["Rutas"])
def create_ruta(ruta: RutaCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO rutas (origen, destino)
        VALUES (%s, %s)
        """
        values = (ruta.origen, ruta.destino)
        
        cursor.execute(query, values)
        conn.commit()
        
        ruta_id = cursor.lastrowid
        return Ruta(ruta_id=ruta_id, **ruta.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/rutas/bulk/", response_model=List[Ruta], tags=["Rutas"])
def create_rutas_bulk(rutas: List[RutaCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO rutas (origen, destino)
        VALUES (%s, %s)
        """
        values = [(r.origen, r.destino) for r in rutas]
        
        cursor.executemany(query, values)
        conn.commit()
        
        cursor.execute("SELECT LAST_INSERT_ID()")
        last_id = cursor.fetchone()[0]
        
        ruta_ids = range(last_id - len(rutas) + 1, last_id + 1)
        
        return [Ruta(ruta_id=oid, **r.dict()) for oid, r in zip(ruta_ids, rutas)]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/rutas/", response_model=List[Ruta], tags=["Rutas"])
def list_rutas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM rutas"
        cursor.execute(query)
        rutas = cursor.fetchall()
        return [Ruta(**ruta) for ruta in rutas]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# Rutas para asignaciones
@router.post("/asignaciones/", response_model=Asignacion, tags=["Asignaciones"])
def create_asignacion(asignacion: AsignacionCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO asignaciones (codigo_empleado, horario_id, tren_id)
        VALUES (%s, %s, %s)
        """
        values = (asignacion.codigo_empleado, asignacion.horario_id, asignacion.tren_id)
        
        cursor.execute(query, values)
        conn.commit()
        
        asignacion_id = cursor.lastrowid
        return Asignacion(asignacion_id=asignacion_id, **asignacion.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/asignaciones/bulk/", response_model=List[Asignacion], tags=["Asignaciones"])
def create_asignaciones_bulk(asignaciones: List[AsignacionCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO asignaciones (codigo_empleado, horario_id, tren_id)
        VALUES (%s, %s, %s)
        """
        values = [(a.codigo_empleado, a.horario_id, a.tren_id) for a in asignaciones]
        
        cursor.executemany(query, values)
        conn.commit()
        
        cursor.execute("SELECT LAST_INSERT_ID()")
        last_id = cursor.fetchone()[0]
        
        asignacion_ids = range(last_id - len(asignaciones) + 1, last_id + 1)
        
        return [Asignacion(asignacion_id=oid, **a.dict()) for oid, a in zip(asignacion_ids, asignaciones)]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/asignaciones/", response_model=List[Asignacion], tags=["Asignaciones"])
def list_asignaciones():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM asignaciones"
        cursor.execute(query)
        asignaciones = cursor.fetchall()
        return [Asignacion(**asignacion) for asignacion in asignaciones]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()