
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
    background: #F7F5EF;
    color: #294B3A;
}

[data-testid="stHeader"] {
    background: rgba(247,245,239,0.95);
}

[data-testid="stSidebar"] {
    background: #E9EEE6;
    border-right: 1px solid #D5DED2;
}

[data-testid="stSidebar"] * {
    color: #294B3A;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #294B3A;
    letter-spacing: -1px;
}

.subtitle {
    color: #7B897D;
    font-size: 14px;
    margin-bottom: 28px;
}

.section-title {
    color: #294B3A;
    font-size: 21px;
    font-weight: 700;
}

.metric-card {
    background: #FFFFFF;
    border: 1px solid #E1E7DE;
    border-radius: 18px;
    padding: 22px;
    min-height: 125px;
    box-shadow: 0 5px 18px rgba(41,75,58,0.06);
    transition: 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 9px 22px rgba(41,75,58,0.12);
}

.metric-label {
    color: #829084;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 1px;
}

.metric-value {
    font-size: 29px;
    font-weight: 800;
    color: #294B3A;
    margin-top: 12px;
}

.metric-note {
    color: #72977A;
    font-size: 12px;
    margin-top: 5px;
}

.stButton>button {
    background: #294B3A;
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    padding: 8px 18px;
    font-weight: 600;
}

.stButton>button:hover {
    background: #426C50;
    color: white;
}

.stDownloadButton>button {
    background: #E3EDE3;
    color: #294B3A;
    border: 1px solid #B9CDBA;
    border-radius: 10px;
}

.stDownloadButton>button:hover {
    background: #D3E3D4;
    color: #294B3A;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #DCE4D9;
    border-radius: 12px;
}

h1, h2, h3 {
    color: #294B3A !important;
}

hr {
    border-color: #DCE4D9;
}

[data-testid="stMetric"] {
    background: #FFFFFF;
    padding: 14px;
    border-radius: 12px;
    border: 1px solid #E1E7DE;
}

[data-baseweb="select"] > div {
    background-color: #FFFFFF;
    border-color: #D5DED2;
    border-radius: 9px;
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
    "#294B3A",  # Forest Green
    "#A3BFA8",  # Sage Green
    "#D68C70",  # Terracotta
    "#D9B86C",  # Soft Gold
    "#7895A3",  # Dusty Blue
    "#B7A6C9"   # Lavender
]



def style_chart(fig, height=350):

    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",

        font=dict(
            family="Arial",
            color="#294B3A",
            size=12
        ),

        height=height,

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),

        title_font=dict(
            size=18,
            color="#294B3A"
        ),

        legend=dict(
            bgcolor="rgba(255,255,255,0)"
        )
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor="#E1E7DE",
        tickfont=dict(color="#718477")
    )

    fig.update_yaxes(
        gridcolor="#EDF0E9",
        zerolinecolor="#DCE4D9",
        tickfont=dict(color="#718477")
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
    "Placed": "#294B3A",
    "Not Placed": "#D68C70"
}
        )

        fig.update_traces(
            textinfo="percent+label",
            marker=dict(line=dict(color="#19182B", width=4))
        )

        fig.add_annotation(
            text=f"{rate:.1f}%<br>PLACED",
            showarrow=False,
            font=dict(size=19, color="#294B3A")
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
