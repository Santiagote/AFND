import tkinter as tk
from tkinter import messagebox

# ──────────────────────────────────────────────────────────
# CONFIGURACIÓN DE EJERCICIOS
# ──────────────────────────────────────────────────────────
EJERCICIOS = {
    "1": {
        "enunciado": "AFND: Construye un autómata que acepte cadenas que terminen en 1.",
        "tipo": "ARBOL", "alf": "01", "ini": "q0", "fin": ["q1"],
        "trans": {"q0": {"0": ["q0"], "1": ["q0", "q1"]}, "q1": {}}
    },
    "2": {
        "enunciado": "AFND: Construye un autómata que comience con 'a' y termine con 'b'.",
        "tipo": "ARBOL", "alf": "ab", "ini": "q0", "fin": ["q2"],
        "trans": {"q0": {"a": ["q1"]}, "q1": {"a": ["q1"], "b": ["q1", "q2"]}, "q2": {}}
    },
    "3": {
        "enunciado": "AFND: Construye un autómata que contenga la subcadena '00'.",
        "tipo": "ARBOL", "alf": "01", "ini": "q0", "fin": ["q2"],
        "trans": {"q0": {"0": ["q0", "q1"], "1": ["q0"]}, "q1": {"0": ["q2"]}, "q2": {"0": ["q2"], "1": ["q2"]}}
    },
    "4": {
        "enunciado": "AFND: La segunda letra es 'a' O la cadena termina en 'b'.",
        "tipo": "ARBOL", "alf": "ab", "ini": "q0", "fin": ["p2", "r2"],
        "trans": {
            "q0": {"a": ["p1", "r1"], "b": ["p1", "r1"]}, 
            "p1": {"a": ["p2"], "b": ["p1"]}, 
            "p2": {"a": ["p2"], "b": ["p2"]},
            "r1": {"a": ["r1"], "b": ["r1", "r2"]},
            "r2": {"a": ["r1"], "b": ["r2"]}
        }
    },
    "5": {
        "enunciado": "AFND: Construye un autómata que contenga la subcadena 'ab'.",
        "tipo": "ARBOL", "alf": "ab", "ini": "q0", "fin": ["q2"],
        "trans": {"q0": {"a": ["q0", "q1"], "b": ["q0"]}, "q1": {"b": ["q2"]}, "q2": {"a": ["q2"], "b": ["q2"]}}
    },
    "6": {
        "enunciado": "CONVERSIÓN AFD: Versión determinista del Ejercicio 2 (Empieza 'a', termina 'b').",
        "tipo": "DIAGRAMA", "alf": "ab", "ini": "q0", "fin": ["q2"],
        "pos": {"q0": (200, 200), "q1": (500, 200), "q2": (800, 200), "q_trap": (200, 450)},
        "trans": {
            "q0": {"a": "q1", "b": "q_trap"}, 
            "q1": {"a": "q1", "b": "q2"}, 
            "q2": {"a": "q1", "b": "q2"}, 
            "q_trap": {"a": "q_trap", "b": "q_trap"}
        }
    }
}

