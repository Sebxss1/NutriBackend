from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.paciente_model import Paciente
from models.usuario_model import Usuario
from repositories.usuario_repository import UsuarioRepository
from schemas.registro_schema import RegistroPaciente
from utils.seguridad import hash_password


class AuthService:
    def __init__(self, db: Session):
        self.usuario_repository = UsuarioRepository(db)

    def register(
            self,
            user_data: RegistroPaciente,
    ) -> tuple[Usuario, Paciente]:
        correo = str(user_data.correo).strip().lower()
        documento = user_data.documento.strip()

        if self.usuario_repository.get_by_email(correo):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Este correo ya está registrado.",
            )

        if self.usuario_repository.get_patient_by_document(documento):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Este documento ya está registrado.",
            )

        paciente = Paciente(
                nombres=user_data.nombres.strip(),
                apellidos=user_data.apellidos.strip(),
                tipo_documento=user_data.tipo_documento,
                documento=documento,
                fecha_nacimiento=user_data.fecha_nacimiento,
                telefono=user_data.telefono,
                correo=correo,
                departamento=user_data.departamento,
                ciudad=user_data.ciudad,
                zona=user_data.zona,
            )

        usuario = Usuario(
            nombres=user_data.nombres.strip(),
            apellidos=user_data.apellidos.strip(),
            correo=correo,
            password_hash=hash_password(user_data.password),
            rol="paciente",
            activo=True,
            paciente=paciente,
        )

        try:
            return self.usuario_repository.create_patient_account(
                paciente=paciente,
                usuario=usuario,
            )
        except ValueError as error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(error),
            ) from error