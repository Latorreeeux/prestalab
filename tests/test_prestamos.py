import sqlite3
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

from prestamos import Prestamos


INICIO = date(2026, 11, 1)
LIMITE = date(2026, 11, 5)
DESPUES = date(2026, 11, 6)
PROYECTO = Path(__file__).resolve().parents[1]


class PruebasPrestamos(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.addCleanup(self.db.close)
        self.registro = Prestamos(self.db)
        self.registro.registrar(" osc-01 ", " Osciloscopio ")

    def test_registrar_normaliza_y_rechaza_duplicados(self):
        equipo = self.db.execute("SELECT * FROM equipos").fetchone()
        self.assertEqual(tuple(equipo), ("OSC-01", "Osciloscopio"))
        with self.assertRaisesRegex(ValueError, "ya está registrado"):
            self.registro.registrar("osc-01", "Otro equipo")

    def test_datos_obligatorios(self):
        with self.subTest("código"):
            with self.assertRaisesRegex(ValueError, "código"):
                self.registro.registrar(" ", "Multímetro")
        with self.subTest("nombre"):
            with self.assertRaisesRegex(ValueError, "nombre"):
                self.registro.registrar("M-01", " ")
        with self.subTest("responsable"):
            with self.assertRaisesRegex(ValueError, "responsable"):
                self.registro.prestar("OSC-01", " ", INICIO, LIMITE)

    def test_rechaza_equipo_inexistente(self):
        with self.subTest("conexión inicializada"):
            with self.assertRaisesRegex(ValueError, "no está registrado"):
                self.registro.prestar("X-00", "Ana", INICIO, LIMITE)
        with self.subTest("conexión con transacción previa"):
            db = sqlite3.connect(":memory:")
            self.addCleanup(db.close)
            db.execute("BEGIN")
            with self.assertRaisesRegex(ValueError, "antes de abrir una transacción"):
                Prestamos(db)
            self.assertTrue(db.in_transaction)

    def test_rechaza_segundo_prestamo_activo(self):
        self.registro.prestar("OSC-01", "Ana", INICIO, LIMITE)
        with self.assertRaisesRegex(ValueError, "ya tiene un préstamo activo"):
            self.registro.prestar("OSC-01", "Luis", LIMITE, DESPUES)
        self.assertEqual(len(self.registro.listar(LIMITE)), 1)

    def test_limite_debe_ser_igual_o_posterior_al_inicio(self):
        with self.assertRaisesRegex(ValueError, "anterior al inicio"):
            self.registro.prestar("OSC-01", "Ana", LIMITE, INICIO)
        self.registro.prestar("OSC-01", "Ana", LIMITE, LIMITE)
        self.assertEqual(len(self.registro.listar(LIMITE)), 1)

    def test_cambia_a_vencido_el_dia_siguiente(self):
        self.registro.prestar("OSC-01", "Ana", INICIO, LIMITE)
        self.assertEqual(self.registro.listar(LIMITE)[0]["estado"], "Vigente")
        self.assertEqual(self.registro.listar(DESPUES)[0]["estado"], "Vencido")

    def test_listar_ordena_por_fecha_y_codigo(self):
        self.registro.registrar("A-01", "Adaptador")
        self.registro.registrar("B-01", "Batería")
        self.registro.prestar("OSC-01", "Ana", INICIO, LIMITE)
        self.registro.prestar("B-01", "Luis", INICIO, INICIO)
        self.registro.prestar("A-01", "Eva", INICIO, LIMITE)
        self.assertEqual(
            [fila["equipo"] for fila in self.registro.listar(LIMITE)],
            ["B-01", "A-01", "OSC-01"],
        )

    def test_devolver_valida_la_fecha_y_conserva_el_historial(self):
        self.registro.prestar("OSC-01", "Ana", LIMITE, LIMITE)
        with self.assertRaisesRegex(ValueError, "anterior al inicio"):
            self.registro.devolver("OSC-01", INICIO)
        self.assertEqual(len(self.registro.listar(LIMITE)), 1)
        self.registro.devolver("osc-01", DESPUES)
        self.assertEqual(self.registro.listar(DESPUES), [])
        with self.assertRaisesRegex(ValueError, "no tiene un préstamo activo"):
            self.registro.devolver("OSC-01", DESPUES)
        self.registro.prestar("OSC-01", "Luis", DESPUES, DESPUES)
        registros = self.db.execute(
            "SELECT responsable, devolucion FROM prestamos ORDER BY id"
        ).fetchall()
        self.assertEqual([tuple(fila) for fila in registros], [("Ana", "2026-11-06"), ("Luis", None)])


class PruebasConsola(unittest.TestCase):
    def setUp(self):
        with tempfile.NamedTemporaryFile(suffix=".sqlite3", dir=PROYECTO, delete=False) as archivo:
            self.ruta_db = archivo.name
        self.addCleanup(Path(self.ruta_db).unlink, missing_ok=True)

    def ejecutar(self, *args):
        return subprocess.run(
            [
                sys.executable, "-B", "-X", "utf8", str(PROYECTO / "prestalab.py"),
                "--db", self.ruta_db, *args,
            ],
            capture_output=True,
            encoding="utf-8",
            timeout=10,
            check=False,
        )

    def test_recorrido_persistente_entre_procesos(self):
        pasos = [
            (("registrar", "M-01", "Multímetro"), "Equipo registrado"),
            (
                ("prestar", "M-01", "Ana", "--desde", "2026-11-01", "--hasta", "2026-11-05"),
                "Préstamo registrado",
            ),
            (("listar", "--fecha", "2026-11-06"), "M-01 | Ana | 2026-11-05 | Vencido"),
            (("devolver", "M-01", "--fecha", "2026-11-06"), "Devolución registrada"),
            (("listar", "--fecha", "2026-11-06"), "No hay préstamos activos"),
        ]
        for args, mensaje in pasos:
            with self.subTest(accion=args[0]):
                salida = self.ejecutar(*args)
                self.assertEqual(salida.returncode, 0, salida.stderr)
                self.assertIn(mensaje, salida.stdout)

    def test_reporta_error_de_negocio_y_de_formato(self):
        salida = self.ejecutar("devolver", "X-00", "--fecha", "2026-11-06")
        self.assertEqual(salida.returncode, 1)
        self.assertIn("no tiene un préstamo activo", salida.stderr)
        salida = self.ejecutar("listar", "--fecha", "20261106")
        self.assertEqual(salida.returncode, 2)
        self.assertIn("AAAA-MM-DD", salida.stderr)


if __name__ == "__main__":
    unittest.main()
