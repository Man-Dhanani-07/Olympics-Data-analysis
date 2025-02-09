import streamlit as st
import pandas as pd
import plotly.express as px
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
# Preprocess the data
df = preprocessor.preprocess()

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSRcYGCB9xflBzmGWXeVnnWTnhWQInOnrxWEQ&s')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    # Display titles based on user selections
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    elif selected_year == 'Overall':
        st.title(f"{selected_country} Overall Performance")
    elif selected_country == 'Overall':
        st.title(f"Medal Tally in {selected_year} Olympics")
    else:
        st.title(f"{selected_country} performance in {selected_year} Olympics")

    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df, 'region')

    # Plotting with Matplotlib
    plt.figure(figsize=(10, 5))
    st.title("Participating Nation over the year")
    plt.plot(nations_over_time['Edition'], nations_over_time['region'], marker='o')
    plt.title("Participating Nations Over the Years")
    plt.xlabel("Edition")
    plt.ylabel("Number of Countries")
    plt.xticks(rotation=45)
    plt.grid()
    st.pyplot(plt)

    events_over_time = helper.data_over_time(df, 'Event')

    # Plotting with Matplotlib
    plt.figure(figsize=(10, 5))
    st.title("Events Over time")
    plt.plot(events_over_time['Edition'], events_over_time['Event'], marker='o')
    plt.title("Events Over the Years")
    plt.xlabel("Edition")
    plt.ylabel("Events")
    plt.xticks(rotation=45)
    plt.grid()
    st.pyplot(plt)
    
    athlete_over_time = helper.data_over_time(df, 'Name')

    # Plotting with Matplotlib
    plt.figure(figsize=(10, 5))
    st.title("Athletes Over the year")
    plt.plot(athlete_over_time['Edition'], athlete_over_time['Name'], marker='o')
    plt.title("Atheletes Over the Years")
    plt.xlabel("Edition")
    plt.ylabel("Athletes")
    plt.xticks(rotation=45)
    plt.grid()
    st.pyplot(plt)
    
    st.title("No. of Events Over time(Every Sport)")
    fig,ax = plt.subplots(figsize = (20,20))
    x = df.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport',columns = 'Year',values = 'Event',aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)
    
    
    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a sport',sport_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)
    

if user_menu == 'Country-wise Analysis':
    
    st.sidebar.title("Country-wise Analysis")
    
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    
    selected_country = st.sidebar.selectbox('Select a Country',country_list)
    country_df = helper.yearwise_medal_tally(df,selected_country)
    st.title(selected_country+" Medal Tally over the year")
    plt.figure(figsize=(10, 6))
    plt.plot(country_df["Year"], country_df["Medal"], marker='o')
    plt.xlabel("Year")
    plt.ylabel("Medal")
    plt.title("Medal Count Over the Years")
    plt.grid(True)
    st.pyplot(plt)

    pt = helper.country_event_heatmap(df,selected_country)
    st.title(selected_country+" excels in the following sports")
    fig,ax = plt.subplots(figsize = (20,20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Most Successful athlete of "+ selected_country)
    top10_df = helper.most_successful_country_wise(df, selected_country)
    st.table(top10_df)
    
    
if user_menu == 'Athlete wise Analysis' :
    athlete_df = df.drop_duplicates(subset=['Name','region'])
    x1 =athlete_df['Age'].dropna()
    x2 =athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3 =athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x4 =athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist = False,show_rug = False)
    fig.update_layout(autosize = False,width = 1000, height = 600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x=[]
    name=[]
    famous_sports = ['Basketball','Judo','Football','Tug-Of-War','Athletics','Swimming','Badminton',
                    'Sailing','Gymnastics','Art Competitions','Handball','Weightlifting',
                    'Wrestling','Water Polo','Hockey','Rowing',
                    'Fencing','Shooting','Boxing','Taekwondo',
                    'Cycling','Diving','Canoeing','Tennis','Golf',
                    'Softball','Archery','Volleyball','Synchronized Swimming',
                    'Table Tennis','Baseball','Rhythmic Gymnastics','Rugby Sevens',
                    'Beach Volleyball','Triathlon','Rugby','Polo','Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport']==sport]
        x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
        name.append(sport)
    
    fig = ff.create_distplot(x,name,show_hist = False,show_rug = False)
    fig.update_layout(autosize = False,width = 1000, height = 600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)
    
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    st.title("Height vs Weight")
    selected_sport = st.selectbox('Select a sport',sport_list)
    
    temp_df = helper.weight_v_height(df, selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x='Weight', y='Height', data=temp_df,hue = temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)
    
    final = helper.men_vs_women(df)

    st.title("Men Vs Women Participation Over the Years")
    fig = px.line(final,x="Year",y=["Male","Female"])
    st.plotly_chart(fig)
    
    