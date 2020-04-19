from flask import Flask, render_template, Response, request, send_file, json, jsonify
from banzai_COVID19 import BanzaiCOVID19
import io
import yaml
import traceback

app = Flask(__name__)

try:
    with open ("config.yaml", "r") as file:
        config = yaml.safe_load(file)
except Exception as e:
    print('Error reading the config file')

@app.route("/", methods=["GET", "POST"])
def home():
    try:
        with open(config["files"]["dynamic_config"], "r") as dynamic_file:
             dynamic_config = yaml.safe_load(dynamic_file)

        default_days = dynamic_config["default"]["days"]
        default_countries = dynamic_config["default"]["countries"]
        default_is_log = dynamic_config["default"]["is_log"]
        default_is_death_rate = dynamic_config["default"]["is_death_rate"]
    except Exception as e:
        default_days = "25"
        default_countries = "brazil;italy;spain"
        default_is_log = "checked"
        default_is_death_rate = "checked"

    return render_template("covid19.html", default_days=default_days, default_countries=default_countries, default_is_log=default_is_log, default_is_death_rate=default_is_death_rate)

@app.route("/ux", methods=["GET", "POST"])
def ux():
    try:
        with open(config["files"]["dynamic_config"], "r") as dynamic_file:
             dynamic_config = yaml.safe_load(dynamic_file)

        default_days = dynamic_config["default"]["days"]
        default_countries = dynamic_config["default"]["countries"]
        default_is_log = dynamic_config["default"]["is_log"]
        default_is_death_rate = dynamic_config["default"]["is_death_rate"]
    except Exception as e:
        default_days = "25"
        default_countries = "brazil;italy;spain"
        default_is_log = "checked"
        default_is_death_rate = "checked"

    return render_template("covid19UX.html", default_days=default_days, default_countries=default_countries, default_is_log=default_is_log, default_is_death_rate=default_is_death_rate)



@app.route("/chart.png", methods=["GET", "POST"])
def chart():
    try:
        days = request.args.get("d")
        s_countries = request.args.get("c")
        s_logy = request.args.get("l")
        s_death_rate = request.args.get("dr")
        log = False
        death_rate = False
        if s_logy == "True":
            log = True
        if s_death_rate =="True":
            death_rate = True

        analysis = BanzaiCOVID19()
        analysis.global_confirmed_deaths_path = config["files"]["covid19_deaths_global"]
        analysis.global_confirmed_cases_path = config["files"]["covid19_cases_global"]
        analysis.brazil_cases_path = config["files"]["covid19_cases_brazil"]
        analysis.brazil_deaths_path = config["files"]["covid19_cases_brazil"]
        analysis.countries_population_path = config["files"]["countries_population"]
        analysis.countries_lookup_path = config["files"]["countries_lookup"]

        countries = s_countries.split(";")
        countries = [string for string in countries if string != ""]

        countries = [x.lower() for x in countries]
        countries = [x.strip() for x in countries]
        img = analysis.get_figure_plot_deaths(countries, 1, days, log, death_rate)
        response = Response(img.getvalue(), mimetype='image/png')
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response
    except:
        response = send_file("static/donuts_error.JPG", mimetype='image/jpg')
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

@app.route("/api", methods=["GET", "POST"])
def api():
    try:
        days = request.args.get("d")
        s_countries = request.args.get("c")
        s_logy = request.args.get("l")
        s_death_rate = request.args.get("dr")
        log = False
        death_rate = False
        if s_logy == "True":
            log = True
        if s_death_rate =="True":
            death_rate = True

        analysis = BanzaiCOVID19()
        analysis.global_confirmed_deaths_path = config["files"]["covid19_deaths_global"]
        analysis.global_confirmed_cases_path = config["files"]["covid19_cases_global"]
        analysis.brazil_cases_path = config["files"]["covid19_cases_brazil"]
        analysis.brazil_deaths_path = config["files"]["covid19_cases_brazil"]
        analysis.countries_population_path = config["files"]["countries_population"]
        analysis.countries_lookup_path = config["files"]["countries_lookup"]

        countries = s_countries.split(";")
        countries = [string for string in countries if string != ""]

        countries = [x.lower() for x in countries]
        countries = [x.strip() for x in countries]
        img = analysis.get_json_gviz_deaths(countries, 1, days, log, death_rate)

        return jsonify(img)
    except Exception:
        err = traceback.format_exc()
        response = Response(err)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')