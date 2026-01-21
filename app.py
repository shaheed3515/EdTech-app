import streamlit as st
import pandas as pd

# ---------- Page Config ----------
st.set_page_config(
    page_title="SkillBridge | EdTech Internship Platform",
    layout="centered"
)

# ---------- SAFE SESSION STATE INIT ----------
st.session_state.setdefault("step", "login")
st.session_state.setdefault("student", {"name": "", "skills": []})
st.session_state.setdefault("company", {"name": "", "skills": []})

# ---------- Title ----------
st.title("🎓 SkillBridge")
st.caption("Industry Internship Matching for Tier-2 & Tier-3 Students")
st.divider()

# ---------- LOGIN ----------
if st.session_state.step == "login":
    st.subheader("Login")

    st.text_input("Username")
    st.text_input("Password", type="password")

    if st.button("Login"):
        st.session_state.step = "role"
        st.rerun()

# ---------- ROLE ----------
elif st.session_state.step == "role":
    st.subheader("Select Role")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("👨‍🎓 Student"):
            st.session_state.step = "student"
            st.rerun()

    with col2:
        if st.button("🏢 Company"):
            st.session_state.step = "company"
            st.rerun()

# ---------- STUDENT ----------
elif st.session_state.step == "student":
    st.subheader("Student Details")

    name = st.text_input("Name")
    skills = st.text_input("Skills (e.g. python java sql)")

    if st.button("Next"):
        st.session_state.student["name"] = name
        st.session_state.student["skills"] = [
            s.strip().lower() for s in skills.replace(",", " ").split() if s.strip()
        ]
        st.session_state.step = "company"
        st.rerun()

# ---------- COMPANY ----------
elif st.session_state.step == "company":
    st.subheader("Company Details")

    cname = st.text_input("Company Name")
    cskills = st.text_input("Required Skills")

    if st.button("Match"):
        st.session_state.company["name"] = cname
        st.session_state.company["skills"] = [
            s.strip().lower() for s in cskills.replace(",", " ").split() if s.strip()
        ]
        st.session_state.step = "result"
        st.rerun()

# ---------- RESULT ----------
elif st.session_state.step == "result":
    st.subheader("📊 Matching Result")

    student_skills = st.session_state.student["skills"]
    company_skills = st.session_state.company["skills"]

    if not company_skills:
        st.error("No company skills provided.")
        st.stop()

    matched = [s for s in student_skills if s in company_skills]
    match_percent = int((len(matched) / len(company_skills)) * 100)

    st.markdown(f"""
**Company:** {st.session_state.company["name"]}  
**Matched Skills:** {", ".join(matched) if matched else "None"}  
**Match Percentage:** **{match_percent}%**
""")

    df = pd.DataFrame({
        "Category": ["Matched", "Missing"],
        "Count": [len(matched), len(company_skills) - len(matched)]
    })

    st.bar_chart(df.set_index("Category"))

    if st.button("🔄 Restart"):
        st.session_state.clear()
        st.rerun()
