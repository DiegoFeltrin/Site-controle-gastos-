from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

def ler_gastos():
    gastos = []
    try:
        if not os.path.exists("gastos.txt"):
            return gastos
            
        with open("gastos.txt", "r") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if not linha or ":" not in linha:
                    continue

                nome, valor = linha.split(":")
                gastos.append((nome, float(valor)))
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
    
    return gastos

@app.route("/", methods=["GET", "POST"])
def index():
    gastos = ler_gastos()
    total = sum(valor for _, valor in gastos)

    if request.method == "POST":
        nome = request.form["nome"]
        valor = request.form["valor"]

        if ":" in nome:
            return render_template(
                "index.html",
                gastos=gastos,
                total=total,
                erro="Boa tentativa mas ':' não passa aqui"
            )

        with open("gastos.txt", "a") as arquivo:
            arquivo.write(f"{nome}:{valor}\n")

        return redirect("/")

    return render_template("index.html", gastos=gastos, total=total)

@app.route("/delete/<int:id>")
def delete(id):
    gastos = ler_gastos()

    if 0 <= id < len(gastos):
        gastos.pop(id)

        with open("gastos.txt", "w") as arquivo:
            for nome, valor in gastos:
                arquivo.write(f"{nome}:{valor}\n")

    return redirect("/")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
