# finance_tools.py

# 1. Importaciones necesarias para las herramientas de Orchestrate
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# 2. Importaciones para la funcionalidad de la herramienta
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from typing import List
import os

# Es una buena práctica definir un directorio de trabajo
WORK_DIR = "output_data"
if not os.path.exists(WORK_DIR):
    os.makedirs(WORK_DIR)


# 3. Definición de la primera herramienta con el decorador y docstring correcto
@tool(
    name="get_and_save_stock_data",
    description="Obtiene datos de acciones YTD, calcula la ganancia, los guarda en un CSV y devuelve un resumen.",
    permission=ToolPermission.READ_ONLY
)
def get_and_save_stock_data(tickers: List[str]) -> str:
    """Obtiene datos de acciones de fin de día (Year-To-Date) para una lista de símbolos (tickers).

    La herramienta guarda los precios de cierre en un archivo CSV en 'output_data/stock_price_ytd.csv'
    y devuelve un resumen en texto con el porcentaje de ganancia YTD para cada acción.

    Args:
        tickers (List[str]): Una lista de símbolos de acciones, por ejemplo ['META', 'TSLA'].

    Returns:
        str: Un mensaje de confirmación con la ruta del archivo y el resumen del rendimiento.
    """
    today = datetime.now()
    start_of_year = datetime(today.year, 1, 1)
    
    data = yf.download(tickers, start=start_of_year, end=today)
    
    if data.empty:
        return "No se encontraron datos para los tickers proporcionados."

    file_path = os.path.join(WORK_DIR, "stock_price_ytd.csv")
    data['Close'].to_csv(file_path)

    summary = "Rendimiento en lo que va del año (YTD):\n"
    for ticker in tickers:
        start_price = data['Close'][ticker].iloc[0]
        end_price = data['Close'][ticker].iloc[-1]
        gain_percent = ((end_price - start_price) / start_price) * 100
        summary += f"- {ticker}: {gain_percent:.2f}% de ganancia.\n"

    return f"Datos guardados exitosamente en {file_path}. {summary}"


# 5. Definición de la tercera herramienta
@tool(
    name="write_blog_post_from_data",
    description="Usa un resumen de rendimiento de acciones para escribir una breve entrada de blog.",
    permission=ToolPermission.READ_ONLY
)
def write_blog_post_from_data(summary: str) -> str:
    """Analiza un resumen de rendimiento de acciones y escribe una breve y atractiva entrada de blog.

    Args:
        summary (str): Un texto que resume el rendimiento de las acciones.

    Returns:
        str: El contenido de la entrada del blog en formato Markdown.
    """
    today_str = datetime.now().strftime("%B %d, %Y")
    
    blog_post = f"""
# Análisis de Acciones: Comparativa YTD

*Publicado el {today_str}*

El rendimiento del mercado tecnológico siempre ofrece una visión interesante. Basado en los datos más recientes, aquí hay un vistazo rápido al comportamiento de las acciones en lo que va del año.

**Resumen del Rendimiento:**

{summary}

Este análisis destaca las trayectorias actuales de estos gigantes tecnológicos.
"""
    return blog_post