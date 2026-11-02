
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="PlacementIQ | Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background: #10101C;
    color: #F5F3FF;
}

[data-testid="stSidebar"] {
    background: #19182B;
    border-right: 1px solid #34304F;
}

[data-testid="stSidebar"] * {
    color: #EDEBFF;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: 1px;
}

.subtitle {
    color: #A5A0C8;
    font-size: 14px;
    margin-bottom: 25px;
}

.section-title {
    color: #F4F0FF;
    font-size: 21px;
    font-weight: 700;
    margin-top: 20px;
}

.metric-card {
    background: linear-gradient(135deg, #25223D, #1A1930);
    border: 1px solid #454065;
    border-radius: 15px;
    padding: 20px;
    min-height: 120px;
    box-shadow: 0 5px 20px #00000030;
}

.metric-label {
    color: #AAA5C7;
    font-size: 13px;
}

.metric-value {
    font-size: 29px;
    font-weight: 800;
    color: #FFFFFF;
    margin-top: 10px;
}

.metric-note {
    color: #54E5D2;
    font-size: 12px;
    margin-top: 5px;
}

.stButton>button {
    background: linear-gradient(90deg, #8B5CF6, #EC4899);
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: bold;
}

.stDownloadButton>button {
    background: #25223D;
    color: #54E5D2;
    border: 1px solid #54E5D2;
    border-radius: 9px;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #454065;
    border-radius: 10px;
}

hr {
    border-color: #34304F;
}
</style>
""", unsafe_allow_html=True)

# ---------------- DATASET ----------------
data = {
    "Student": [
        "Amit", "Priya", "Rahul", "Sneha", "Rohit",
        "Neha", "Akash", "Pooja", "Karan", "Riya",
        "Sahil", "Anjali", "Om", "Sakshi", "Vikas",
        "Isha", "Arjun", "Meera", "Dev", "Kavya"
    ],
    "Department": [
        "CSE", "IT", "CSE", "ENTC", "IT",
        "CSE", "Mechanical", "IT", "CSE", "ENTC",
        "Mechanical", "CSE", "IT", "ENTC", "CSE",
        "CSE", "IT", "Mechanical", "ENTC", "CSE"
    ],
    "Company": [
        "TCS", "Infosys", "Google", "Wipro", "TCS",
        "Amazon", "Not Placed", "Infosys", "Microsoft",
        "Not Placed", "Not Placed", "Wipro",
        "Amazon", "TCS", "Infosys", "Google",
        "Microsoft", "Not Placed", "Wipro", "Amazon"
    ],
    "Package": [
        4.5, 5, 18, 4, 4.5,
        12, 0, 5, 22, 0,
        0, 4, 12, 4.5, 5,
        16, 20, 0, 4.5, 14
    ],
    "Status": [
        "Placed", "Placed", "Placed", "Placed", "Placed",
        "Placed", "Not Placed", "Placed", "Placed",
        "Not Placed", "Not Placed", "Placed",
        "Placed", "Placed", "Placed", "Placed",
        "Placed", "Not Placed", "Placed", "Placed"
    ]
}

df = pd.DataFrame(data)

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("# 🎓 PlacementIQ")
st.sidebar.caption("CAMPUS INTELLIGENCE PLATFORM")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "NAVIGATION",
    ["Overview", "Department Analysis", "Company Analysis",
     "Salary Insights", "Student Records"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### FILTERS")

departments = st.sidebar.multiselect(
    "Select Department",
    sorted(df["Department"].unique()),
    default=sorted(df["Department"].unique())
)

filtered = df[df["Department"].isin(departments)]

placed_df = filtered[filtered["Status"] == "Placed"]
total = len(filtered)
placed = len(placed_df)
unplaced = total - placed

rate = placed / total * 100 if total else 0
avg = placed_df["Package"].mean() if placed else 0
highest = placed_df["Package"].max() if placed else 0

# ---------------- CHART THEME ----------------
COLORS = [
    "#9B5DE5",
    "#00F5D4",
    "#F15BB5",
    "#FEE440",
    "#00BBF9",
    "#FB8500"
]

def style_chart(fig, height=350):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#19182B",
        plot_bgcolor="#19182B",
        font=dict(
            family="Arial",
            color="#EDEBFF"
        ),
        height=height,
        margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(
            bgcolor="rgba(0,0,0,0)"
        ),
        title_font=dict(size=17, color="#FFFFFF")
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor="#454065"
    )
    fig.update_yaxes(
        gridcolor="#34304F",
        zerolinecolor="#454065"
    )
    return fig

# ---------------- HEADER ----------------
st.markdown(
    '<div class="main-title">Placement Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Real-time campus recruitment insights | Academic Year 2026-27</div>',
    unsafe_allow_html=True
)

# ---------------- OVERVIEW ----------------
if page == "Overview":

    st.markdown("### ✨ PERFORMANCE OVERVIEW")

    if total == 0:
        st.warning("No students available for the selected departments.")
        st.stop()

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        ("TOTAL STUDENTS", total, "Academic database"),
        ("PLACED STUDENTS", placed, "Successful selections"),
        ("PLACEMENT RATE", f"{rate:.1f}%", "Overall performance"),
        ("AVERAGE PACKAGE", f"₹{avg:.2f} LPA", "Placed students only")
    ]

    for col, (label, value, note) in zip(
        [c1, c2, c3, c4], metrics
    ):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-note">✦ {note}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### Placement Status")

        status = filtered["Status"].value_counts().reset_index()
        status.columns = ["Status", "Students"]

        fig = px.pie(
            status,
            names="Status",
            values="Students",
            hole=0.68,
            color="Status",
            color_discrete_map={
                "Placed": "#00F5D4",
                "Not Placed": "#F15BB5"
            }
        )

        fig.update_traces(
            textinfo="percent+label",
            marker=dict(line=dict(color="#19182B", width=4))
        )

        fig.add_annotation(
            text=f"{rate:.1f}%<br>PLACED",
            showarrow=False,
            font=dict(size=19, color="#FFFFFF")
        )

        st.plotly_chart(style_chart(fig), use_container_width=True)

    with c2:
        st.markdown("### Department Performance")

        dept = filtered.groupby(
            ["Department", "Status"]
        ).size().reset_index(name="Students")

        fig = px.bar(
            dept,
            x="Department",
            y="Students",
            color="Status",
            barmode="group",
            color_discrete_map={
                "Placed": "#9B5DE5",
                "Not Placed": "#F15BB5"
            }
        )

        st.plotly_chart(style_chart(fig), use_container_width=True)

    st.markdown("### 🏆 Top Recruiting Companies")

    company = placed_df["Company"].value_counts().reset_index()
    company.columns = ["Company", "Students"]

    fig = px.bar(
        company,
        x="Company",
        y="Students",
        color="Company",
        color_discrete_sequence=COLORS,
        text="Students"
    )

    fig.update_traces(
        marker_line_width=0,
        textposition="outside"
    )

    st.plotly_chart(style_chart(fig), use_container_width=True)

# ---------------- DEPARTMENT ANALYSIS ----------------
elif page == "Department Analysis":

    st.markdown("## 🏢 Department-wise Analysis")

    dept = filtered.groupby("Department").agg(
        Total=("Student", "count"),
        Placed=("Status", lambda x: (x == "Placed").sum()),
        Average_Package=("Package", "mean")
    ).reset_index()

    dept["Placement Rate"] = (
        dept["Placed"] / dept["Total"] * 100
    )

    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(
            dept,
            x="Department",
            y="Placement Rate",
            color="Department",
            color_discrete_sequence=COLORS,
            text_auto=".1f",
            title="Placement Percentage by Department"
        )
        fig.update_yaxes(title="Placement Rate (%)")
        st.plotly_chart(style_chart(fig), use_container_width=True)

    with c2:
        fig = px.treemap(
            dept,
            path=["Department"],
            values="Placed",
            color="Placement Rate",
            color_continuous_scale=[
                "#25223D", "#9B5DE5", "#00F5D4"
            ],
            title="Department Placement Treemap"
        )
        st.plotly_chart(style_chart(fig), use_container_width=True)

    st.dataframe(dept.round(2), use_container_width=True)

# ---------------- COMPANY ANALYSIS ----------------
elif page == "Company Analysis":

    st.markdown("## 🏆 Company Recruitment Analysis")

    if placed_df.empty:
        st.info("No placed students in selected departments.")
    else:
        company = placed_df.groupby("Company").agg(
            Students=("Student", "count"),
            Average_Package=("Package", "mean"),
            Highest_Package=("Package", "max")
        ).reset_index()

        c1, c2 = st.columns(2)

        with c1:
            fig = px.bar(
                company,
                x="Company",
                y="Students",
                color="Company",
                color_discrete_sequence=COLORS,
                title="Company-wise Selection"
            )
            st.plotly_chart(style_chart(fig), use_container_width=True)

        with c2:
            fig = px.scatter(
                company,
                x="Average_Package",
                y="Students",
                size="Highest_Package",
                color="Company",
                color_discrete_sequence=COLORS,
                hover_name="Company",
                title="Package vs Recruitment"
            )
            st.plotly_chart(style_chart(fig), use_container_width=True)

        st.dataframe(company.round(2), use_container_width=True)

# ---------------- SALARY INSIGHTS ----------------
elif page == "Salary Insights":

    st.markdown("## 💰 Salary Package Insights")

    if placed_df.empty:
        st.info("No placed students in selected departments.")
    else:
        c1, c2, c3 = st.columns(3)

        c1.metric("Average Package", f"₹{avg:.2f} LPA")
        c2.metric("Highest Package", f"₹{highest:.2f} LPA")
        c3.metric("Students Placed", placed)

        c1, c2 = st.columns(2)

        with c1:
            fig = px.histogram(
                placed_df,
                x="Package",
                nbins=8,
                color_discrete_sequence=["#9B5DE5"],
                title="Salary Distribution"
            )
            st.plotly_chart(style_chart(fig), use_container_width=True)

        with c2:
            fig = px.box(
                placed_df,
                x="Department",
                y="Package",
                color="Department",
                color_discrete_sequence=COLORS,
                title="Department-wise Salary Comparison"
            )
            st.plotly_chart(style_chart(fig), use_container_width=True)

# ---------------- STUDENT RECORDS ----------------
elif page == "Student Records":

    st.markdown("## 👨‍🎓 Student Placement Records")

    search = st.text_input("🔍 Search Student or Company")

    records = filtered.copy()

    if search:
        records = records[
            records["Student"].str.contains(search, case=False) |
            records["Company"].str.contains(search, case=False)
        ]

    st.dataframe(
        records,
        use_container_width=True,
        hide_index=True
    )

    csv = records.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download Student Records",
        data=csv,
        file_name="placement_records.csv",
        mime="text/csv"
    )

st.markdown("---")
st.markdown(
    "<center style='color:#77718F'>PLACEMENTIQ © 2026 | "
    "SMART CAMPUS ANALYTICS</center>",
    unsafe_allow_html=True
)
