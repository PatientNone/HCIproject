# HCIproject

# Usability Testing Tool

A **Streamlit-based web application** designed to collect and report user experience data through structured usability testing. This tool captures participant consent, demographic information, task performance metrics, and exit feedback, and summarizes the data into visual reports.

---

## Features

- **Consent Form** — Ensures ethical participation by recording participant agreement.
- **Demographics** — Gathers user characteristics (e.g., age, education, familiarity with tools).
- **Task Evaluation** — Records task completion, time spent, success level, and observer notes.
- **Exit Questionnaire** — Captures post-task satisfaction, perceived difficulty, and user suggestions.
- **Dynamic Reports** — Aggregates and visualizes data using interactive charts and metrics.

---

## Getting Started

### Requirements
- Python 3.8+
- Streamlit
- Pandas


## CSV Outputs

Each submission writes data to a corresponding CSV:
- consent_data.csv — Consent checkbox and timestamp.
- demographic_data.csv — Name, age, gender, education, income, and more.
- task_data.csv — Task selection, timer duration, completion status, and notes.
- exit_data.csv — Feedback on satisfaction, difficulty, confidence, and open-ended suggestions.

##Sample Use Cases

- Academic research in Human-Computer Interaction
- Usability testing of digital tools or prototypes
- Pre- and post-evaluation for UX improvement projects
