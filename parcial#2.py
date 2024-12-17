from flask import Flask, jsonify
import pandas as pd


app = Flask(__name__)


def load_data():

    file_path = 'measles_vaccination_data.csv'
    df = pd.read_csv(file_path)


    df = df[df['Country Name'] == 'Panama']
    df = df[['Year', 'Value']]
    df = df.rename(columns={'Value': 'Vaccination Coverage'})

    return df


data = load_data()

@app.route('/')
def home():
    return jsonify({
        "message": "Bienvenido al API de vacunación contra el sarampión en Panamá",
        "endpoints": [
            {"route": "/data", "description": "Obtén todos los datos disponibles"},
            {"route": "/data/<year>", "description": "Obtén los datos de un año específico"}
        ]
    })

@app.route('/data', methods=['GET'])
def get_all_data():
    result = data.to_dict(orient='records')
    return jsonify(result)

@app.route('/data/<int:year>', methods=['GET'])
def get_data_by_year(year):
    result = data[data['Year'] == year]

    if result.empty:
        return jsonify({"error": "Datos no encontrados para el año especificado"}), 404

    return jsonify(result.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
