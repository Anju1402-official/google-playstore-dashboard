📱 Real-Time Google Play Store Data Dashboard
📌 Project Overview
This project is part of the NullClass Internship task — Build Real-Time Google Play Store Data Analytics (Python).
It visualizes Google Play Store app data using Streamlit and Plotly, applying the internship’s strict filtering rules, translations, and IST time-based display restrictions for each task.

🎯 Features & Tasks
Task 1: Grouped Bar Chart
Compares average rating and total reviews for the top 10 app categories (by installs).

Filters out:

Rating < 4.0

Size < 10MB

Last updated month ≠ January

Time restriction: Visible only between 3 PM and 5 PM IST.

Task 2: Choropleth Map
Displays global installs by category.

Shows only top 5 app categories with installs > 1 million.

Excludes categories starting with A, C, G, S.

Time restriction: Visible only between 6 PM and 8 PM IST.

Task 3: Dual-Axis Chart
Compares average installs and revenue for free vs paid apps.

Filters include:

Installs ≥ 10,000

Revenue ≥ $10,000

Android version > 4.0

Size > 15MB

Content rating = Everyone

App name length ≤ 30 characters

Shows only top 3 categories by installs.

Time restriction: Visible only between 1 PM and 2 PM IST.

Task 4: Time Series Trend
Displays total installs over time by category.

Highlights months with >20% growth.

Category translation:

Beauty → सौंदर्य (Hindi)

Business → வணிகம் (Tamil)

Dating → Verabredung (German)

Filters:

App name not starting with X, Y, Z

Category starting with E, C, or B

Reviews > 500

App name not containing "S"

Time restriction: Visible only between 6 PM and 9 PM IST.

Task 5: Bubble Chart
Shows relationship between app size and average rating.

Bubble size = Installs.

Filters:

Rating > 3.5

Category in: Game, Beauty, Business, Comics, Communication, Dating, Entertainment, Social, Event

Reviews > 500

No "S" in app name

Subjectivity > 0.5

Installs > 50,000

Game category highlighted in pink.

Translations same as Task 4.

Time restriction: Visible only between 5 PM and 7 PM IST.

📂 Dataset
Recommended dataset: Google Play Store Apps - Kaggle
This dataset contains categories, installs, ratings, and paid apps required for Task 3 and Task 5.

🛠 Installation & Setup
1️⃣ Clone the repository
bash
Copy
Edit
git clone https://github.com/yourusername/google-playstore-dashboard.git
cd google-playstore-dashboard
2️⃣ Install dependencies
bash
Copy
Edit
pip install streamlit pandas plotly numpy pytz
3️⃣ Run the Streamlit app
bash
Copy
Edit
streamlit run app.py
4️⃣ Upload dataset in dashboard
Upload the Kaggle CSV file via the uploader in the web UI.

📸 Example Output
Task 1: Grouped bar chart (3–5 PM IST only).

Task 2: Choropleth map (6–8 PM IST only).

Task 3: Dual-axis bar chart (1–2 PM IST only).

Task 4: Time series chart (6–9 PM IST only).

Task 5: Bubble chart (5–7 PM IST only).

📜 License
This project is for educational and internship evaluation purposes only.