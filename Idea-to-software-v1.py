import streamlit as st
from io import BytesIO
import base64
from streamlit_ace import st_ace
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime

# Function to create download PDF link
def create_download_link_pdf(pdf_data, download_filename):
    b64 = base64.b64encode(pdf_data).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{download_filename}">Download PDF Specification</a>'
    return href

# Initialize session states
if 'project_list' not in st.session_state:
    st.session_state.project_list = []
if 'project_data' not in st.session_state:
    st.session_state.project_data = {}  # Main dict to store all info per project

# Main app layout
st.set_page_config(page_title="App Spec Builder", layout="centered")
st.title("🚀 App Specification & Requirements Builder")
st.markdown("Build professional, structured app specifications with features, user stories, tech stack, and more — then export as PDF.")

# Sidebar for project selection
with st.sidebar:
    st.header("Your Projects")
    project_name_input = st.text_input("New Project Name", placeholder="e.g., Fitness Tracker Pro")
    if st.button("Create New Project") and project_name_input.strip():
        project_id = project_name_input.strip()
        if project_id not in st.session_state.project_list:
            st.session_state.project_list.append(project_id)
            st.session_state.project_data[project_id] = {
                "overview": "", "target_audience": "", "core_features": [], "user_stories": [],
                "tech_stack": "", "non_functional": [], "api_integrations": [], "mockups_notes": "", "timeline": ""
            }
            st.success(f"Project '{project_id}' created!")
            st.rerun()

    if st.session_state.project_list:
        st.selectbox("Select Project to Edit", options=[""] + st.session_state.project_list, key="selected_project")

