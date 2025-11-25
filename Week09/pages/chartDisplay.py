import streamlit as st
import pandas as pd
import numpy as np

date = pd.DataFrame(
    np.random.randn(30,4),
    columns=["London", "New York", "Tokyo", "Dubai"]
)

col1,col2 = st.columns(2)

with col1:
    st.line_chart(date)
with col2:
    st.area_chart(date)