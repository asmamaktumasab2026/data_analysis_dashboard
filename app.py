import streamlit as st
st.title(" Interactive Data Analysis Dashboard")
st.write("Explore your data,Discover insights")
import pandas as pd
import plotly.express as px
st.subheader("Upload your dataset")
uploaded_file=st.file_uploader("Upload csv or excel file",type=["csv","xlsx"])
if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df=pd.read_csv(uploaded_file)
    else:
        df=pd.read_excel(uploaded_file)
else:
    df=pd.read_csv("StudentsPerformance.csv")
numeric_columns=df.select_dtypes(include="number").columns.tolist()
st.subheader("Choose metrics to Analyze");
selected_columns=st.multiselect("Choose numerical columns",numeric_columns,default=numeric_columns[:3])
if selected_columns:
    averages=df[selected_columns].mean()
    st.subheader("Average values overview")
    st.bar_chart(averages)
if selected_columns:
    first_column=selected_columns[0]
    col1,col2,col3=st.columns(3)
    col1.metric("Average",round(df[first_column].mean(),2))
    col2.metric("Maximum",round(df[first_column].max(),2))
    col3.metric("Minimum",round(df[first_column].min(),2))
st.subheader("Filter your data")
filter_column=st.selectbox("Choose column to filter",df.columns,key="filter_column")
filter_values=df[filter_column].dropna().unique()
selected_values=st.multiselect("Choose values",filter_values)
filtered_df=df[df[filter_column].isin(selected_values)]
st.subheader("Filtered dataset")
st.dataframe(filtered_df)
st.subheader("Distribution and insights")
pie_column=st.selectbox("Choose column to pie chart",df.columns,key="pie_column")
if pd.api.types.is_numeric_dtype(df[pie_column]):
    pie_data=df[pie_column].dropna()
    analysis_type=st.radio("Choose analysis",["Exact value","range"],key="pie_analysis")
    if analysis_type=="Exact value":
      target_value=st.number_input("Enter value",value=float(pie_data.min()))
      matching=(pie_data==target_value).sum()
      remaining=len(pie_data)-matching
      fig=px.pie(names=["matching","remaining"],values=[matching,remaining],hole=0.4)
    else:
        selected_range=st.slider("select  range",min_value=float(pie_data.min()),max_value=float(pie_data.max()),
                                 value=(float(pie_data.min()),float(pie_data.max())))
        matching=pie_data.between(selected_range[0],selected_range[1]).sum()
        remaining=len(pie_data)-matching
        
        fig=px.pie(names=["Matching","Remaining"],
                   values=[matching,remaining],
                   hole=0.4)
else:
    category_counts=(df[pie_column].fillna("Missing").astype(str).value_counts())
    fig=px.pie(names=category_counts.index,values=category_counts.values,title=f"Distribution of{pie_column}",hole=0.4)     
fig.update_traces(textinfo="label+percent+value")
st.plotly_chart(fig,width="stretch")                                   
                                
    

    
                
    
                

