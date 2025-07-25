from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth.hashers import check_password
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from django.http import HttpResponse
import joblib



 
def index(request):
    if 'username' not in request.session:
        return render(request,'home.html')
    user = True
    context = {'name': user}
    response = render(request, 'home.html', context)
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response



def blog(request):
    return render(request,'blog.html')
 
def investor(request):
    return render(request,'investing insights.html')

def contact(request):
    return render(request,'contact.html')



def advisor(request):
    return render(request,'Aiadvisor.html')


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Replace 'success' with your actual success page
    else:
        form = RegistrationForm()
    
    return render(request, 'registration.html', {'form': form})

def login(request):
    if 'username' in request.session:
        return redirect('index')
    else:
        if request.method == 'POST':
            form = Loginform(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                try:
                    user = Customer.objects.get(name=username)
                except Customer.DoesNotExist:
                    return render(request, 'login.html', {
                        'form': form,
                        'error': 'Invalid username or password'
                    })

                if check_password(password, user.password):
                    # Set session
                    request.session['username'] = user.name
                    return redirect('index')
                else:
        
                    return render(request, 'login.html', {
                        'form': form,
                        'error': 'Invalid username or password'
                    })
                
        else:
            form = Loginform()
            response = render(request, 'login.html', {'form': form})
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response


def logout(request):
    request.session.pop('username')
    return redirect('index')

from .ml import append_to_dataset
from .train_model import train_model
# def submit_financial_form(request):
#     context = {}
#     if 'username' in request.session:
#         user = request.session['username']
#         customer = Customer.objects.get(name=user)  # fix this based on your model
#         custumer_finance = Finacial_statements.objects.get(name=customer)
#         print('the custumer is:',custumer_finance)
#         if request.method == 'POST':
#             form = FinancialStatementForm(request.POST)
#             liability_formset = LiabilityFormSet(request.POST)
#             goals_formset = FinancialGoalsFormSet(request.POST)

#             if form.is_valid() and liability_formset.is_valid() and goals_formset.is_valid():
#                 if not custumer_finance:
#                     # Save the main financial statement
#                     statement = form.save(commit=False)

#                     # Get the Customer instance (not a string)
#                     customer = Customer.objects.get(name=user)
#                     statement.name = customer  # Assign ForeignKey
#                     statement.save()  #  Save before using in related objects

#                     # Save related liabilities
#                     total_liability = 0
#                     for liability_form in liability_formset:
#                         if liability_form.cleaned_data and not liability_form.cleaned_data.get('DELETE', False):
#                             liability = liability_form.save(commit=False)
#                             liability.statement = statement
#                             liability.save()
#                             total_liability += liability.amount

#                     # Save related financial goals
#                     for goal_form in goals_formset:
#                         if goal_form.cleaned_data and not goal_form.cleaned_data.get('DELETE', False):
#                             goal = goal_form.save(commit=False)
#                             goal.goals = statement  #  Assuming `goals` is FK to `Finacial_statements`
#                             goal.save()

#                     # Optional: ML model training and dataset update
#                     train_model()
#                     append_to_dataset(statement, total_liability)

#                     return redirect('generate_financial_advice', statement_id=statement.id)
#                 else:
#                     context['show_alert'] = True
#                     return render(request, 'dia.html', {
#                         'form': form,
#                         'user': user,
#                         'liability_formset': liability_formset,
#                         'goals_formset': goals_formset,
#                     },context)
#         else:
#             form = FinancialStatementForm()
#             liability_formset = LiabilityFormSet(queryset=Liability.objects.none())
#             goals_formset = FinancialGoalsFormSet(queryset=Financial_goals.objects.none())

#         return render(request, 'dia.html', {
#             'form': form,
#             'user': user,
#             'liability_formset': liability_formset,
#             'goals_formset': goals_formset,
#         })
        
#     else:
#         user = False
#         return render(request, "dia.html", {'user': user,},context)

def submit_financial_form(request):
    context = {}
    if 'username' in request.session:
        user = request.session['username']
        try:
            customer = Customer.objects.get(name=user)
        except Customer.DoesNotExist:
            # show error if customer not found (optional)
            context['error_message'] = "Customer not found."
            return render(request, "dia.html", context)

        # Only check for duplicates on POST (i.e., when form is submitted)
        if request.method == 'POST':
            # 💡 Check if this user already submitted data
            if Finacial_statements.objects.filter(name=customer).exists():
                context['show_alert'] = True  # This triggers the JS alert in template
                context.update({
                    'form': FinancialStatementForm(),
                    'user': user,
                    'liability_formset': LiabilityFormSet(queryset=Liability.objects.none()),
                    'goals_formset': FinancialGoalsFormSet(queryset=Financial_goals.objects.none()),
                })
                return render(request, "dia.html", context)

            # Form submission logic (if not already submitted)
            form = FinancialStatementForm(request.POST)
            liability_formset = LiabilityFormSet(request.POST)
            goals_formset = FinancialGoalsFormSet(request.POST)

            if form.is_valid() and liability_formset.is_valid() and goals_formset.is_valid():
                statement = form.save(commit=False)
                statement.name = customer
                statement.save()

                total_liability = 0
                for liability_form in liability_formset:
                    if liability_form.cleaned_data and not liability_form.cleaned_data.get('DELETE', False):
                        liability = liability_form.save(commit=False)
                        liability.statement = statement
                        liability.save()
                        total_liability += liability.amount

                for goal_form in goals_formset:
                    if goal_form.cleaned_data and not goal_form.cleaned_data.get('DELETE', False):
                        goal = goal_form.save(commit=False)
                        goal.goals = statement
                        goal.save()

                train_model()
                append_to_dataset(statement, total_liability)

                return redirect('generate_financial_advice', statement_id=statement.id)
        else:
            # Initial GET: blank forms
            form = FinancialStatementForm()
            liability_formset = LiabilityFormSet(queryset=Liability.objects.none())
            goals_formset = FinancialGoalsFormSet(queryset=Financial_goals.objects.none())

        return render(request, 'dia.html', {
            'form': form,
            'user': user,
            'liability_formset': liability_formset,
            'goals_formset': goals_formset,
        })
    else:
        return render(request, "dia.html", {'user': False})


# training the model


# make prediction and advice
# from django.shortcuts import render, get_object_or_404
# def generate_financial_advice(request, statement_id):
#     model = joblib.load('saving_model.pkl')

#     fs = get_object_or_404(Finacial_statements, id=statement_id)
#     liabilities = Liability.objects.filter(statement=fs)
#     total_liability = sum([l.amount for l in liabilities])
#     goals = Financial_goals.objects.filter(goals=fs)
#     goals_list = [g.goal_type for g in goals]

#     income = float(fs.income)
#     expenses = float(fs.expenses)
#     total_liability = float(total_liability)

#     # Health score
#     total_points = 6
#     earned_points = 0
#     if income >= 20000: earned_points += 1
#     if fs.Saving_inuff == "yes": earned_points += 1
#     if fs.emergency_savings == "yes": earned_points += 1
#     if fs.is_overspending == "no": earned_points += 1
#     if total_liability <= income * 5: earned_points += 1
#     if fs.investement_risk in ["low", "medium"]: earned_points += 1
#     status_percent = int((earned_points / total_points) * 100)

#     # ML model prediction
#     input_data = pd.DataFrame([{
#         'income': income,
#         'expenses': expenses,
#         'assets': fs.assets,
#         'total_liability': total_liability
#     }])
#     input_data = pd.get_dummies(input_data)
#     expected_columns = model.feature_names_in_
#     for col in expected_columns:
#         if col not in input_data.columns:
#             input_data[col] = 0
#     input_data = input_data[expected_columns]
#     prediction = model.predict(input_data)[0]

#     # Prepare advice blocks
#     advice = []

#     if income < 20000:
#         advice.append({
#             "problem": "Your income is below ₹20,000.",
#             "why": "It limits your ability to save, invest, and manage financial goals.",
#             "solution": [
#                 "Track all income streams and try to reduce income leakage.",
#                 "Explore freelancing, gig work, or part-time jobs.",
#                 "Invest time in high-income skill development (e.g., tech, finance, marketing)."
#             ]
#         })

#     if expenses > income * 0.7:
#         advice.append({
#             "problem": "You’re spending more than 70% of your income.",
#             "why": "This reduces your savings and increases risk of financial instability.",
#             "solution": [
#                 "Track every weekly expense using an app or notebook.",
#                 "Categorize needs vs wants. Cut non-essentials by 10–20%.",
#                 "Follow the 50-30-20 rule: 50% needs, 30% wants, 20% savings."
#             ]
#         })

#     if total_liability > income * 5:
#         advice.append({
#             "problem": "Your liabilities are more than 5x your monthly income.",
#             "why": "This puts extreme pressure on your finances and increases debt burden.",
#             "solution": [
#                 "List all debts with interest rates and due dates.",
#                 "Use the avalanche (high interest first) or snowball (smallest first) repayment method.",
#                 "Avoid taking new credit until current debts are under control."
#             ]
#         })

#     if fs.Saving_inuff == "no":
#         advice.append({
#             "problem": "You’re not saving enough money.",
#             "why": "Without savings, even small emergencies can create financial stress.",
#             "solution": [
#                 "Start saving at least 10–20% of your income monthly.",
#                 "Use automated saving tools or recurring bank deposits.",
#                 "Build a savings target tied to each of your financial goals."
#             ]
#         })

#     if fs.emergency_savings == "no":
#         advice.append({
#             "problem": "You have no emergency savings.",
#             "why": "Without emergency funds, you risk falling into debt during crises.",
#             "solution": [
#                 "Build an emergency fund of 3–6 months of expenses.",
#                 "Start with ₹1000–2000/month in a separate bank account.",
#                 "Avoid using this fund for anything other than real emergencies."
#             ]
#         })

#     if fs.is_overspending == "yes":
#         advice.append({
#             "problem": "Overspending behavior detected.",
#             "why": "Chronic overspending leads to unnecessary debt and loss of wealth.",
#             "solution": [
#                 "Use spending limits for non-essentials (food, shopping).",
#                 "Review transactions weekly to identify and reduce patterns.",
#                 "Switch to cash or prepaid cards for better discipline."
#             ]
#         })

#     if fs.assets == "no assets":
#         advice.append({
#             "problem": "You currently have no assets.",
#             "why": "Assets help build wealth and provide financial security.",
#             "solution": [
#                 "Start small with digital gold, mutual funds, or fixed deposits.",
#                 "Learn basic personal finance and investing.",
#                 "Reinvest savings into productive, safe asset classes."
#             ]
#         })

#     if fs.investement_risk == "high":
#         advice.append({
#             "problem": "You have high-risk investments.",
#             "why": "This exposes your money to large losses if markets fluctuate.",
#             "solution": [
#                 "Review your investment portfolio with a financial advisor.",
#                 "Diversify into low-risk options like PPF, mutual funds, and NPS.",
#                 "Don’t invest in schemes you don’t fully understand."
#             ]
#         })

#     if "buy a house" in goals_list and fs.Saving_inuff == "no":
#         advice.append({
#             "problem": "Goal: Buy a house, but savings are insufficient.",
#             "why": "You may not meet this goal in time without disciplined saving.",
#             "solution": [
#                 "Open a separate SIP or RD focused on this goal.",
#                 "Estimate your target (e.g. ₹10L in 3 years), then divide monthly.",
#                 "Track progress every 3 months and adjust contributions."
#             ]
#         })

#     if "retirements" in goals_list and fs.age < 35:
#         advice.append({
#             "problem": "You have a retirement goal but haven't started early investments.",
#             "why": "Starting early gives you huge compounding benefits.",
#             "solution": [
#                 "Start with NPS or long-term equity mutual funds.",
#                 "Invest consistently, even if the amount is small.",
#                 "Reinvest returns to take full advantage of compounding."
#             ]
#         })

#     if prediction == "yes":
#         advice.append({
#             "problem": "AI predicts you’re under financial strain.",
#             "why": "Your overall financial pattern indicates stress or instability.",
#             "solution": [
#                 "Prioritize debt repayment and build savings.",
#                 "Avoid high-risk investments or big expenses for now.",
#                 "Follow structured goals for 3–6 months and reassess."
#             ]
#         })
#     else:
#         advice.append({
#             "problem": "AI predicts you're financially stable.",
#             "why": "Your current income, spending, and liability patterns are healthy.",
#             "solution": [
#                 "Maintain your habits: save regularly and avoid new debt.",
#                 "Review your insurance and retirement plan annually.",
#                 "Set new goals like travel fund, education, or wealth creation."
#             ]
#         })

#     #  Save advice to DB if not already saved
#     if not FinancialAdvice.objects.filter(statement=fs).exists():
#         for block in advice:
#             if isinstance(block, dict):
#                 FinancialAdvice.objects.create(
#                     user=fs.name,
#                     statement=fs,
#                     problem=block["problem"],
#                     why=block["why"],
#                     solution="\n".join(block["solution"])
#                 )

#     return render(request, 'Aiadvisor.html', {
#         'fs': fs,
#         'total_liability': total_liability,
#         'advice_blocks': advice,
#         'goals_list': goals_list,
#         'prediction': prediction,
#         'status_percent': status_percent
#     })
from django.shortcuts import get_object_or_404
from .ml import predict_and_generate_advice

def generate_financial_advice(request, statement_id):
    customer = request.session.get('username')
    fs = Finacial_statements.objects.get(id=statement_id)
    result = predict_and_generate_advice(statement_id)
    print("Logged in as:", request.user.username)

    #  Get the logged-in user's Customer object
    try:
        customer = Customer.objects.get(name=customer)
    except Customer.DoesNotExist:
        return HttpResponse("Customer not found", status=404)
    
    #  Save to FinancialAdvice using the Customer object
    FinancialAdvice.objects.create(
        user=customer,
        statement=fs,
        is_saving_enough=result['is_saving_enough'],
        can_achieve_goal=result['can_achieve_goal'],
        advice_text = "\n---\n".join([
            f" Problem:\n{item['problem']}\n Solution:\n{item['solution']}" for item in result['advice']
        ]),
        score=result['score_percentage']
    )
    score=result['score_percentage']
    circumference = 2 * 3.1416 * 54  # 2πr where r = 54
    dash_offset = circumference - (circumference * score / 100)
    
    return redirect('advice_history')
    # return render(request, 'Aiadvisor.html', {
    #     'fs': fs,
    #     'advice_list': result['advice'],
    #     'score': result['score_percentage'],
    #     'dash_offset': dash_offset,
    # })

# def advice_history(request):
#     user = request.session.get('username')

#     #  Get the logged-in user's Customer object
#     customer = get_object_or_404(Customer, name=user)


#     advice_list = FinancialAdvice.objects.filter(user=customer).first()
#     score=advice_list.score
#     circumference = 2 * 3.1416 * 54  # 2πr where r = 54
#     dash_offset = circumference - (circumference * score / 100)

#     return render(request, 'Aiadvisor.html', {
#         'advice_list': advice_list,
#         'dash_offset': dash_offset,
#     })

def parse_advice_string(raw_text):
    # Split by "---"
    chunks = raw_text.strip().split('---')
    advice_list = []

    for chunk in chunks:
        if "Problem:" in chunk and "Solution:" in chunk:
            problem_part = chunk.split("Solution:")[0].replace("Problem:", "").strip()
            solution_part = chunk.split("Solution:")[1].strip()
            advice_list.append({
                "problem": problem_part,
                "solution": solution_part
            })
    return advice_list


def advice_history(request):
    user = request.session.get('username')
    customer = get_object_or_404(Customer, name=user)

    advice_entries = FinancialAdvice.objects.filter(user=customer).order_by('-created_at')  # All advice history
    latest_advice = advice_entries.first()  # Get latest entry
    print('the user is here:',advice_entries)

    if latest_advice:
        parsed_advice = parse_advice_string(latest_advice.advice_text)
        score = latest_advice.score
    else:
        parsed_advice = []
        score = 0

    circumference = 2 * 3.1416 * 54
    dash_offset = circumference - (circumference * score / 100)

    return render(request, 'Aiadvisor.html', {
        'user':user,
        'parsed_advice': parsed_advice,
        'score': score,
        'dash_offset': dash_offset,
        'history': advice_entries,  # optional: pass full history if needed
    })
