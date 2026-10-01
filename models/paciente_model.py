from datetime import date, datetime

from sqlalchemy import Date, DateTime, String, Integer, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from config.database import Base

class Paciente(Base):
    __tablename__ = "pacientes"


    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombres: Mapped[str] = mapped_column(String(100), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(100), nullable=False)
    tipo_documento: Mapped[str | None] = mapped_column(String(100))
    documento: Mapped[str] = mapped_column(String(30), unique=True, index=True, nullable=False)
    fecha_nacimiento: Mapped[date | None] = mapped_column(Date)
    telefono: Mapped[str | None] = mapped_column(String(30))
    correo: Mapped[str | None] = mapped_column(String(150))
    departamento: Mapped[str | None] = mapped_column(String(100))
    ciudad: Mapped[str | None] = mapped_column(String(100))
    zona: Mapped[str | None] = mapped_column(String(20))  # urbana o rural
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    usuario = relationship("Usuario", back_populates="paciente", uselist=False)