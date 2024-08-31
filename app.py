from flask import Flask, request, render_template
app = Flask(__name__)

# Define emission factors (example values, replace with accurate data)
EMISSION_FACTORS = {
    "South Africa": {
        "Transportation": 0.18,  # kgCO2/km
        "Electricity": 0.94,  # kgCO2/kWh
        "Diet": 1.5,  # kgCO2/meal
        "Waste": 0.12  # kgCO2/kg
    },
    "Nigeria": {
        "Transportation": 0.12,  # kgCO2/km
        "Electricity": 0.5,  # kgCO2/kWh
        "Diet": 1.2,  # kgCO2/meal
        "Waste": 0.08  # kgCO2/kg
    },
    "Kenya": {
        "Transportation": 0.1,  # kgCO2/km
        "Electricity": 0.25,  # kgCO2/kWh
        "Diet": 1.0,  # kgCO2/meal
        "Waste": 0.05  # kgCO2/kg
    }
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        country = request.form['country']
        distance = float(request.form['distance'])
        electricity = float(request.form['electricity'])
        waste = float(request.form['waste'])
        meals = int(request.form['meals'])
        
        # Normalize inputs
        distance *= 365  # Convert daily distance to yearly
        electricity *= 12  # Convert monthly electricity to yearly
        meals *= 365  # Convert daily meals to yearly
        waste *= 52  # Convert weekly waste to yearly

        # Calculate carbon emissions
        factors = EMISSION_FACTORS[country]
        transportation_emissions = factors["Transportation"] * distance
        electricity_emissions = factors["Electricity"] * electricity
        diet_emissions = factors["Diet"] * meals
        waste_emissions = factors["Waste"] * waste

        # Convert emissions to tonnes and round off to 2 decimal points
        transportation_emissions = round(transportation_emissions / 1000, 2)
        electricity_emissions = round(electricity_emissions / 1000, 2)
        diet_emissions = round(diet_emissions / 1000, 2)
        waste_emissions = round(waste_emissions / 1000, 2)

        # Calculate total emissions
        total_emissions = round(
            transportation_emissions + electricity_emissions + diet_emissions + waste_emissions, 2
        )
        
        return render_template('results.html', 
                               transportation_emissions=transportation_emissions,
                               electricity_emissions=electricity_emissions,
                               diet_emissions=diet_emissions,
                               waste_emissions=waste_emissions,
                               total_emissions=total_emissions)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