# Only show editor if a project is selected
if st.session_state.get("selected_project"):
    proj = st.session_state.selected_project
    data = st.session_state.project_data[proj]

    st.header(f"📱 Editing: **{proj}**")
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # 1. Project Overview
    st.subheader("1. Project Overview")
    data["overview"] = st.text_area("Brief description of the app", value=data["overview"], height=100,
                                    help="What problem does this app solve? What's the vision?")

    # 2. Target Audience
    st.subheader("2. Target Audience")
    data["target_audience"] = st.text_area("Who is this app for?", value=data["target_audience"], height=80,
                                           placeholder="e.g., Busy professionals aged 25-40, fitness enthusiasts, remote teams...")

    # 3. Core Features
    st.subheader("3. Core Features")
    feature_input = st.text_input("Add a new feature", key=f"feature_input_{proj}")
    if st.button("➕ Add Feature") and feature_input.strip():
        data["core_features"].append(feature_input.strip())
        st.rerun()

    if data["core_features"]:
        st.write("**Current Features:**")
        for i, feat in enumerate(data["core_features"]):
            col1, col2 = st.columns([6, 1])
            with col1:
                st.write(f"• {feat}")
            with col2:
                if st.button("✖", key=f"del_feat_{i}_{proj}"):
                    data["core_features"].pop(i)
                    st.rerun()

    # 4. User Stories
    st.subheader("4. User Stories (As a [user], I want [feature] so that [benefit])")
    story_input = st.text_area("Write a user story", height=80, key=f"story_input_{proj}")
    if st.button("➕ Add User Story") and story_input.strip():
        data["user_stories"].append(story_input.strip())
        st.rerun()

    if data["user_stories"]:
        for i, story in enumerate(data["user_stories"]):
            with st.expander(f"User Story {i+1}"):
                st.write(story)
                if st.button("Delete", key=f"del_story_{i}_{proj}"):
                    data["user_stories"].pop(i)
                    st.rerun()

    # 5. Technical Stack & Architecture
    st.subheader("5. Tech Stack & Architecture")
    data["tech_stack"] = st.text_area(
        "Recommended technologies (frontend, backend, database, hosting, etc.)",
        value=data["tech_stack"], height=150,
        placeholder="Frontend: React Native / Flutter\nBackend: Node.js + Express or Python + FastAPI\nDatabase: Firebase / PostgreSQL\nAuthentication: Firebase Auth / Supabase\nHosting: Vercel / AWS"
    )

    # 6. Non-Functional Requirements
    st.subheader("6. Non-Functional Requirements")
    nfr_options = [
        "Must support offline mode",
        "App size < 50MB",
        "Load time < 2s on 4G",
        "Support dark mode",
        "GDPR compliant",
        "Support 10,000 concurrent users",
        "99.9% uptime SLA",
        "Multi-language support (i18n)"
    ]
    selected_nfr = st.multiselect("Select or add custom NFRs", options=nfr_options + ["Custom..."], default=data["non_functional"])
    if "Custom..." in selected_nfr:
        custom = st.text_input("Enter custom non-functional requirement")
        if custom and st.button("Add Custom NFR"):
            data["non_functional"].append(custom)
            st.rerun()
    data["non_functional"] = [x for x in selected_nfr if x != "Custom..."]

    # 7. Third-Party APIs & Integrations
    st.subheader("7. Third-Party APIs & Integrations")
    api_input = st.text_input("Add integration (e.g., Stripe, Google Maps, OpenAI)", key="api_input")
    if st.button("➕ Add Integration") and api_input.strip():
        data["api_integrations"].append(api_input.strip())
        st.rerun()

    if data["api_integrations"]:
        for i, api in enumerate(data["api_integrations"]):
            col1, col2 = st.columns([5, 1])
            col1.write(f"🔗 {api}")
            if col2.button("Remove", key=f"del_api_{i}"):
                data["api_integrations"].pop(i)
                st.rerun()

    # 8. UI/UX Notes & Mockups
    st.subheader("8. UI/UX Notes & Mockup References")
    data["mockups_notes"] = st.text_area("Design style, color palette, inspiration, Figma links, etc.", value=data["mockups_notes"], height=100)

    # 9. Timeline & Milestones
    st.subheader("9. Estimated Timeline")
    data["timeline"] = st.text_area("MVP deadline, phases, milestones", value=data["timeline"], height=100,
                                    placeholder="MVP: 8 weeks\nPhase 1 (Core): 4 weeks\nPhase 2 (Social + Analytics): +3 weeks")

    # Generate PDF Button
    st.markdown("---")
    if st.button("🖨️ Generate PDF Specification Document", type="primary", use_container_width=True):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=50, rightMargin=50, topMargin=60, bottomMargin=60)
        styles = getSampleStyleSheet()
        story = []

        # Title
        story.append(Paragraph(f"<font size=18><b>{proj}</b></font>", styles['Title']))
        story.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
        story.append(Spacer(1, 20))

        # Overview
        story.append(Paragraph("1. Project Overview", styles['Heading2']))
        story.append(Paragraph(data["overview"] or "Not provided", styles['Normal']))
        story.append(Spacer(1, 12))

        # Target Audience
        story.append(Paragraph("2. Target Audience", styles['Heading2']))
        story.append(Paragraph(data["target_audience"] or "Not specified", styles['Normal']))
        story.append(Spacer(1, 12))

        # Core Features
        story.append(Paragraph("3. Core Features", styles['Heading2']))
        if data["core_features"]:
            feature_list = [ListItem(Paragraph(feat, styles['Normal'])) for feat in data["core_features"]]
            story.append(ListFlowable(feature_list, bulletType='bullet'))
        else:
            story.append(Paragraph("No features defined yet.", styles['Italic']))
        story.append(Spacer(1, 12))

        # User Stories
        story.append(Paragraph("4. User Stories", styles['Heading2']))
        if data["user_stories"]:
            for i, s in enumerate(data["user_stories"], 1):
                story.append(Paragraph(f"{i}. {s}", styles['Normal']))
                story.append(Spacer(1, 6))
        else:
            story.append(Paragraph("No user stories added.", styles['Italic']))
        story.append(Spacer(1, 12))

        # Tech Stack
        story.append(Paragraph("5. Tech Stack & Architecture", styles['Heading2']))
        story.append(Preformatted(data["tech_stack"] or "Not specified", ParagraphStyle('Code', fontName='Courier', fontSize=9)))
        story.append(Spacer(1, 12))

        # Non-functional
        story.append(Paragraph("6. Non-Functional Requirements", styles['Heading2']))
        if data["non_functional"]:
            nfr_list = [ListItem(Paragraph(nfr, styles['Normal'])) for nfr in data["non_functional"]]
            story.append(ListFlowable(nfr_list, bulletType='bullet'))
        story.append(Spacer(1, 12))

        # Integrations
        story.append(Paragraph("7. Third-Party APIs & Integrations", styles['Heading2']))
        if data["api_integrations"]:
            api_list = [ListItem(Paragraph(api, styles['Normal'])) for api in data["api_integrations"]]
            story.append(ListFlowable(api_list, bulletType='bullet'))
        story.append(Spacer(1, 12))

        # UI/UX
        story.append(Paragraph("8. UI/UX Notes", styles['Heading2']))
        story.append(Paragraph(data["mockups_notes"] or "No design notes provided.", styles['Normal']))
        story.append(Spacer(1, 12))

        # Timeline
        story.append(Paragraph("9. Timeline & Milestones", styles['Heading2']))
        story.append(Paragraph(data["timeline"] or "No timeline defined.", styles['Normal']))

        # Build PDF
        doc.build(story)
        pdf_data = buffer.getvalue()
        buffer.close()

        st.success("PDF Specification Generated Successfully!")
        st.markdown(create_download_link_pdf(pdf_data, f"{proj.replace(' ', '_')}_Spec_{datetime.now().strftime('%Y%m%d')}.pdf"), unsafe_allow_html=True)

else:
    st.info("👈 Create or select a project from the sidebar to start building your app specification.")
    st.markdown("""
    ### Perfect for:
    - Founders pitching to developers
    - Product managers writing PRDs
    - Freelancers scoping client projects
    - Teams aligning on MVP scope
    """)
