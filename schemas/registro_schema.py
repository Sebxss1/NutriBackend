from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)
from datetime import date


class RegistroPaciente(BaseModel):
    nombres: str = Field(min_length=2, max_length=100)
    apellidos: str = Field(min_length=2, max_length=100)
    tipo_documento: str | None = Field(default=None, max_length=100)
    fecha_nacimiento: date | None = None
    telefono: str | None = Field(default=None, max_length=30)
    departamento: str | None = Field(default=None, max_length=100)
    ciudad: str | None = Field(default=None, max_length=100)
    zona: str | None = Field(default=None, max_length=20)
    documento: str = Field(min_length=5, max_length=30)
    correo: EmailStr
    password: str = Field(min_length=8, max_length=72)

    @field_validator("password")
    @classmethod
    def validar_longitud_bcrypt(cls, password: str) -> str:
        if len(password.encode("utf-8")) > 72:
            raise ValueError("La contraseña no puede superar 72 bytes.")
        return password


class PacienteRegistrado(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombres: str
    apellidos: str
    documento: str


class UsuarioRegistrado(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    correo: EmailStr
    rol: str


class RegistroRespuesta(BaseModel):
    mensaje: str
    usuario: UsuarioRegistrado
    paciente: PacienteRegistrado