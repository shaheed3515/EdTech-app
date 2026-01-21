import streamlit as st
import pandas as pd

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="SkillBridge | Internship Matching",
    layout="centered"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.main {
    background-color: #0e1117;
}
.card {
    background-color: #161b22;
    padding: 25px;
    border-radius: 14px;
    margin-bottom: 20px;
    border: 1px solid #2a2f3a;
}
.result-card {
    background-color: #0f2a1d;
    padding: 25px;
    border-radius: 14px;
    border-left: 6px solid #10b981;
}
h1, h2, h3 {
    color: white;
}
label, p {
    color: #c9d1d9;
}
.footer {
    text-align: center;
    color: #8b949e;
    font-size: 13px;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
st.session_state.setdefault("step", "login")
st.session_state.setdefault("student", {"name": "", "skills": []})
st.session_state.setdefault("company", {"name": "", "skills": []})

# ---------- HEADER ----------
st.title("🎓 SkillBridge")
st.caption("Skill-based Internship Matching for Tier-2 & Tier-3 Students")
st.divider()

# ---------- LOGIN ----------
if st.session_state.step == "login":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔐 Login")

    st.text_input("Username")
    st.text_input("Password", type="password")

    if st.button("Login →"):
        st.session_state.step = "role"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- ROLE ----------
elif st.session_state.step == "role":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("👥 Select Role")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("👨‍🎓 Student"):
            st.session_state.step = "student"
            st.rerun()
    with col2:
        if st.button("🏢 Company"):
            st.session_state.step = "company"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- STUDENT ----------
elif st.session_state.step == "student":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("👨‍🎓 Student Profile")

    name = st.text_input("Student Name")
    skills = st.text_input("Skills (example: python java sql)")

    if st.button("Continue →"):
        st.session_state.student["name"] = name
        st.session_state.student["skills"] = [
            s.strip().lower()
            for s in skills.replace(",", " ").split()
            if s.strip()
        ]
        st.session_state.step = "company"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- COMPANY ----------
elif st.session_state.step == "company":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🏢 Company Requirements")

    cname = st.text_input("Company Name")
    cskills = st.text_input("Required Skills")

    if st.button("Match Candidate →"):
        st.session_state.company["name"] = cname
        st.session_state.company["skills"] = [
            s.strip().lower()
            for s in cskills.replace(",", " ").split()
            if s.strip()
        ]
        st.session_state.step = "result"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- RESULT ----------
elif st.session_state.step == "result":
    student_skills = st.session_state.student["skills"]
    company_skills = st.session_state.company["skills"]

    matched = [s for s in student_skills if s in company_skills]
    match_percent = int((len(matched) / len(company_skills)) * 100) if company_skills else 0

    st.subheader("📊 Match Analysis")
    st.progress(match_percent / 100)

    st.markdown(f"""
<div class="result-card">
<h3>🏢 {st.session_state.company["name"]}</h3>
<p><b>Matched Skills:</b> {", ".join(matched) if matched else "None"}</p>
<p><b>Match Percentage:</b> {match_percent}%</p>
</div>
""", unsafe_allow_html=True)

    df = pd.DataFrame({
        "Category": ["Matched Skills", "Missing Skills"],
        "Count": [len(matched), len(company_skills) - len(matched)]
    })

    st.bar_chart(df.set_index("Category"))

    if st.button("🔄 Start Over"):
        st.session_state.clear()
        st.rerun()

# ---------- FOOTER ----------
st.markdown("""
<div class="footer">
🚀 Built for Hackathon | AI Career Assistant Coming Soon
</div>
""", unsafe_allow_html=True)
