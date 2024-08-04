from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Define file paths for all CSV files
file_paths = [
    "data\FOOD-DATA-GROUP1.csv",
    "data\FOOD-DATA-GROUP2.csv",
    "data\FOOD-DATA-GROUP3.csv",
    "data\FOOD-DATA-GROUP4.csv",
    "data\FOOD-DATA-GROUP5.csv"
]

# Load and combine all CSV files
data_frames = [pd.read_csv(file_path) for file_path in file_paths]
df_combined = pd.concat(data_frames, ignore_index=True)
df_combined = df_combined.drop_duplicates().reset_index(drop=True)

# Create a list of food items for the dropdown
food_items = df_combined['food'].unique().tolist()

def calculate_nutrition(food_list):
    total_nutrition = {
        'Caloric Value': 0,
        'Fat': 0,
        'Saturated Fats': 0,
        'Monounsaturated Fats': 0,
        'Polyunsaturated Fats': 0,
        'Carbohydrates': 0,
        'Sugars': 0,
        'Protein': 0,
        'Dietary Fiber': 0,
        'Cholesterol': 0,
        'Sodium': 0,
        'Water': 0,
        'Vitamin A': 0,
        'Vitamin B1 (Thiamine)': 0,
        'Vitamin B11 (Folic Acid)': 0,
        'Vitamin B12': 0,
        'Vitamin B2 (Riboflavin)': 0,
        'Vitamin B3 (Niacin)': 0,
        'Vitamin B5 (Pantothenic Acid)': 0,
        'Vitamin B6': 0,
        'Vitamin C': 0,
        'Vitamin D': 0,
        'Vitamin E': 0,
        'Vitamin K': 0,
        'Calcium': 0,
        'Copper': 0,
        'Iron': 0,
        'Magnesium': 0,
        'Manganese': 0,
        'Phosphorus': 0,
        'Potassium': 0,
        'Selenium': 0,
        'Zinc': 0
    }

    for food, quantity in food_list:
        food_data = df_combined[df_combined['food'] == food]
        if not food_data.empty:
            food_data = food_data.iloc[0]
            for nutrient in total_nutrition.keys():
                if nutrient in food_data:
                    total_nutrition[nutrient] += (quantity / 100) * food_data[nutrient]

    return total_nutrition

@app.template_filter('enumerate')
def enumerate_filter(items):
    return enumerate(items)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        food_list = []
        for i in range(len(food_items)):
            food_name = request.form.get(f'food{i}')
            quantity = request.form.get(f'quantity{i}')
            if food_name and quantity:
                food_list.append((food_name, float(quantity)))
        
        # Calculate nutrition
        nutrition = calculate_nutrition(food_list)
        return render_template('result.html', nutrition=nutrition)
    
    return render_template('index.html', food_items=food_items)

if __name__ == '__main__':
    app.run(debug=True)
