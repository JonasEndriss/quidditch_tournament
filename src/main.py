from src.ui.simulation_app import SimulationApp
import ttkbootstrap as ttk

if __name__ == "__main__":
    root = ttk.Window(themename="cosmo")
    app = SimulationApp(root)
    root.mainloop()