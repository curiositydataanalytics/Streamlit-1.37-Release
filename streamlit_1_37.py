# Data process
import numpy as np
import datetime as dt
import pandas as pd
import geopandas as gpd

# Data viz
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import graphviz
import pydeck as pdk

# App config
#----------------------------------------------------------------------------------------------------------------------------------#
# Page config
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title
st.title("What's new in Streamlit 1.37?")
st.divider()

with st.sidebar:
    st.image('logo.png')

#
#

# 1) Introducing st.context to read headers and cookies
#---------------------------------------------------------------------------------------#
st.header(':one: Introducing st.context to read headers and cookies')

# options
options = ['Option ' + str(i+1) for i in np.arange(0,20,1)]

# using multiselect
st.multiselect('test', options)

# using expander + checkbox
with st.expander('Choose an option'):
    for i in options:
        st.checkbox(i, key=i)
selected_options = [key for key, value in st.session_state.items() if value is True]
st.write(selected_options)

st.code('''
st.context.headers
''')

header = {"Host":"localhost:8501",
"Connection":"Upgrade",
"Pragma":"no-cache",
"Cache-Control":"no-cache",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
"Upgrade":"websocket",
"Origin":"http://localhost:8501",
"Sec-Websocket-Version":"13",
"Accept-Encoding":"gzip, deflate, br, zstd",
"Accept-Language":"es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
"Cookie":"ajs_anonymous_id=6bece3ec-8e56-4db2-96d8-70e8a2e594db",
"Sec-Websocket-Key":"342223kuaq428KqfgsdsSvcdgfg2u6Q==",
"Sec-Websocket-Extensions":"permessage-deflate; client_max_window_bits",
"Sec-Websocket-Protocol":"streamlit, PLACEHOLDER_AUTH_TOKEN"
}
st.write(header)

st.code('''

if 'en' in st.context.headers['Accept-Language'].split(',')[0]:
        st.subheader('Welcome!')
elif 'es' in st.context.headers['Accept-Language'].split(',')[0]:
        st.subheader('Bienvenidos!')
''')

if 'en' in header['Accept-Language'].split(',')[0]: st.subheader('Welcome!')
elif 'es' in header['Accept-Language'].split(',')[0]: st.subheader('Bienvenidos!')

st.divider()

# 2) st.bar_chart can render charts horizontally
#---------------------------------------------------------------------------------------#
st.header(':two: Introducing st.feedback to collect ratings and sentiment from your users')

cols = st.columns(3)

with cols[0]:
    st.code('''
    st.subheader('Rate your experience')        

    feedback = st.feedback('thumbs')
            
    if feedback==1:
        st.write('Thanks for your positive feedback!')
    elif feedback==0:
        st.write('Sorry to hear you had a negative experience.')
    ''')

with cols[1]:
    st.code('''
    st.subheader('Rate your experience')        

    feedback = st.feedback('faces')

    if feedback != None:
        st.write(({0 : 'Very unsatisfied',
                   1 : 'Unsatisfied',
                   2 : 'Neutral',
                   3 : 'Satisfied',
                   4 : 'Very satisfied'}.get(feedback)))
    ''')

with cols[2]:
    st.code('''
st.subheader('Rate your experience')
            
feedback = st.feedback('stars')
            
if feedback != None:
    st.write(f'You have selected {feedback+1} star(s).') 
''')

cols = st.columns(3)

with cols[0]:
    st.subheader('Rate your experience')
    feedback = st.feedback('thumbs')
    if feedback==1:
        st.write('Thanks for your positive feedback!')
    elif feedback==0:
        st.write('Sorry to hear you had a negative experience.')

with cols[1]:
    st.subheader('Rate your experience')
    feedback = st.feedback('faces')
    if feedback != None:
        st.write(({0 : 'Very unsatisfied', 1 : 'Unsatisfied', 2 : 'Neutral', 3 : 'Satisfied', 4 : 'Very satisfied'}.get(feedback)))

with cols[2]:
    st.subheader('Rate your experience')
    feedback = st.feedback('stars')
    if feedback != None:
        st.write(f'You have selected {feedback+1} star(s).') 




st.divider()

# 3) Announcing the general availability of st.fragment, a decorator that lets you rerun functions independently of the whole page
#---------------------------------------------------------------------------------------#
st.header(':three: Announcing the general availability of st.fragment, a decorator that lets you rerun functions independently of the whole page')

