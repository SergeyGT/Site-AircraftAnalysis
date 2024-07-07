from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sklearn.linear_model import LinearRegression
import pymysql
import numpy as np

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:7891230456A&s@127.0.0.1/aircraft_db'
app.config['SECRET_KEY'] = '2411'
db = SQLAlchemy(app)

class AircraftMaintenance(db.Model):
    __tablename__ = 'aircraftmaintenance'
    aircraft_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    maintenance_date = db.Column(db.Date, nullable=False)
    maintenance_type = db.Column(db.String(50), nullable=False)
    maintenance_description = db.Column(db.String(255))
    maintenance_cost = db.Column(db.DECIMAL(10, 2), nullable=False)

    def __repr__(self):
        return f"<AircraftMaintenance(aircraft_id={self.aircraft_id}, maintenance_date={self.maintenance_date}, maintenance_type={self.maintenance_type})>"


class MaintenanceModels(db.Model):
    __tablename__ = 'maintenancemodels'
    model_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_name = db.Column(db.String(100), nullable=False)
    model_description = db.Column(db.String(255))
    optimal_parameters = db.Column(db.Text)

    def __repr__(self):
        return f"<MaintenanceModels(model_id={self.model_id}, model_name={self.model_name})>"


class AnalysisReports(db.Model):
    __tablename__ = 'analysisreports'
    report_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircraft_maintenance.aircraft_id'))
    model_id = db.Column(db.Integer, db.ForeignKey('maintenance_models.model_id'))
    deviation_from_optimal = db.Column(db.String(255))
    trend_analysis = db.Column(db.Text)
    recommendations = db.Column(db.Text)

    def __repr__(self):
        return f"<AnalysisReports(report_id={self.report_id}, aircraft_id={self.aircraft_id}, model_id={self.model_id})>"



@app.route('/')
def home():
    return render_template('home.html')


@app.route('/calculation')
def calculate():
    models_data = MaintenanceModels.query.all()  # Получаем все модели обслуживания из базы данных
    return render_template('calculate.html', models=models_data)


@app.route('/verification')
def verificate():
    analysis_reports = AnalysisReports.query.all()
    # Создаем словарь, в котором ключами будут model_id, а значениями model_name
    model_names = {model.model_id: model.model_name for model in MaintenanceModels.query.all()}
    # Заменяем model_id на model_name в каждом отчете
    for report in analysis_reports:
        report.model_id = model_names.get(report.model_id, '')  # Получаем model_name по model_id
    return render_template('verificate.html', analysis_reports=analysis_reports)

@app.route('/reports', methods=['GET', 'POST'])
def reports():
    if request.method == 'POST':
        maintenance_type = request.form['maintenance_type']  # Получаем выбранный тип технического обслуживания
        # Получаем записи из базы данных, отфильтрованные по выбранному типу обслуживания
        maintenance_records = AircraftMaintenance.query.filter_by(maintenance_type=maintenance_type).all()
        return render_template('reports.html', maintenance_records=maintenance_records)

    return render_template('reports.html')


if __name__ == '__main__':
    print("Запуск сайта...")
    app.run()
    print("Завершение работы...")
