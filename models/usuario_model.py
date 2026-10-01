from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    __table_args__ = (
        CheckConstraint(
            "rol IN ('nutricionista', 'administrador', 'paciente')",
            name="ck_usuarios_rol",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    paciente_id: Mapped[int | None] = mapped_column(
        ForeignKey("pacientes.id"),
        unique=True,
        nullable=True,
    )

    nombres: Mapped[str] = mapped_column(String(100), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(100), nullable=False)

    correo: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    rol: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="nutricionista",
        server_default="nutricionista",
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    paciente = relationship(
        "Paciente",
        back_populates="usuario",
        uselist=False,
    )