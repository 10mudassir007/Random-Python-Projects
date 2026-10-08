import pandas as pd
import plotly.express as px
import streamlit as st

data = pd.read_csv('data.csv')

data['year_built'] = 2024 - data['housing_median_age']
data = data.sort_values(by='year_built')
#print(data.head())
s = data.groupby('year_built',as_index=False).agg({'median_house_value':'mean'})
s['median_house_value'] = round(s['median_house_value'],-1)
s.loc[0,'median_house_value'] = s.iloc[:10]['median_house_value'].median()
s.loc[51,'median_house_value'] = s.iloc[-11:]['median_house_value'].median()


st.set_page_config(page_title='Dashboard',page_icon='😍',layout='wide',initial_sidebar_state='expanded')
scatter_p = px.scatter_3d(data_frame=data,x='longitude',y='latitude',z='median_house_value',color='ocean_proximity')
scatter_p.update_layout(height=500)

donut = px.pie(data_frame=data,names='ocean_proximity',hole=0.65)
donut.update_layout(height=400)

df = pd.DataFrame({
    "Country": ["USA", "Canada", "Mexico",'Russia','Pakistan','India'],
    "Value": [10, 20, 15,50,100,500]
})

# Create a choropleth map
fig = px.choropleth(
    df,
    locations="Country",
    locationmode="country names",
    color="Value",
    hover_name="Country",
    width=600,
    height=500
)


tseries = px.line(s,x='year_built',y='median_house_value',width=600,height=500)
tseries_scater = px.scatter(s,x='year_built',y='median_house_value').data[0]
tseries.add_trace(tseries_scater)

col = st.columns((7.0,4.0),gap='medium')
print(s.tail())

with col[0]:
   st.markdown('### House Prices over the years')
   st.plotly_chart(tseries)
   st.markdown('### Example Chloropleth map')
   st.plotly_chart(fig)
with col[1]:
    st.markdown('### 3D long,lat and ocean proximity plot')
    st.plotly_chart(scatter_p)
    st.markdown('### Donut chart')
    st.plotly_chart(donut)
st.metric(label='abcd',value='aaaa')

print(s)
