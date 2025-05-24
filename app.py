# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from scraper import scrape_remoteok

st.set_page_config(page_title="Real-Time Job Trend Analyzer", layout="wide")

st.title("💼 Real-Time Job Trend Analyzer (RemoteOK)")

keyword = st.text_input("Enter a job keyword (e.g. data scientist, python developer):", "data scientist")

if st.button("🔍 Fetch Jobs"):
    with st.spinner("Scraping RemoteOK..."):
        jobs = scrape_remoteok(keyword)

        if jobs:
            df = pd.DataFrame(jobs)
            st.success(f"✅ Found {len(jobs)} jobs for '{keyword}'")
            st.dataframe(df)

            # Download
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📁 Download CSV", csv, f"{keyword}_jobs.csv", "text/csv")

            # --- CHARTS SECTION ---
            st.subheader("📊 Insights")

            col1, col2 = st.columns(2)

            with col1:
                top_companies = df["company"].value_counts().head(5).reset_index()
                top_companies.columns = ["Company", "Job Count"]
                fig1 = px.bar(top_companies, x="Company", y="Job Count", title="Top 5 Hiring Companies", color="Company")
                st.plotly_chart(fig1, use_container_width=True)

            with col2:
                top_locations = df["location"].value_counts().head(5).reset_index()
                top_locations.columns = ["Location", "Job Count"]
                fig2 = px.pie(top_locations, values="Job Count", names="Location", title="Top 5 Job Locations")
                st.plotly_chart(fig2, use_container_width=True)

            # --- Posting Trends ---
            if "date_posted" in df.columns:
                try:
                    df["date_posted"] = pd.to_datetime(df["date_posted"], errors="coerce")
                    trend_data = df["date_posted"].value_counts().sort_index().reset_index()
                    trend_data.columns = ["Date Posted", "Job Count"]
                    fig3 = px.line(trend_data, x="Date Posted", y="Job Count", title="Job Posting Trend Over Time")
                    st.plotly_chart(fig3, use_container_width=True)
                except Exception as e:
                    st.warning(f"Could not generate trend chart: {e}")
        else:
            st.warning("❌ No jobs found or RemoteOK blocked the request.")
