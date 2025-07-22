import streamlit as st
import requests

# 🚩 Preloaded indications (editable list)
preloaded_indications = [
    "multiple sclerosis",
    "ALS",
    "Alzheimer's Disease",
    "Parkinson's Disease",
    "focal onset seizure",
    "dry eye disease",
    "geographic atrophy",
    "macular degeneration",
    "retinitis pigmentosa",
    "Rett syndrome",
    "migraine",
    "fibromyalgia",
    "major depression",
    "treatment resistant depression",
    "PTSD",
    "schizophrenia",
    "bipolar disorder",
    "Prader Willi syndrome",
    "Angelman's syndrome"
]

def fetch_trials(indication):
    """Fetch the 10 most recent trials for a given indication."""
    url = "https://clinicaltrials.gov/api/query/study_fields"
    params = {
        "expr": indication,
        "fields": "NCTId,BriefTitle,LeadSponsorName,OverallStatus,StartDate,CompletionDate,Phase",
        "min_rnk": 1,
        "max_rnk": 10,
        "fmt": "json"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()['StudyFieldsResponse']['StudyFields']
    else:
        return []

# Streamlit UI setup
st.set_page_config(page_title="Clinical Trials Dashboard", layout="wide")
st.title("🧪 Clinical Trials Dashboard")
st.markdown("Displays the **10 most recent trials ever** for each indication. You can also search for a new indication below.")

# 🔍 Search bar for dynamic indication lookup
search_indication = st.text_input("🔎 Search for a new indication (optional):")

if search_indication:
    st.subheader(f"Results for: {search_indication.title()}")
    trials = fetch_trials(search_indication)
    if trials:
        for trial in trials:
            nct_id = trial['NCTId'][0]
            title = trial['BriefTitle'][0]
            sponsor = trial.get('LeadSponsorName', ["N/A"])[0]
            status = trial.get('OverallStatus', ["N/A"])[0]
            start_date = trial.get('StartDate', ["N/A"])[0]
            completion_date = trial.get('CompletionDate', ["N/A"])[0]
            phase = trial.get('Phase', ["N/A"])[0]
            st.markdown(f"**[{nct_id}](https://clinicaltrials.gov/ct2/show/{nct_id})** – {title}")
            st.text(f"Sponsor: {sponsor} | Phase: {phase} | Status: {status} | Start: {start_date} | Expected Completion: {completion_date}")
            st.markdown("---")
    else:
        st.warning("No trials found for this indication or API error.")

st.markdown("---")

# 📋 Display preloaded indications as expandable panels
st.subheader("Preloaded Indications")
for indication in preloaded_indications:
    with st.expander(f"🔽 {indication.title()}"):
        trials = fetch_trials(indication)
        if trials:
            for trial in trials:
                nct_id = trial['NCTId'][0]
                title = trial['BriefTitle'][0]
                sponsor = trial.get('LeadSponsorName', ["N/A"])[0]
                status = trial.get('OverallStatus', ["N/A"])[0]
                start_date = trial.get('StartDate', ["N/A"])[0]
                completion_date = trial.get('CompletionDate', ["N/A"])[0]
                phase = trial.get('Phase', ["N/A"])[0]
                st.markdown(f"**[{nct_id}](https://clinicaltrials.gov/ct2/show/{nct_id})** – {title}")
                st.text(f"Sponsor: {sponsor} | Phase: {phase} | Status: {status} | Start: {start_date} | Expected Completion: {completion_date}")
                st.markdown("---")
        else:
            st.write("No trials found or API error.")
