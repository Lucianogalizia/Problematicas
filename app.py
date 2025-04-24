import os
import logging
from flask import Flask, render_template, request
import pandas as pd

def create_app():
    app = Flask(__name__)
    app.logger.setLevel(logging.INFO)

    # Intento de carga del Excel
    try:
        df = pd.read_excel("datos_resumen.xlsx", engine="openpyxl")
        df["fecha"] = pd.to_datetime(df["date_ops_end"]).dt.date
        app.logger.info("✔️ Excel cargado correctamente: %d filas", len(df))
    except Exception as e:
        df = pd.DataFrame(columns=["POZO", "fecha", "problematicas_riesgos"])
        app.logger.exception("❌ Error cargando datos_resumen.xlsx")
    app.config["DF"] = df

    @app.route("/")
    def index():
        df = app.config["DF"]
        pozos = sorted(df["POZO"].unique())
        return render_template("index.html", pozos=pozos, resultados=None)

    @app.route("/buscar")
    def buscar():
        df = app.config["DF"]
        pozo = request.args.get("pozo")
        pozos = sorted(df["POZO"].unique())
        resultados = df[df["POZO"] == pozo][["fecha", "problematicas_riesgos"]]\
                      .to_dict(orient="records")
        return render_template(
            "index.html",
            pozos=pozos,
            resultados=resultados,
            seleccionado=pozo
        )

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

