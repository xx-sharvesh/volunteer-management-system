from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load data from Excel files for events, volunteers, and assignments
events_df = pd.read_excel('events.xlsx')
volunteers_df = pd.read_excel('volunteers.xlsx')
assignments_df = pd.read_excel('assignments.xlsx')

import pandas as pd

# Check if the DataFrame is empty
if events_df.empty:
    # Define the columns when creating the DataFrame
    events_df = pd.DataFrame(columns=['Event', 'Category', 'Date', 'Location'])

# Now you can add rows to the DataFrame
events_df.loc[len(events_df)] = ['event_name', 'event_category','event_date', 'event_location']

# Ensure defined columns for volunteers and assignments DataFrames
if volunteers_df.empty:
    volunteers_df = pd.DataFrame(columns=['Name', 'Interests', 'Availability'])

if assignments_df.empty:
    assignments_df = pd.DataFrame(columns=['Volunteer', 'Event'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events', methods=['GET', 'POST'])
def events():
    if request.method == 'POST':
        # Handle adding new event
        event_name = request.form['event_name']
        event_category = request.form['event_category']
        event_date = request.form['event_date']
        event_location = request.form['event_location']
        events_df.loc[len(events_df)] = [event_name, event_category, event_date, event_location]
        events_df.to_excel('events.xlsx', index=False)
    return render_template('events.html', events=events_df)

@app.route('/volunteers', methods=['GET', 'POST'])
def volunteers():
    if request.method == 'POST':
        # Handle adding new volunteer
        volunteer_name = request.form['volunteer_name']
        volunteer_interests = request.form['volunteer_interests']
        volunteer_availability = request.form.getlist('volunteer_availability')
        volunteers_df.loc[len(volunteers_df)] = [volunteer_name, volunteer_interests, volunteer_availability]
        volunteers_df.to_excel('volunteers.xlsx', index=False)
    return render_template('volunteers.html', volunteers=volunteers_df)

@app.route('/assignments', methods=['GET', 'POST'])
def assignments():
    if request.method == 'POST':
        # Handle assigning volunteer to event
        volunteer = request.form['volunteer']
        event = request.form['event']
        assignments_df.loc[len(assignments_df)] = [volunteer, event]
        assignments_df.to_excel('assignments.xlsx', index=False)
    return render_template('assignments.html', assignments=assignments_df, volunteers=volunteers_df, events=events_df)



if __name__ == '__main__':
    app.run(debug=True)
