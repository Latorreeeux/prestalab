"""Interfaz de consola del registro de préstamos."""

import argparse
import sqlite3
import sys
from contextlib import closing
from datetime import date

from prestamos import Prestamos


def fecha_iso(valor: str) -> date:
    try:
        fecha = date.fromisoformat(valor)
        if fecha.isoformat() == valor:
            return fecha
    except ValueError:
        pass
    raise argparse.ArgumentTypeError("Usa una fecha válida en formato AAAA-MM-DD.")


def argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Registro de préstamos de laboratorio.")
    parser.add_argument("--db", default="prestalab.sqlite3", help="Ruta de la base SQLite.")
    comandos = parser.add_subparsers(dest="accion", required=True)

    registrar = comandos.add_parser("registrar", help="Registra un equipo.")
    registrar.add_argument("codigo")
    registrar.add_argument("nombre")

    prestar = comandos.add_parser("prestar", help="Abre un préstamo.")
    prestar.add_argument("codigo")
    prestar.add_argument("responsable")
    prestar.add_argument("--hasta", required=True, type=fecha_iso)
    prestar.add_argument("--desde", type=fecha_iso, default=date.today())

    devolver = comandos.add_parser("devolver", help="Cierra un préstamo.")
    devolver.add_argument("codigo")
    devolver.add_argument("--fecha", type=fecha_iso, default=date.today())

    listar = comandos.add_parser("listar", help="Muestra los préstamos abiertos.")
    listar.add_argument("--fecha", type=fecha_iso, default=date.today())
    return parser.parse_args()


def main() -> int:
    args = argumentos()
    try:
        with closing(sqlite3.connect(args.db)) as conexion:
            registro = Prestamos(conexion)
            if args.accion == "registrar":
                registro.registrar(args.codigo, args.nombre)
                print("Equipo registrado.")
            elif args.accion == "prestar":
                registro.prestar(args.codigo, args.responsable, args.desde, args.hasta)
                print("Préstamo registrado.")
            elif args.accion == "devolver":
                registro.devolver(args.codigo, args.fecha)
                print("Devolución registrada.")
            else:
                prestamos = registro.listar(args.fecha)
                if not prestamos:
                    print("No hay préstamos activos.")
                else:
                    print("Equipo | Responsable | Límite | Estado")
                    for prestamo in prestamos:
                        print(" | ".join(prestamo))
    except (ValueError, sqlite3.OperationalError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
