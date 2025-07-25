import pandas as pd
import os

def label_can_achieve_goal(row):
    saving_ratio = (row['income'] - row['expenses']) / (row['income'] + 1)
    has_savings = row['emergency_savings'] > 0.1 * row['income']
    not_too_much_debt = row['total_liability'] < 0.5 * row['assets']
    
    if saving_ratio >= 0.2 and has_savings and not_too_much_debt:
        return 1
    return 0

def append_to_dataset(financial_data, total_liability):
    from .models import Financial_goals  # make sure this import is correct

    csv_path = 'dataset.csv'

    # Get all goal types
    goals = Financial_goals.objects.filter(goals=financial_data)
    goal_types = ','.join([g.goal_type for g in goals])

    row = {
        'income': float(financial_data.income),
        'expenses': float(financial_data.expenses),
        'assets': float(financial_data.assets),
        'investment_risk': financial_data.investment_risk,
        'emergency_savings': float(financial_data.emergency_savings),
        'total_liability': float(total_liability),
        'goal_type': goal_types,
        'is_saving_enough': financial_data.is_saving_enough,
        'is_overspending': financial_data.is_overspending,
        'is_debt_hurting': financial_data.is_debt_hurting,
    }

    row['can_achieve_goal'] = label_can_achieve_goal(row)

    df = pd.DataFrame([row])

    if not os.path.exists(csv_path):
        df.to_csv(csv_path, index=False)
    else:
        df.to_csv(csv_path, mode='a', index=False, header=False)





import joblib
from sklearn.preprocessing import LabelEncoder
from .models import Finacial_statements, Financial_goals
from pathlib import Path
import json
from decimal import Decimal
# Load feature names used in training
     
def predict_and_generate_advice(statement_id):
    from decimal import Decimal
    from pathlib import Path
    import json
    import joblib
    import pandas as pd
    from .models import Finacial_statements, Financial_goals

    # Load the models
    BASE_DIR = Path(__file__).resolve().parent
    MODEL_DIR = BASE_DIR / 'model'

    feature_path = MODEL_DIR / 'features.json'
    if not feature_path.exists():
        raise FileNotFoundError("features.json not found. Please run train_model.py first.")

    with open(feature_path) as f:
        expected_features = json.load(f)

    saving_model = joblib.load(MODEL_DIR / 'saving_model.pkl')
    goal_model = joblib.load(MODEL_DIR / 'goal_model.pkl')

    # Get data from DB
    fs = Finacial_statements.objects.get(id=statement_id)
    goals = Financial_goals.objects.filter(goals=fs)
    goal_types = ','.join([g.goal_type for g in goals])

    goal_list = goal_types.split(',') if goal_types else []
    goal_one_hot = {f'goal_type_{g.strip()}': 1 for g in goal_list}

    all_possible_goals = ['investment', 'emergency', 'vacation', 'home', 'retirement']
    for g in all_possible_goals:
        goal_one_hot[f'goal_type_{g}'] = goal_one_hot.get(f'goal_type_{g}', 0)

    # Prepare input row
    from sklearn.preprocessing import LabelEncoder
    input_row = {
        'income': fs.income,
        'expenses': fs.expenses,
        'assets': fs.assets,
        'investment_risk': LabelEncoder().fit_transform([fs.investment_risk])[0],
        'emergency_savings': fs.emergency_savings,
        'total_liability': sum(l.amount for l in fs.liability_items.all()),
        'saving': fs.income - fs.expenses  # Required for rules using saving
    }
    input_row.update(goal_one_hot)

    input_df = pd.DataFrame([input_row])

    # Add any missing columns
    for col in expected_features:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[expected_features]

    # Predictions
    is_saving_enough = saving_model.predict(input_df)[0]
    can_achieve_goal = goal_model.predict(input_df)[0]

    # --- Structured Advice Format ---
    advice_list = []

    score = 0

    # Saving check
    if is_saving_enough:
        score += 20
    

    # Emergency fund
    if fs.emergency_savings >= Decimal(0.1) * fs.income:
        score += 20
    

    # Liabilities vs. assets
    if input_row['total_liability'] <= fs.assets:
        score += 20
    

    # Expenses vs. income
    if fs.expenses <= Decimal(0.8) * fs.income:
        score += 20
    

    # Goal prediction
    if can_achieve_goal:
        score += 20
    

    if not is_saving_enough:
        advice_list.append({
            "problem": "You are not saving enough.",
            "solution": "Aim to save at least 20% of your income every month. Set up automatic monthly transfers to a savings account."
        })

    if not can_achieve_goal:
        advice_list.append({
            "problem": "Your current financial habits might prevent you from reaching your goals.",
            "solution": "Consider adjusting your expenses, increasing your savings, or lowering debts."
        })

    if fs.expenses > Decimal('0.8') * fs.income:
        advice_list.append({
            "problem": "You're spending more than 80% of your income.",
            "solution": "Reduce discretionary spending like online shopping and subscriptions. Use budgeting apps like Walnut or YNAB."
        })

    if input_row['total_liability'] > fs.assets:
        advice_list.append({
            "problem": "Your liabilities are higher than your assets.",
            "solution": "Start paying off high-interest debts first. Use the debt snowball or avalanche method. Apps like Cred or Paytm can help."
        })

    if fs.emergency_savings < Decimal('0.1') * fs.income:
        advice_list.append({
            "problem": "Your emergency fund is too low.",
            "solution": "Set aside a fixed monthly amount until you save at least 3–6 months of expenses. Use liquid mutual funds like SBI Magnum InstaCash."
        })

    if fs.emergency_savings > Decimal('0.5') * fs.income and fs.assets < Decimal('0.2') * fs.income:
        advice_list.append({
            "problem": "You have excess emergency savings but low assets.",
            "solution": "Reallocate part of your emergency fund into fixed deposits, PPF, or safe debt mutual funds."
        })

    if fs.income > 100000 and input_row['saving'] < Decimal('0.1') * fs.income:
        advice_list.append({
            "problem": "You have a high income but low savings.",
            "solution": "Follow the 50-30-20 rule. Use auto-debit to a savings/investment account to enforce discipline."
        })

    if fs.emergency_savings > Decimal('0.2') * fs.income and fs.investment_risk in ["none", "low"]:
        advice_list.append({
            "problem": "You're saving well but not investing.",
            "solution": "Invest in safe options like:\n• Mutual Funds via Zerodha or Groww\n• PPF\n• ELSS\n• Large-cap index funds\n• Recurring Deposits"
        })

    if fs.assets > 100000 and fs.investment_risk == "low":
        advice_list.append({
            "problem": "You have high assets but a low-risk profile.",
            "solution": "Diversify into balanced mutual funds (HDFC Balanced), Gold ETFs, or REITs for passive income."
        })

    return {
        'is_saving_enough': bool(is_saving_enough),
        'can_achieve_goal': bool(can_achieve_goal),
        'advice': advice_list,
        'score_percentage': score
    }
