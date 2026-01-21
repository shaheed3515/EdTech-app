import streamlit as st
import pandas as pd
import time

# ---------- Page Config ----------
st.set_page_config(
    page_title="SkillBridge | EdTech Internship Platform",
    layout="centered"
)

# ---------- Custom CSS ----------
st.markdown("""
<style>
body {
    background-color: #f9fafb;
}
.card {
    background-color: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.06);
    margin-bottom: 1rem;
}
.title {
    color: #1f2937;
}
.subtitle {
    color: #6b7280;
}
.success-box {
    background-color: #ecfdf5;
    padding: 1rem;
    border-radius: 10px;
    border-left: 5px solid #10b981;
}
</style>
""", unsafe_allow_html=True)

# ---------- SAFE SESSION STATE INIT ----------
st.session_state.setdefault("step", "login")
st.session_state.setdefault("student", {"name": "", "skills": []})
st.session_state.setdefault("company", {"name": "", "skills": []})

# ---------- Header ----------
st.markdown("<h1 class='title'>🎓 SkillBridge</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Skill-based Internship Matching for Tier-2 & Tier-3 Students</p>", unsafe_allow_html=True)
st.divider()

# ---------- LOGIN ----------
if st.session_state.step == "login":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🔐 Login")

    st.text_input("Username")
    st.text_input("Password", type="password")

    if st.button("Login ➜"):
        st.session_state.step = "role"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- ROLE ----------
elif st.session_state.step == "role":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("👤 Select Role")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("👨‍🎓 Student"):
            st.session_state.step = "student"
            st.rerun()

    with col2:
        if st.button("🏢 Company"):
            st.session_state.step = "company"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- STUDENT ----------
elif st.session_state.step == "student":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("👨‍🎓 Student Profile")

    name = st.text_input("Name")
    skills = st.text_input("Skills (python, java, sql)")

    if st.button("Continue ➜"):
        st.session_state.student["name"] = name
        st.session_state.student["skills"] = [
            s.strip().lower() for s in skills.replace(",", " ").split() if s.strip()
        ]
        st.session_state.step = "company"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- COMPANY ----------
elif st.session_state.step == "company":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🏢 Company Requirements")

    cname = st.text_input("Company Name")
    cskills = st.text_input("Required Skills")

    if st.button("🔍 Match Candidate"):
        st.session_state.company["name"] = cname
        st.session_state.company["skills"] = [
            s.strip().lower() for s in cskills.replace(",", " ").split() if s.strip()
        ]
        with st.spinner("Analyzing skill compatibility..."):
            time.sleep(1.2)
        st.session_state.step = "result"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- RESULT ----------
elif st.session_state.step == "result":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Match Analysis")

    student_skills = st.session_state.student["skills"]
    company_skills = st.session_state.company["skills"]

    matched = [s for s in student_skills if s in company_skills]
    match_percent = int((len(matched) / len(company_skills)) * 100) if company_skills else 0

    st.progress(match_percent / 100)

    st.markdown(f"""
<div class='success-box'>
<b>Company:</b> {st.session_state.company["name"]}<br>
<b>Matched Skills:</b> {", ".join(matched) if matched else "None"}<br>
<b>Match Percentage:</b> {match_percent}%
</div>
""", unsafe_allow_html=True)

    df = pd.DataFrame({
        "Category": ["Matched", "Missing"],
        "Count": [len(matched), len(company_skills) - len(matched)]
    })

    st.bar_chart(df.set_index("Category"))

    if st.button("🔄 Start New Match"):
        st.session_state.clear()
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Footer ----------
st.caption("🚀 Built for Hackathon | AI Assistant Coming Soon")
