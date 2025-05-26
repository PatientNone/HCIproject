# Import required libraries
import streamlit as st      # Web app framework
import pandas as pd         # For working with tabular data
import time                 # To track time durations
import os                   # For file and folder handling

# Create folder called data in the main project folder if one does not already exist
DATA_FOLDER = "data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# Define file paths for CSV Outputs
# Each CSV file relates to their respective part of the usability testing workflow
CONSENT_CSV = os.path.join(DATA_FOLDER, "consent_data.csv")
DEMOGRAPHIC_CSV = os.path.join(DATA_FOLDER, "demographic_data.csv")
TASK_CSV = os.path.join(DATA_FOLDER, "task_data.csv")
EXIT_CSV = os.path.join(DATA_FOLDER, "exit_data.csv")

# Save dictionary data to CSV file
def save_to_csv(data_dict, csv_file):
    # Convert dictionary to Pandas DataFrame and save to CSV file
    df_new = pd.DataFrame([data_dict])
    if not os.path.isfile(csv_file):
        # Create file with headers if it does not already exist
        df_new.to_csv(csv_file, mode='w', header=True, index=False)
    else:
        # Otherwise add row without headers
        df_new.to_csv(csv_file, mode='a', header=False, index=False)

# Load existing data from CSV file for reporting
def load_from_csv(csv_file):
    # Load data from CSV file into a Pandas DataFrame and return it
    if os.path.isfile(csv_file):
        return pd.read_csv(csv_file)
    else:
        # Return empty DataFrame if file does not exist
        return pd.DataFrame()

# Define Streamlit user interface elements and functions
def main():
    st.title("Usability Testing Tool")
    # Create tabs for each section of the test
    home, consent, demographics, tasks, exit, report = st.tabs([
        "Home", "Consent", "Demographics", "Task", "Exit Questionnaire", "Report"
    ])