cols = st.columns(2)
cols[0].subheader('Streamlit 1.36')
cols[1].subheader('Streamlit 1.37')

cols[0].code('''
import pydeck as pdk             

cols = st.columns((0.3,0.7))
             
cols[0].selectbox('Status', status_options, index=None)
cols[0].selectbox('Type', types_options, index=None)

pdk.ViewState(...)
pdk.Layer(...)
pdk_map = pdk.Deck(...)

cols[1].pydeck_chart(pdk_map)

             

#
''')

cols[1].code('''
import pydeck as pdk  

@st.fragment
def map_selection():
    cols = st.columns((0.3,0.7))
             
    cols[0].selectbox('Status', status_options, index=None)
    cols[0].selectbox('Type', types_options, index=None)

    pdk.ViewState(...)
    pdk.Layer(...)
    pdk_map = pdk.Deck(...)

    cols[1].pydeck_chart(pdk_map)

map_selection()
''')

@st.cache_data
def load_data():
    volcanos = gpd.read_file('https://services.arcgis.com/BG6nSlhZSAWtExvp/arcgis/rest/services/World_Volcanoes/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson')
    volcanos['color'] = volcanos.ELEV.apply(lambda x: [(i * 255) for i in plt.cm.Blues((x-volcanos.ELEV.min()) / (volcanos.ELEV.max() - volcanos.ELEV.min()))[0:3]])
    return volcanos

cols = st.columns(2)
with cols[0]:
    volcanos136 = load_data()
    subcols = st.columns((0.3,0.7))
    status = subcols[0].selectbox('Status', volcanos136.STATUS.unique(), index=None)
    type = subcols[0].selectbox('Type', volcanos136.TYPE.unique(), index=None)

    view_state = pdk.ViewState(
                    longitude=volcanos136.Lon.mean(),
                    latitude=volcanos136.Lat.mean(),
                    zoom=1,
                    min_zoom=1,
                    max_zoom=15
                )

    # Points Layer
    layer_pts = pdk.Layer(
        type="ScatterplotLayer",
        data=volcanos136[(volcanos136.STATUS==status) & (volcanos136.TYPE==type)],
        get_fill_color='[color[0], color[1], color[2]]',
        get_radius=1,
        pickable=True,
        radius_scale=1,
        radius_min_pixels=5,
        radius_max_pixels=500,
        get_position='[Lon, Lat]'
        )

    # Pydeck object
    pdk_map = pdk.Deck(
                map_provider='carto',
                map_style='light',
                initial_view_state=view_state,
                layers=[layer_pts]
                )

    subcols[1].pydeck_chart(pdk_map)


with cols[1]:
    volcanos137 = load_data()
    @st.fragment
    def vol():
        subcols = st.columns((0.3,0.7))
        with subcols[0]:
            st.selectbox('Status', volcanos137.STATUS.unique(), key='status', index=None)
            st.selectbox('Type', volcanos137.TYPE.unique(), key='type', index=None)

        view_state = pdk.ViewState(
                        longitude=volcanos137.Lon.mean(),
                        latitude=volcanos137.Lat.mean(),
                        zoom=1,
                        min_zoom=1,
                        max_zoom=15
                    )

        # Points Layer
        layer_pts = pdk.Layer(
            type="ScatterplotLayer",
            data=volcanos137[(volcanos137.STATUS==status) & (volcanos137.TYPE==type)],
            get_fill_color='[color[0], color[1], color[2]]',
            get_radius=1,
            pickable=True,
            radius_scale=1,
            radius_min_pixels=5,
            radius_max_pixels=500,
            get_position='[Lon, Lat]'
            )

        # Pydeck object
        pdk_map2 = pdk.Deck(
                    map_provider='carto',
                    map_style='light',
                    initial_view_state=view_state,
                    layers=[layer_pts]
                    )
        
        subcols[1].pydeck_chart(pdk_map2)

    vol()
        



# 4) Announcing the general availability of st.dialog, a decorator that lets you create modal dialogs.
#---------------------------------------------------------------------------------------#
st.header(':four: Announcing the general availability of st.dialog, a decorator that lets you create modal dialogs.')


