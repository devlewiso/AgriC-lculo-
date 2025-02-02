"""
Calculadora Agrícola GTQ - Versión con Interfaz Gráfica

Para mejoras: devlewiso@gmail.com
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timedelta
from tkcalendar import DateEntry

class AgriculturaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora Agrícola GTQ - Maíz")
        self.geometry("900x600")
        self.configure(bg="#f0f0f0")
        
        # Datos del cultivo
        self.cultivo = {
            'requerimientos': {
                'agua': 5000,
                'fertilizante': {'germinacion': 80, 'crecimiento': 150, 'maduracion': 100},
                'semillas': 25000
            },
            'rendimiento': {
                'produccion': 10.5,
                'dias_cosecha': 120
            }
        }
        
        self._crear_widgets()
        self._configurar_estilos()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10, 'bold'))
        style.configure('Entrada.TEntry', padding=5)

    def _crear_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Sección de entrada de datos
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        ttk.Label(input_frame, text="🌾 DATOS DE ENTRADA", font=('Arial', 12, 'bold')).grid(row=0, column=0, pady=10)

        # Hectáreas
        ttk.Label(input_frame, text="Hectáreas:").grid(row=1, column=0, sticky=tk.W)
        self.hectareas = ttk.Entry(input_frame, style='Entrada.TEntry')
        self.hectareas.grid(row=2, column=0, pady=5)

        # Fase de cultivo
        ttk.Label(input_frame, text="Fase de crecimiento:").grid(row=3, column=0, sticky=tk.W)
        self.fase = ttk.Combobox(input_frame, values=["Germinacion", "Crecimiento", "Maduracion"])
        self.fase.grid(row=4, column=0, pady=5)

        # Costo semillas
        ttk.Label(input_frame, text="Costo por 1000 semillas (GTQ):").grid(row=5, column=0, sticky=tk.W)
        self.costo_semilla = ttk.Entry(input_frame, style='Entrada.TEntry')
        self.costo_semilla.grid(row=6, column=0, pady=5)

        # Precio mercado
        ttk.Label(input_frame, text="Precio por quintal (GTQ):").grid(row=7, column=0, sticky=tk.W)
        self.precio_quintal = ttk.Entry(input_frame, style='Entrada.TEntry')
        self.precio_quintal.grid(row=8, column=0, pady=5)

        # Fecha siembra
        ttk.Label(input_frame, text="Fecha de siembra:").grid(row=9, column=0, sticky=tk.W)
        self.fecha_siembra = DateEntry(input_frame, date_pattern='dd/mm/yyyy')
        self.fecha_siembra.grid(row=10, column=0, pady=5)

        # Botón de cálculo
        btn_calcular = ttk.Button(input_frame, text="📊 Calcular", command=self._calcular)
        btn_calcular.grid(row=11, column=0, pady=20)

        # Sección de resultados
        result_frame = ttk.Frame(main_frame)
        result_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        self.resultados = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, height=25, width=50)
        self.resultados.pack(fill=tk.BOTH, expand=True)

    def _calcular(self):
        try:
            # Obtener valores
            hectareas = float(self.hectareas.get())
            fase = self.fase.get().lower()
            costo_semilla = float(self.costo_semilla.get())
            precio_quintal = float(self.precio_quintal.get())
            fecha_siembra = self.fecha_siembra.get_date()

            # Validaciones
            if hectareas <= 0:
                raise ValueError("Las hectáreas deben ser mayores a 0")
            if fase not in ['germinacion', 'crecimiento', 'maduracion']:
                raise ValueError("Fase de crecimiento no válida")
            if any(x < 0 for x in [costo_semilla, precio_quintal]):
                raise ValueError("Los valores monetarios no pueden ser negativos")

            # Cálculos
            req = self.cultivo['requerimientos']
            rend = self.cultivo['rendimiento']
            
            agua_total = req['agua'] * hectareas
            fertilizante_total = req['fertilizante'][fase] * hectareas
            semillas_total = req['semillas'] * hectareas
            produccion_total = rend['produccion'] * hectareas
            ingreso_bruto = produccion_total * (precio_quintal * 10)
            costo_semillas_total = (semillas_total / 1000) * costo_semilla
            ganancia_neta = ingreso_bruto - costo_semillas_total
            fecha_cosecha = fecha_siembra + timedelta(days=rend['dias_cosecha'])

            # Mostrar resultados
            self._mostrar_resultados(
                hectareas, agua_total, fertilizante_total, semillas_total,
                fase, produccion_total, ingreso_bruto, costo_semillas_total,
                ganancia_neta, fecha_cosecha
            )

        except Exception as e:
            messagebox.showerror("Error", f"Datos incorrectos: {str(e)}")

    def _mostrar_resultados(self, hectareas, agua, fertilizante, semillas, fase,
                          produccion, ingreso, costo, ganancia, fecha):
        self.resultados.delete(1.0, tk.END)
        
        texto = f"""
        🌽 REQUERIMIENTOS PARA {hectareas} HA 🌽

        💧 Agua diaria: {agua:,.2f} litros
        🌱 Fertilizante ({fase.capitalize()}): {fertilizante:,.2f} kg
        🌾 Semillas necesarias: {semillas:,.0f} unidades

        📈 ANÁLISIS ECONÓMICO 📉

        🚜 Producción estimada: {produccion:,.1f} toneladas
        💵 Ingresos brutos: Q{ingreso:,.2f}
        💸 Costo semillas: Q{costo:,.2f}
        📉📈 Ganancia neta: Q{ganancia:,.2f}
        📅 Fecha cosecha: {fecha.strftime('%d/%m/%Y')}
        """

        if ganancia < 0:
            texto += "\n\n❌ ¡ALERTA! Proyecto con pérdidas"
        else:
            rentabilidad = (ganancia / costo) * 100 if costo != 0 else 0
            texto += f"\n\n✅ Rentabilidad: {rentabilidad:.1f}%"

        self.resultados.insert(tk.END, texto)
        self.resultados.tag_configure('center', justify='center')
        self.resultados.tag_add('center', 1.0, tk.END)

if __name__ == "__main__":
    app = AgriculturaApp()
    app.mainloop()