# Functions defined separately for each section called from main

    with home:
        st.subheader("Welcome to Human Computer Interaction Testing")
        st.write("""
        The Usability Testing Tool seeks to capture the users experience in evaluating specific tasks.
        
        Please complete each of the following steps to complete the process:
        1. Consent: Provide consent for data collection.
        2. Demographics: Fill out a short demographic questionnaire.
        3. Task: Complete a task from the list of available tasks.
        4. Exit Questionnaire: Answer a short questionnaire about your user experience. 
        5. Report: View a summary report.
        """)

    with consent:
        st.header("Consent Form")
        st.write("Please read and accept the terms listed below to participate in this user "
                 "experience testing.")

        # Insert scrolling text box
        st.text_area("Consent Terms:",
        "By participating, you agree to allow your responses to be recorded and used for research "
        "and improvement purposes. You understand that you will be asked to complete specific tasks "
        "as a part of this evaluation.\n"
        "\n"
        "The data collected during this session including task performance, feedback, and demographic "
        "information will be used solely for research and analysis to improve the user's experience "
        "with the application.\n"
        "\n"
        "All data will be kept confidential and will not be used for any purpose other than research "
        "and product improvement. Your participation is voluntary and you may withdraw at any time.\n")

        consent_given = st.checkbox("I have read, understand, and agree to the terms listed above.")
        if st.button("Submit Consent"):
            if not consent_given:
                st.warning("Please check the box acknowledging your understanding and agreement to the Consent Terms.")
            else:
                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "consent_given": consent_given
                }
                save_to_csv(data_dict, CONSENT_CSV)
                st.success("Consent recorded.")

    with demographics:
        st.header("Demographic Questionnaire")

        with st.form("demographic_form"):
            name = st.text_input("Name")
            gender = st.radio("Gender", ["Male", "Female", "Other", "Prefer not to say"])
            education = st.radio("Education Level", ["High School or equivalent", "Some College",
                                                     "Associate's Degree", "Bachelor's Degree",
                                                     "Graduate Degree", "Professional Degree or PhD", "Other"])
            occupation = st.text_input("Enter your occupation:")
            income = st.radio("Annual Income", ["\$0 - $25,000", "\$25,000 - $50,000", "\$50,000 - $75,000",
                                                "\$75,000 - $100,000", "\$100,000 - $150,000",
                                                "\$150,000 - $250,000", "\$250,000 +","Prefer not to say"])
            ethnicity = st.radio("How would you best describe yourself?", ["African", "African American",
                                                     "American Indian or Alaska Native", "East Asian",
                                                     "Central American", "European", "Hawaii Native or Other "
                                                     "Pacific Islander", "Hispanic or Latin American", "Middle Eastern",
                                                     "North American", "South Asian", "Southeast Asian", "Other"])
            age = st.radio("Age Range",
                           ["Under 18", "18 - 24", "25 - 34", "35 - 44", "45 - 54", "55 - 64", "65 and above",
                            "Prefer not to say"])
            familiarity = st.selectbox("How familiar are you with similar tools?",
                                       ["Very familiar", "Somewhat familiar", "Not at all familiar"])

            submitted = st.form_submit_button("Submit Demographics")
            if submitted:
                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "name": name,
                    "gender": gender,
                    "education": education,
                    "occupation": occupation,
                    "income": income,
                    "ethnicity": ethnicity,
                    "age": age,
                    "familiarity": familiarity,
                }
                save_to_csv(data_dict, DEMOGRAPHIC_CSV)
                st.success("Demographics saved.")

    with tasks:
        st.header("Task Page")
        st.write("Please select a task and record your experience completing it.")

        # Task selection placeholder
        selected_task = st.selectbox("Select Task", ["Task 1: Example Task"])
        st.write("Task Description: Perform the example task in our system...")

        # Timer logic
        if st.button("Start Task Timer"):
            st.session_state["start_time"] = time.time()

        if st.button("Stop Task Timer") and "start_time" in st.session_state:
            duration = time.time() - st.session_state["start_time"]
            st.session_state["task_duration"] = duration

        # Capture results
        success = st.radio("Were you able to complete the task successfully?", ["Yes", "No", "Partial"])
        notes = st.text_area("Observer Notes")

        if st.button("Save Task Results"):
            duration_val = st.session_state.get("task_duration", None)
            data_dict = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "task_name": selected_task,
                "success": success,
                "duration_seconds": duration_val if duration_val else "",
                "notes": notes
            }
            save_to_csv(data_dict, TASK_CSV)

            # Clear timers
            if "start_time" in st.session_state: del st.session_state["start_time"]
            if "task_duration" in st.session_state: del st.session_state["task_duration"]
            st.success("Task results saved.")

    with (exit):
        st.header("Exit Questionnaire")
        st.subheader("Please provide feedback on your experience. Your time and consideration is greatly appreciated.")
        with st.form("exit_form"):
            satisfaction = st.radio("Level of Satisfaction: \n"
                                    "\n"
                                    " --- How satisfied were you with performing the task?",
                                    ["1 - Very Dissatisfied", "2 - Dissatisfied", "3 - Unsure", "4 - Satisfied",
                                                              "5 - Very Satisfied"])
            difficulty = st.radio("Level of Difficulty: \n"
                                    "\n"
                                    " --- How difficult was it to complete the task?",
                                    ["1 - Very Difficult", "2 - Difficult", "3 - Not Difficult, But Not Easy",
                                     "4 - Easy", "5 - Very Easy"])
            confidence = st.radio("Level of Confidence: \n"
                                  "\n"
                                  " --- How confident were you in completing the task?",
                                  ["1 - Not At All Confident", "2 - A Little Confident", "3 - Somewhat Confident",
                                   "4 - Confident", "5 - Very Confident"])
            completion = st.text_input("If you were unable to complete the task, please explain what prevented "
                                       "you from doing so. What changes, if any, would you recommend to help "
                                       "improve the likelihood of task completion?")
            design = st.text_input("Did you find the design or presentation of the task to be clear?  Are there"
                                   "any changes about the design or presentation that you recommend making, "
                                   " to improve the user's experience with performing the task?")
            accessibility = st.text_input("What changes, if any, could be made to enhance accessibility and ease of use?")
            improvements = st.text_input("Do you have any recommendations for improvement?")
            open_feedback = st.text_area("Please provide any additional feedback, observations, or suggestions.")
            submitted_exit = st.form_submit_button("Submit Exit Questionnaire")
            if submitted_exit:
                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "satisfaction": satisfaction,
                    "difficulty": difficulty,
                    "confidence": confidence,
                    "completion": completion,
                    "design": design,
                    "accessibility": accessibility,
                    "improvements": improvements,
                    "open_feedback": open_feedback
                }
                save_to_csv(data_dict, EXIT_CSV)
                st.success("Exit questionnaire data saved.")

    with report:
        st.header("Usability Report - Summary of Results")

        st.write("### Consent Data")
        consent_df = load_from_csv(CONSENT_CSV)
        if not consent_df.empty:
            st.dataframe(consent_df)
            consent_summary = consent_df["consent_given"].value_counts()
            st.bar_chart(consent_summary)
        else:
            st.info("No consent data is available yet.")

        st.write("### Demographic Data")
        demographic_df = load_from_csv(DEMOGRAPHIC_CSV)
        if not demographic_df.empty:
            st.dataframe(demographic_df)
            st.write("**Age Distribution**")
            st.bar_chart(demographic_df["age"])
            st.write("**Familiarity**")
            familiarity_counts = demographic_df["familiarity"].value_counts()
            st.bar_chart(familiarity_counts)
        else:
            st.info("No demographic data is available yet.")

        st.write("### Task Performance Data")
        task_df = load_from_csv(TASK_CSV)
        if not task_df.empty:
            st.dataframe(task_df)
            st.write("**Success Rate**")
            success_counts = task_df["success"].value_counts()
            st.bar_chart(success_counts)
            if "duration_seconds" in task_df.columns:
                st.write("**Average Duration**")
                avg_duration = task_df["duration_seconds"].mean()
                st.metric("Average Task Duration (seconds)", f"{avg_duration:.2f}")
        else:
            st.info("No task data is available yet.")

        st.write("### Exit Questionnaire Data")
        exit_df = load_from_csv(EXIT_CSV)
        if not exit_df.empty:
            st.dataframe(exit_df)

            # Convert satisfaction, difficulty, confidence to numeric (by extracting leading number)
            exit_df["satisfaction_numeric"] = exit_df["satisfaction"].str.extract(r"(\d+)").astype(float)
            exit_df["difficulty_numeric"] = exit_df["difficulty"].str.extract(r"(\d+)").astype(float)
            exit_df["confidence_numeric"] = exit_df["confidence"].str.extract(r"(\d+)").astype(float)

            # Display charts for numeric values
            st.write("**Satisfaction, Difficulty and Confidence Scores**")
            st.bar_chart(exit_df[["satisfaction_numeric", "difficulty_numeric", "confidence_numeric"]])

            # Compute and display averages
            avg_satisfaction = exit_df["satisfaction_numeric"].mean()
            avg_difficulty = exit_df["difficulty_numeric"].mean()
            avg_confidence = exit_df["confidence_numeric"].mean()

            st.metric("Average Level of Satisfaction", f"{avg_satisfaction:.2f}")
            st.metric("Average Level of Difficulty", f"{avg_difficulty:.2f}")
            st.metric("Average Level of Confidence", f"{avg_confidence:.2f}")

            st.subheader("Exit Questionnaire Averages")

            # Ordering data
            education_order = [
                "High School or equivalent",
                "Some College",
                "Associate's Degree",
                "Bachelor's Degree",
                "Graduate Degree",
                "Professional Degree or PhD",
                "Other"
            ]

            age_order = [
                "Under 18",
                "18 - 24",
                "25 - 34",
                "35 - 44",
                "45 - 54",
                "55 - 64",
                "65 and above"
            ]

            gender_counts = demographic_df["gender"].value_counts()
            age_counts = demographic_df["age"].value_counts().reindex(age_order)
            education_counts = demographic_df["education"].value_counts().reindex(education_order)
            task_success_counts = task_df["success"].value_counts()

            merge_demo_exit = pd.merge(exit_df, demographic_df, left_index=True, right_index=True)
            merge_demo_task = pd.merge(task_df, demographic_df, left_index=True, right_index=True)

            st.subheader("Breakdowns by Demographics")
            st.write(gender_counts)
            st.write(age_counts)
            st.write(education_counts)
            st.write(task_success_counts)

            st.subheader("Average Difficulty by Age Group")
            avg_difficulty_by_age = merge_demo_exit.groupby("age")["difficulty_numeric"].mean().reindex(age_order)
            st.bar_chart(avg_difficulty_by_age)

            st.subheader("Average Confidence by Gender")
            avg_confidence_by_gender = merge_demo_exit.groupby("gender")["confidence_numeric"].mean()
            st.bar_chart(avg_confidence_by_gender)

            st.subheader("Task Completion Breakdown by Education")
            success_by_education = merge_demo_task.groupby("education")["success"].value_counts().unstack(
                fill_value=0).reindex(education_order)
            st.dataframe(success_by_education)

            # Plot one of the success categories by education
            if "Yes" in success_by_education.columns:
                st.bar_chart(success_by_education["Yes"])


        else:
            st.info("No exit questionnaire data is available yet.")


# Run the application using Streamlit's run() function
# Start the Streamlit server and open the application in browser
if __name__ == "__main__":
    main()