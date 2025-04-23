import os
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Carga el Excel una sola vez
df = pd.read_excel("datos_resumen.xlsx", engine="openpyxl")
df["fecha"] = pd.to_datetime(df["date_ops_end"]).dt.date

@app.route("/")
def index():
    pozos = sorted(df["POZO"].unique())
    return render_template("index.html", pozos=pozos, resultados=None)

@app.route("/buscar")
def buscar():
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
