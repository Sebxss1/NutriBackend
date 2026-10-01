from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.database import get_db
from schemas.registro_schema import RegistroPaciente, RegistroRespuesta
from services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post(
    "/registro",
    response_model=RegistroRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def registrar_paciente(
        datos: RegistroPaciente,
        db: Session = Depends(get_db),
):
    auth_service = AuthService(db)
    usuario, paciente = auth_service.register(datos)

    return {
        "mensaje": "Registro completado.",
        "usuario": usuario,
        "paciente": paciente,
    }