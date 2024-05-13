import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc, callback, Input,Output
import dash_bootstrap_components as dbc

dash.register_page(__name__, path = "/salesanalysis", title = "Sales Analysis")

superstore = pd.read_csv("data/Sample - Superstore.csv", encoding = "latin1")
superstore['Order Date'] = pd.to_datetime(superstore['Order Date'], format = "%m/%d/%Y")

categorysales = superstore.groupby('Category')['Sales'].sum()


####

segmentsales = superstore.groupby('Segment')['Sales'].sum()
segmentsalesdistribution = px.pie(names = segmentsales.index, 
                                      values = categorysales.values,
                                      hole = 0.7,
                                      color_discrete_sequence = px.colors.qualitative.Dark24_r)

segmentsalesdistribution.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)",
                                           legend_font_color = 'white', title = dict(font = dict(color = 'white')))

totalsales = '${:,}'.format(round(segmentsales.sum(), 2))
segmentsalesdistribution.add_annotation(text = "Total Sales by Segment", showarrow = False,
                                            font_size = 14, font_color = 'White',
                                            y = 0.55)
segmentsalesdistribution.add_annotation(text = totalsales, showarrow = False,
                                            font_size = 14, font_color = 'White', y = 0.45)


categoryprofit = superstore.groupby('Category')['Profit'].sum()
categoryprofitdistribution = px.pie(names = categoryprofit.index, 
                                      values = categoryprofit.values,
                                      hole = 0.7,
                                      color_discrete_sequence = px.colors.qualitative.Dark24_r)

categoryprofitdistribution.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)",
                                           legend_font_color = 'white')

totalprofit = '${:,}'.format(round(categoryprofit.sum(), 2))
categoryprofitdistribution.add_annotation(text = "Total Profit by Category", showarrow = False,
                                            font_size = 14, font_color = 'White',
                                            y = 0.55)
categoryprofitdistribution.add_annotation(text = totalprofit, showarrow = False,
                                            font_size = 14, font_color = 'White', y = 0.45)

##

categorysalesprofit = superstore.groupby('Category').agg(
                      {"Sales" : 'sum', 'Profit' : 'sum', 'Quantity' : 'sum'}  
                    ).reset_index()

categorysalesprofitdistribution = px.scatter(categorysalesprofit, x = 'Profit', y = 'Sales', color = 'Category',
                                             size = "Quantity" , title = "Category Quantity for Sales Vs Returns")

categorysalesprofitdistribution.update_layout(plot_bgcolor = 'rgba(0,0,0,0)', paper_bgcolor = 'rgba(0,0,0,0)',
                                              xaxis = dict(title = "Total Profit", color = 'white'),
                                              yaxis = dict(title = "Total Sales", color = 'white'),
                                              title = dict(font  = dict(color = 'white')),
                                              legend_font_color = 'white'
                                              )

categorysalesprofitdistribution.update_xaxes(showgrid = False)
categorysalesprofitdistribution.update_yaxes(showgrid = False)

####

totalprofitbycustomer = superstore.groupby(['Customer Name', 'Order Date'])['Profit'].sum().reset_index()

totalprofitbycustomer = totalprofitbycustomer.groupby('Customer Name')['Profit'].sum().reset_index()

top5customersbyprofit = totalprofitbycustomer.nlargest(5, 'Profit')['Customer Name']

filteredtop5 = superstore[superstore['Customer Name'].isin(top5customersbyprofit)]

totalprofitovertimetop5 = filteredtop5.groupby(['Customer Name', filteredtop5['Order Date'].dt.year])['Profit'].sum().reset_index()
totalprofitovertimetop5['Order Date'] = pd.to_datetime(totalprofitovertimetop5['Order Date'], format = "%Y")

totalprofitovertimetop5distribution = px.area(totalprofitovertimetop5, x = 'Order Date', y = "Profit", color = "Customer Name", title = "Customer Profit Over Years")

totalprofitovertimetop5distribution.update_layout(plot_bgcolor = 'rgba(0,0,0,0)', paper_bgcolor = "rgba(0,0,0,0)",
                                                  legend_font_color = 'white', title_font = dict(color = "white"),
                                                  xaxis = dict(title = "Order Date", color = "white"),
                                                  yaxis = dict(title = "Total Profit", color = "white"),
                                                  )

totalprofitovertimetop5distribution.update_xaxes(showgrid = False)
totalprofitovertimetop5distribution.update_yaxes(showgrid = False)
####

categorysubcategorysales = superstore.groupby(['Category', 'Sub-Category'])['Sales'].sum().reset_index()

categorysubcategorysalesdistribution = px.sunburst(categorysubcategorysales, path = ['Category', 'Sub-Category'], values = 'Sales')

categorysubcategorysalesdistribution.update_layout(paper_bgcolor = 'rgba(0,0,0,0)')

categorysubcategorysalesdistribution.update_traces(marker = dict(colors = px.colors.qualitative.Dark24))


layout=html.Div(
    children=[
        dbc.Row(
            children=[
                dcc.Dropdown(
                    superstore['City'].unique(),value="Los Angeles",
                    id = "City_Dropdown",
                    style={'background':'black','color':'Yellow','font-size':20}
                ),
            ],
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    children=dcc.Graph(id="sales_category_distribution")
                ),
                dbc.Col(
                    children=dcc.Graph(figure=segmentsalesdistribution)
                ),
                dbc.Col(
                    children=dcc.Graph(figure=categoryprofitdistribution)
                ),
            ],
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    children=dcc.Graph(figure=categorysalesprofitdistribution)
                ),
                dbc.Col(
                    children=dcc.Graph(figure=totalprofitovertimetop5distribution)
                ),
                dbc.Col(
                    children=dcc.Graph(figure=categorysubcategorysalesdistribution)
                ),
            ],
        ),
    ]
)

@callback(
   Output("sales_category_distribution", "figure"),
   Input("City_Dropdown", 'value'),
)

def update_sales_category_distribution(city_value):
   city_filter_superstore=superstore[superstore['City']==city_value]

   categorysales = city_filter_superstore.groupby('Category')['Sales'].sum()
   categorysalesdistribution = px.pie(names = categorysales.index, 
                                       values = categorysales.values,
                                       hole = 0.8,
                                       color_discrete_sequence = px.colors.qualitative.Dark24_r)

   categorysalesdistribution.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)",
                                             legend_font_color = 'white', title = dict(font = dict(color = 'white', size=14)))

   totalsales = '${:,}'.format(round(categorysales.sum(), 2))
   categorysalesdistribution.add_annotation(text = "Total Sales by Category", showarrow = False,
                                             font_size = 11.5, font_color = 'White',
                                             y = 0.55)
   categorysalesdistribution.add_annotation(text = totalsales, showarrow = False,
                                             font_size = 10, font_color = 'White', y = 0.45)
   return categorysalesdistribution


