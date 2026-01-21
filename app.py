import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SkillBridge | Internship Matching",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- CUSTOM CSS (WHITE THEME) ----------------
st.markdown("""
<style>
/* Global */
html, body, [class*="css"] {
    background-color: #ffffff !important;
    color: #111827 !important;
}

/* Container */
.block-container {
    padding-top: 2rem;
    max-width: 800px;
}

/* Headings */
h1, h2, h3 {
    color: #111827 !important;
}

/* Inputs */
input, textarea {
    background-color: #f9fafb !important;
    color: #111827 !important;
    border-radius: 10px !important;
    border: 1px solid #d1d5db !important;
}

/* Buttons */
button {
    background: linear-gradient(90deg, #2563eb, #1d4ed8) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 10px 20px !important;
    border: none !important;
    font-weight: 600 !important;
}

/* Card */
.card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}

/* Result box */
.result {
    background: #ecfdf5;
    border-left: 6px solid #10b981;
    padding: 20px;
    border-radius: 14px;
    color: #065f46;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
st.session_state.setdefault("step", "login")
st.session_state.setdefault("student", {"name": "", "skills": []})
st.session_state.setdefault("company", {"name": "", "skills": []})

# ---------------- HEADER ----------------
st.markdown("## 🎓 SkillBridge")
st.caption("Skill-based Internship Matching for Tier-2 & Tier-3 Students")
st.divider()

# ---------------- LOGIN ----------------
if st.session_state.step == "login":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🔐 Login")

    st.text_input("Username")
    st.text_input("Password", type="password")

    if st.button("Login →"):
        st.session_state.step = "role"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- ROLE ----------------
elif st.session_state.step == "role":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Select Your Role")

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

# ---------------- STUDENT ----------------
elif st.session_state.step == "student":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Student Details")

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

# ---------------- COMPANY ----------------
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

# ---------------- RESULT ----------------
elif st.session_state.step == "result":
    st.subheader("📊 Match Analysis")

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
