"""Reglas y almacenamiento de los préstamos de PrestaLab."""

import sqlite3
from datetime import date


class Prestamos:
    def __init__(self, conexion: sqlite3.Connection):
        if conexion.in_transaction:
            raise ValueError("Inicializa el registro antes de abrir una transacción.")
        self.conexion = conexion
        conexion.row_factory = sqlite3.Row
        conexion.execute("PRAGMA foreign_keys = ON")
        conexion.executescript(
            """
            CREATE TABLE IF NOT EXISTS equipos (
                codigo TEXT PRIMARY KEY,
                nombre TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS prestamos (
                id INTEGER PRIMARY KEY,
                equipo TEXT NOT NULL REFERENCES equipos(codigo),
                responsable TEXT NOT NULL,
                inicio TEXT NOT NULL,
                limite TEXT NOT NULL CHECK (limite >= inicio),
                devolucion TEXT CHECK (devolucion >= inicio)
            );

            CREATE UNIQUE INDEX IF NOT EXISTS prestamo_activo_por_equipo
                ON prestamos(equipo) WHERE devolucion IS NULL;
            """
        )

    def registrar(self, codigo: str, nombre: str) -> None:
        codigo = _texto(codigo, "código").upper()
        nombre = _texto(nombre, "nombre")
        with self.conexion:
            resultado = self.conexion.execute(
                "INSERT INTO equipos VALUES (?, ?) ON CONFLICT(codigo) DO NOTHING",
                (codigo, nombre),
            )
            if resultado.rowcount == 0:
                raise ValueError(f"El equipo {codigo} ya está registrado.")

    def prestar(self, codigo: str, responsable: str, inicio: date, limite: date) -> None:
        codigo = _texto(codigo, "código").upper()
        responsable = _texto(responsable, "responsable")
        if limite < inicio:
            raise ValueError("La fecha límite no puede ser anterior al inicio.")

        try:
            with self.conexion:
                self.conexion.execute(
                    """
                    INSERT INTO prestamos(equipo, responsable, inicio, limite)
                    VALUES (?, ?, ?, ?)
                    """,
                    (codigo, responsable, inicio.isoformat(), limite.isoformat()),
                )
        except sqlite3.IntegrityError as error:
            if error.sqlite_errorname == "SQLITE_CONSTRAINT_FOREIGNKEY":
                raise ValueError(f"El equipo {codigo} no está registrado.") from error
            if error.sqlite_errorname == "SQLITE_CONSTRAINT_UNIQUE":
                raise ValueError(f"El equipo {codigo} ya tiene un préstamo activo.") from error
            raise

    def devolver(self, codigo: str, fecha: date) -> None:
        codigo = _texto(codigo, "código").upper()
        dia = fecha.isoformat()
        with self.conexion:
            resultado = self.conexion.execute(
                """
                UPDATE prestamos SET devolucion = ?
                WHERE equipo = ? AND devolucion IS NULL AND inicio <= ?
                """,
                (dia, codigo, dia),
            )
            if resultado.rowcount == 1:
                return

            abierto = self.conexion.execute(
                "SELECT 1 FROM prestamos WHERE equipo = ? AND devolucion IS NULL",
                (codigo,),
            ).fetchone()
            if abierto:
                raise ValueError("La devolución no puede ser anterior al inicio.")
            raise ValueError(f"El equipo {codigo} no tiene un préstamo activo.")

    def listar(self, fecha: date) -> list[sqlite3.Row]:
        return self.conexion.execute(
            """
            SELECT equipo, responsable, limite,
                   CASE WHEN limite < ? THEN 'Vencido' ELSE 'Vigente' END AS estado
            FROM prestamos WHERE devolucion IS NULL
            ORDER BY limite, equipo
            """,
            (fecha.isoformat(),),
        ).fetchall()


def _texto(valor: str, campo: str) -> str:
    valor = valor.strip()
    if not valor:
        raise ValueError(f"El campo {campo} es obligatorio.")
    return valor
