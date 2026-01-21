import streamlit as st
import pandas as pd

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="SkillBridge | Internship Matching",
    layout="centered"
)

# ---------- CUSTOM CSS (IMPORTANT FIX) ----------
st.markdown("""
<style>
body {
    background-color: #0f172a;
}
.block-container {
    padding-top: 2rem;
}
.card {
    background-color: #111827;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    margin-bottom: 20px;
}
.title {
    color: #e5e7eb;
    font-size: 32px;
    font-weight: 700;
}
.subtitle {
    color: #9ca3af;
    font-size: 16px;
}
.label {
    color: #e5e7eb;
    font-weight: 600;
}
.result {
    background-color: #022c22;
    border-left: 6px solid #10b981;
    padding: 20px;
    border-radius: 12px;
    color: #ecfdf5;
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
st.session_state.setdefault("step", "login")
st.session_state.setdefault("student", {"name": "", "skills": []})
st.session_state.setdefault("company", {"name": "", "skills": []})

# ---------- HEADER ----------
st.markdown("<div class='title'>🎓 SkillBridge</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Skill-based Internship Matching for Tier-2 & Tier-3 Students</div>", unsafe_allow_html=True)
st.divider()

# ---------- LOGIN ----------
if st.session_state.step == "login":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🔐 Login")

    st.text_input("Username")
    st.text_input("Password", type="password")

    if st.button("Login →"):
        st.session_state.step = "role"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- ROLE ----------
elif st.session_state.step == "role":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Choose Role")

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
    st.subheader("Student Profile")

    name = st.text_input("Student Name")
    skills = st.text_input("Skills (python java sql)")

    if st.button("Continue →"):
        st.session_state.student["name"] = name
        st.session_state.student["skills"] = [
            s.lower() for s in skills.replace(",", " ").split() if s
        ]
        st.session_state.step = "company"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- COMPANY ----------
elif st.session_state.step == "company":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Company Requirements")

    cname = st.text_input("Company Name")
    cskills = st.text_input("Required Skills")

    if st.button("Match Candidate"):
        st.session_state.company["name"] = cname
        st.session_state.company["skills"] = [
            s.lower() for s in cskills.replace(",", " ").split() if s
        ]
        st.session_state.step = "result"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- RESULT ----------
elif st.session_state.step == "result":
    st.subheader("📊 Match Result")

    student_skills = st.session_state.student["skills"]
    company_skills = st.session_state.company["skills"]

    matched = [s for s in student_skills if s in company_skills]
    percent = int((len(matched) / len(company_skills)) * 100) if company_skills else 0

    st.progress(percent / 100)

    st.markdown(f"""
    <div class="result">
        <b>Company:</b> {st.session_state.company["name"]}<br><br>
        <b>Matched Skills:</b> {", ".join(matched) if matched else "None"}<br><br>
        <b>Match Percentage:</b> {percent}%
    </div>
    """, unsafe_allow_html=True)

    df = pd.DataFrame({
        "Category": ["Matched", "Missing"],
        "Count": [len(matched), len(company_skills) - len(matched)]
    })
    st.bar_chart(df.set_index("Category"))

    if st.button("🔄 Start Again"):
        st.session_state.clear()
        st.rerun()