st.code('''
@st.dialog('Contact details')
def popup_dialog():
    Name = st.text_input('Name')
    Email = st.text_input('Email')
    if st.button('Submit'):
        st.session_state['contact_list'].append({'Name' : Name, 'Email' : Email})
        st.rerun()

if 'contact_list' not in st.session_state:
    st.session_state['contact_list'] = []

cols = st.columns((0.1,0.9))
if cols[0].button('Create New Contact'):
    popup_dialog()
if cols[1].button('Reset Contact List'):
    st.session_state['contact_list'] = []

st.subheader('My Contact List')

if st.session_state['contact_list'] == []:
    st.write('The list is empty.')
else:
    st.dataframe(pd.DataFrame(st.session_state['contact_list']), width=1000, hide_index=True)

''')


@st.dialog('Contact details')
def popup_dialog():
    Name = st.text_input('Name')
    Email = st.text_input('Email')
    if st.button('Submit'):
        st.session_state['contact_list'].append({'Name' : Name, 'Email' : Email})
        st.rerun()

if 'contact_list' not in st.session_state:
    st.session_state['contact_list'] = []

cols = st.columns((0.1,0.9))
if cols[0].button('Create New Contact'):
    popup_dialog()
if cols[1].button('Reset Contact List'):
    st.session_state['contact_list'] = []

st.subheader('My Contact List')

if st.session_state['contact_list'] == []:
    st.write('The list is empty.')
else:
    st.dataframe(pd.DataFrame(st.session_state['contact_list']), width=1000, hide_index=True)

st.divider()


# 5) You can use icons from the Material Symbols library in Markdown.
#---------------------------------------------------------------------------------------#
st.header(':five: You can use icons from the Material Symbols library in Markdown')

cols = st.columns(2)
cols[0].subheader('Streamlit 1.36')
cols[1].subheader('Streamlit 1.37')

cols[0].code('''
st.title(':house: :question: :arrows_clockwise: :hourglass_flowing_sand:')
''')

cols[1].code('''
st.title(':material/search: :material/home: :material/download: :material/refresh:')
''')

cols[0].title(':house: :question: :arrows_clockwise: :hourglass_flowing_sand:')
cols[1].title(':material/search: :material/home: :material/download: :material/refresh:')

st.divider()

# 6) You can pass graphviz.Source objects to st.graphviz_chart
#---------------------------------------------------------------------------------------#
st.header(':six: You can pass graphviz.Source objects to st.graphviz_chart')

cols = st.columns(2)
cols[0].subheader('Streamlit 1.36')
cols[1].subheader('Streamlit 1.37')

cols[0].code('''
import graphviz

dot = graphviz.Digraph()
dot.node('A', 'Node A')
dot.node('B', 'Node B.1')
dot.node('C', 'Node B.2')
dot.edge('A', 'B')
dot.edge('A', 'C')

st.graphviz_chart(dot, use_container_width=True)
''')

cols[1].code('''
import graphviz

dot = 'digraph { A [label="Node A"] B [label="Node B.1"] C [label="Node B.2"] A -> B A -> C }'
             
st.graphviz_chart(dot, use_container_width=True)      


             

# 
''')

dot = graphviz.Digraph()
dot.node('A', 'Node A')
dot.node('B', 'Node B.1')
dot.node('C', 'Node B.2')
dot.edge('A', 'B')
dot.edge('A', 'C')

cols[0].graphviz_chart(dot, use_container_width=True)

cols[1].graphviz_chart('digraph { A [label="Node A"] B [label="Node B.1"] C [label="Node B.2"] A -> B A -> C }', use_container_width=True)

st.divider()

# 7) You can modify the stacking behavior for st.bar_chart and st.area_chart.
#---------------------------------------------------------------------------------------#
st.header(':seven: You can modify the stacking behavior for st.bar_chart and st.area_chart.')

cols = st.columns(2, vertical_alignment='top')
cols[0].subheader('Streamlit 1.36')
cols[1].subheader('Streamlit 1.37')

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

cols[0].code('''
st.bar_chart(df)
''')

cols[0].bar_chart(chart_data)

cols[1].code('''
st.bar_chart(df, stack=False)
''')
cols[1].bar_chart(chart_data, stack=False)

cols[1].code('''
st.bar_chart(df, stack='layered')
''')
cols[1].bar_chart(chart_data, stack='layered')

cols[1].code('''
st.bar_chart(df, stack='normalize')
''')
cols[1].bar_chart(chart_data, stack='normalize')

cols[1].code('''
st.bar_chart(df, stack='center')
''')
cols[1].bar_chart(chart_data, stack='center')

st.divider()