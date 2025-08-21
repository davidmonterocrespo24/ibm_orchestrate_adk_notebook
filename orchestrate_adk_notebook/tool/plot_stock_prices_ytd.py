
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# 2. Importaciones para la funcionalidad de la herramienta
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from typing import List
import os


# 4. Definición de la segunda herramienta
@tool(
    name="plot_stock_prices_ytd",
    description="Lee un archivo CSV con datos de acciones y crea un gráfico de precios que guarda como PNG.",
    permission=ToolPermission.READ_ONLY
)
def plot_stock_prices_ytd(csv_file_path: str) -> str:
    """Lee datos de acciones desde un archivo CSV y grafica los cambios de precio YTD.

    Guarda el gráfico resultante en la ruta 'output_data/stock_price_ytd.png'.

    Args:
        csv_file_path (str): La ruta al archivo CSV que contiene los datos de las acciones.

    Returns:
        str: Un mensaje de confirmación con la ruta del archivo de imagen guardado.
    """
    try:
        data = pd.read_csv(csv_file_path, index_col='Date', parse_dates=True)
    except FileNotFoundError:
        return f"Error: Archivo no encontrado en {csv_file_path}."

    plt.figure(figsize=(10, 6))
    for column in data.columns:
        plt.plot(data.index, data[column], label=column)
    
    plt.title("Cambio de Precio de Acciones YTD")
    plt.xlabel("Fecha")
    plt.ylabel("Precio (USD)")
    plt.legend()
    plt.grid(True)
    
    plot_path = os.path.join(WORK_DIR, "stock_price_ytd.png")
    plt.savefig(plot_path)
    plt.close()
    
    return f"Gráfico guardado exitosamente en {plot_path}"
