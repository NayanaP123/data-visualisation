import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')    #ignore warning


st.set_page_config(page_title="Superstore!!!", page_icon=":bar_chart:", layout="wide")  #barchart

st.title(":bar_chart: Sample SuperStore EDA")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)  #to up the title


#user can browse and upload data to the dashboard

fl=st.file_uploader(":file_folder: Upload a file", type=(["csv","txt","xlsx","xls"]))

if fl is not None:    #if not choosing file
    filename=fl.name
    st.write(filename)
    df=pd.read_csv(filename, encoding="ISO-8859-1")

else:
    os.chdir("F:\data")
    df=pd.read_csv("Superstore.csv", encoding="ISO-8859-1")




col1, col2= st.columns((2))

df["Order Date"]=pd.to_datetime(df["Order Date"])
startDate=pd.to_datetime(df["Order Date"]).min()
endDate=pd.to_datetime(df["Order Date"]).max()


with col1:
    date1=pd.to_datetime(st.date_input("Start Date", startDate))
with col2:
    date2=pd.to_datetime(st.date_input("End Date", endDate))


df= df[(df["Order Date"]>= date1)&(df["Order Date"]<=date2)].copy()

#data saved in df automatically(data frame)

#filter

st.sidebar.header("choose your filter: ")
#for region
region=st.sidebar.multiselect("pick your region", df["Region"].unique())


if not region:
    df2=df.copy()
else:
    df2=df[df["Region"].isin(region)]


#create for state
state=st.sidebar.multiselect("pick your state", df["State"].unique())


if not state:
    df3=df2.copy()
else:
    df3=df2[df2["State"].isin(state)]

#create for city
city=st.sidebar.multiselect("pick your city", df["City"].unique())

#filter data based o region and state and city --permutation and combination
if not region and not state and not city:
    filtered_df=df
elif not state and not city:
    filtered_df=df[df["Region"].isin(region)]
elif not region and not city:
    filtered_df=df[df["State"].isin(state)]

elif state and city:
    filtered_df=df3[df["State"].isin(state) & df3["City"].isin(city)]
elif region and city:
    filtered_df=df3[df["State"].isin(region) & df3["City"].isin(city)]
elif region and state:
    filtered_df=df3[df["Region"].isin(region) & df3["State"].isin(state)]
elif city:
    filtered_df=df3[df3["City"].isin(city)]

else:
    filtered_df=df3[df3["Region"].isin(region) & df3["State"].isin(state) & df3["City"].isin(city)]

#coloum chart for category and region
category_df=filtered_df.groupby(by=["Category"], as_index=False)["Sales"].sum()
#how can create the chart
with col1:
    st.subheader("Category Wise Sales")
    fig=px.bar(category_df, x="Category", y="Sales", text=['${:,.2f}'.format(x) for x in category_df["Sales"]],
               template="seaborn")
    st.plotly_chart(fig,use_container_width=True, height=200)

with col2:
    st.subheader("Region Wise Sales")
    fig=px.pie(filtered_df, values="Sales", names="Region", hole=0.5)
    fig.update_traces(text=filtered_df["Region"], textposition="outside")
    st.plotly_chart(fig,use_container_width=True)


cl1,cl2=st.columns(2)
with cl1:
    with st.expander("Category_ViewData"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        #to download the data
        csv= category_df.to_csv(index=False).encode('utf-8')
        #button
        st.download_button("Download Data", data=csv, file_name="Category.csv", mime="text/csv",
                           help='click here to download the data as a csv file')

with cl2:
    with st.expander("Region_ViewData"):
        Region=filtered_df.groupby(by="Region", as_index=False)["Sales"].sum()
        st.write(Region.style.background_gradient(cmap="Oranges"))
        #to download the data
        csv= Region.to_csv(index=False).encode('utf-8')
        #button
        st.download_button("Download Data", data=csv, file_name="Region.csv", mime="text/csv",
                           help='click here to download the data as a csv file')