class SimuladorHibrido:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador AFND/AFD - Santiago")
        self.root.geometry("1100x850")
        
        header = tk.Frame(root, bg="#2c3e50", pady=10)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="Ejercicio:", fg="white", bg="#2c3e50", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)
        self.sel = tk.StringVar(value="1")
        menu = tk.OptionMenu(header, self.sel, *sorted(EJERCICIOS.keys(), key=int), command=self.limpiar)
        menu.pack(side=tk.LEFT)
        
        self.ent = tk.Entry(header, font=("Arial", 12), width=20)
        self.ent.pack(side=tk.LEFT, padx=10)
        self.ent.insert(0, "aaab")
        
        tk.Button(header, text="EJECUTAR", command=self.correr, bg="#27ae60", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)

        self.lbl_enun = tk.Label(root, text="", font=("Arial", 11, "italic"), bg="#ecf0f1", pady=10, wraplength=1000)
        self.lbl_enun.pack(fill=tk.X)

        self.canvas = tk.Canvas(root, bg="white", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.limpiar()

    def limpiar(self, *args):
        self.canvas.delete("all")
        ej = EJERCICIOS[self.sel.get()]
        self.lbl_enun.config(text=f"Objetivo: {ej['enunciado']}")
        if ej["tipo"] == "DIAGRAMA":
            self.dibujar_afd_base(None)

    def correr(self):
        self.canvas.delete("all")
        ej = EJERCICIOS[self.sel.get()]
        cadena = self.ent.get().strip()
        
        if any(c not in ej["alf"] for c in cadena):
            messagebox.showerror("Error", f"Símbolos no válidos")
            return

        if ej["tipo"] == "ARBOL":
            self.dibujar_arbol(cadena, 0, ej["ini"], 550, 50, 500, ej)
        else:
            self.animar_afd(cadena, 0, ej["ini"], ej)

    def dibujar_arbol(self, cadena, idx, estado, x, y, ancho, ej):
        r = 20
        es_fin = estado in ej["fin"]
        termino = (idx == len(cadena))
        color = "#d5f5e3" if (es_fin and termino) else "white"
        
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline="black", width=2)
        self.canvas.create_text(x, y, text=estado, font=("Arial", 9, "bold"))
        if es_fin: self.canvas.create_oval(x-16, y-16, x+16, y+16)

        if not termino:
            char = cadena[idx]
            destinos = ej["trans"].get(estado, {}).get(char, [])
            if not destinos:
                self.canvas.create_text(x, y+35, text="✘ muere", fill="red", font=("Arial", 8, "bold"))
                return
            
            ancho_hijo = ancho / len(destinos)
            start_x = x - (ancho/2) + (ancho_hijo/2)
            for i, d in enumerate(destinos):
                hx, hy = start_x + (i * ancho_hijo), y + 90
                self.canvas.create_line(x, y+r, hx, hy-r, arrow=tk.LAST, fill="#7f8c8d")
                self.canvas.create_text((x+hx)/2+12, (y+hy)/2, text=char, fill="#c0392b", font=("Arial", 10, "bold"))
                self.dibujar_arbol(cadena, idx+1, d, hx, hy, ancho_hijo, ej)
        else:
            txt = "ACEPTA ★" if es_fin else "RECHAZA ✗"
            self.canvas.create_text(x, y+35, text=txt, fill="#27ae60" if es_fin else "#e74c3c", font=("Arial", 9, "bold"))

    def dibujar_afd_base(self, estado_activo, ej=None):
        if not ej: ej = EJERCICIOS[self.sel.get()]
        
        # Guardamos qué transiciones ya dibujamos para evitar duplicar texto en bucles
        dibujados = set()

        for origen, transiciones in ej["trans"].items():
            for char, destino in transiciones.items():
                identificador = (origen, destino)
                if identificador in dibujados: continue
                
                x1, y1 = ej["pos"][origen]
                x2, y2 = ej["pos"][destino]
                color_f = "#34495e"
                
                # Para el dibujo, agrupamos letras si van al mismo destino
                letras = [c for c, d in transiciones.items() if d == destino]
                texto_flecha = ", ".join(letras)

                if origen == destino:
                    self.canvas.create_arc(x1-25, y1-60, x1+25, y1-15, start=0, extent=180, style=tk.ARC, outline=color_f)
                    self.canvas.create_text(x1, y1-65, text=texto_flecha, fill="red", font=("Arial", 10, "bold"))
                elif x1 < x2:
                    self.canvas.create_line(x1+30, y1, x2-30, y2, arrow=tk.LAST, fill=color_f)
                    self.canvas.create_text((x1+x2)/2, y1-15, text=texto_flecha, fill="red", font=("Arial", 10, "bold"))
                elif x1 > x2:
                    self.canvas.create_line(x1-30, y1+10, x2+30, y2+10, arrow=tk.LAST, fill=color_f, smooth=True)
                    self.canvas.create_text((x1+x2)/2, y1+25, text=texto_flecha, fill="red", font=("Arial", 10, "bold"))
                else:
                    self.canvas.create_line(x1, y1+30, x2, y2-30, arrow=tk.LAST, fill=color_f)
                    self.canvas.create_text(x1-15, (y1+y2)/2, text=texto_flecha, fill="red", font=("Arial", 10, "bold"))
                
                dibujados.add(identificador)

        for nombre, (x, y) in ej["pos"].items():
            bg = "#f1c40f" if nombre == estado_activo else "white"
            ancho_l = 4 if nombre == estado_activo else 1
            self.canvas.create_oval(x-30, y-30, x+30, y+30, fill=bg, outline="#2c3e50", width=ancho_l)
            self.canvas.create_text(x, y, text=nombre, font=("Arial", 10, "bold"))
            if nombre in ej["fin"]:
                self.canvas.create_oval(x-25, y-25, x+25, y+25, outline="#2c3e50")

    def animar_afd(self, cadena, idx, estado, ej):
        self.canvas.delete("all")
        self.dibujar_afd_base(estado, ej)
        
        if idx < len(cadena):
            char = cadena[idx]
            siguiente = ej["trans"][estado][char]
            self.root.after(600, lambda: self.ejecutar_transicion(cadena, idx, siguiente, ej))
        else:
            res = "ACEPTADA" if estado in ej["fin"] else "RECHAZADA"
            messagebox.showinfo("Resultado", f"Cadena {res}")

    def ejecutar_transicion(self, cadena, idx, siguiente, ej):
        self.canvas.delete("all")
        self.dibujar_afd_base(None, ej)
        self.root.after(400, lambda: self.animar_afd(cadena, idx + 1, siguiente, ej))

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorHibrido(root)
    root.mainloop()