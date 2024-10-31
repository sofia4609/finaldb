from pydantic import BaseModel, Field, EmailStr
from datetime import date
from typing import Optional

class EmployeeCreate(BaseModel):
    nombre: str = Field(..., description="Nombre completo del empleado (campo requerido)")
    apellido: str = Field(..., description="Apellido del empleado (campo requerido)")
    cargo: str = Field(..., description="Cargo del empleado (campo requerido)")
    area_id: Optional[int] = Field(None, description="ID del área (opcional)")

class Employee(EmployeeCreate):
    codigo_empleado: int

class AreaCreate(BaseModel):
    nombre_area: str = Field(..., description="Nombre del área (campo requerido)")

class Area(AreaCreate):
    area_id: int

class HorarioCreate(BaseModel):
    hora_entrada: str = Field(..., description="Hora de entrada (campo requerido)")
    hora_salida: str = Field(..., description="Hora de salida (campo requerido)")

class Horario(HorarioCreate):
    horario_id: int

class AsignacionCreate(BaseModel):
    codigo_empleado: int = Field(..., description="Código del empleado (campo requerido)")
    horario_id: int = Field(..., description="ID del horario (campo requerido)")
    tren_id: int = Field(..., description="ID del tren (campo requerido)")

class Asignacion(AsignacionCreate):
    asignacion_id: int

class TrenCreate(BaseModel):
    nombre_tren: str = Field(..., description="Nombre del tren (campo requerido)")
    capacidad: int = Field(..., description="Capacidad del tren (campo requerido)")

class Tren(TrenCreate):
    tren_id: int

class RutaCreate(BaseModel):
    origen: str = Field(..., description="Origen de la ruta (campo requerido)")
    destino: str = Field(..., description="Destino de la ruta (campo requerido)")

class Ruta(RutaCreate):
    ruta_id: int

class TrenRutaCreate(BaseModel):
    tren_id: int = Field(..., description="ID del tren (campo requerido)")
    ruta_id: int = Field(..., description="ID de la ruta (campo requerido)")

class TrenRuta(TrenRutaCreate):
    pass