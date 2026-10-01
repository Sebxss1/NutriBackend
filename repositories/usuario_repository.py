from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.paciente_model import Paciente
from models.usuario_model import Usuario


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, correo: str) -> Usuario | None:
        return self.db.scalar(
            select(Usuario).where(Usuario.correo == correo)
        )

    def get_patient_by_document(self, documento: str) -> Paciente | None:
        return self.db.scalar(
            select(Paciente).where(Paciente.documento == documento)
        )

    def create_patient_account(
            self,
            paciente: Paciente,
            usuario: Usuario,
    ) -> tuple[Usuario, Paciente]:
        try:
            self.db.add(paciente)
            self.db.flush()

            usuario.paciente_id = paciente.id
            self.db.add(usuario)

            self.db.commit()
            self.db.refresh(usuario)
            self.db.refresh(paciente)

            return usuario, paciente

        except IntegrityError:
            self.db.rollback()
            raise ValueError(
                "El correo o documento ya está registrado."
            )
        except Exception:
            self.db.rollback()
            raise