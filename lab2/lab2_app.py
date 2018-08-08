from spyre import server
import pandas as pd

class Global_Vegetation_Health_Products(server.App):
    title = "Global and Regional Vegetation Health"

    inputs = [{     "input_type":'dropdown',
                    "label": 'Region',
                    "options" : [ {"label": "Vinnytsya", "value":"Vinnytsya"},
                                  {"label": "Volyn", "value":"Volyn"},
                                  {"label": "Dnipropetrovsk", "value":"Dnipropetrovsk"},
                                  {"label": "Donetsk", "value":"Donetsk"},
                                  {"label": "Zhytomyr", "value":"Zhytomyr"},
                                  {"label": "Transcarpathia", "value":"Transcarpathia"},
                                  {"label": "Zaporizhzhya", "value":"Zaporizhzhya"},
                                  {"label": "Ivano-Frankivsk", "value":"Ivano-Frankivsk"},
                                  {"label": "Kiev", "value":"Kiev"},
                                  {"label": "Kirovohrad", "value":"Kirovohrad"},
                                  {"label": "Lugansk", "value":"Lugansk"},
                                  {"label": "Lviv", "value":"Lviv"},
                                  {"label": "Mykolayiv", "value":"Mykolayiv"},
                                  {"label": "Odessa", "value":"Odessa"},
                                  {"label": "Poltava", "value":"Poltava"},
                                  {"label": "Rivne", "value":"Rivne"},
                                  {"label": "Sumy", "value":"Sumy"},
                                  {"label": "Ternopil", "value":"Ternopil"},
                                  {"label": "Kharkiv", "value":"Kharkiv"},
                                  {"label": "Kherson", "value":"Kherson"},
                                  {"label": "Khmelnytskyy", "value":"Khmelnytskyy"},
                                  {"label": "Cherkasy", "value":"Cherkasy"},
                                  {"label": "Chernivtsi", "value":"Chernivtsi"},
                                  {"label": "Chernihiv", "value":"Chernihiv"},
                                  {"label": "Crimea", "value":"Crimea"}],
                    "variable_name": 'province', 
                    "action_id": "update_data" }]  # action_ids can point to controls
    
    # changing the input state now activates this control so we no longer need a button
    controls = [{   "control_type" : "hidden",  
                    "label" : "get global and regional vegetation health",
                    "control_id" : "update_data"}]

    tabs = ["Plot", "Table"]  # add tabs

    outputs = [{    "output_type" : "plot",
                    "output_id" : "plot",
                    "control_id" : "update_data",
                    "tab" : "Plot",  # must specify which tab each output should live in
                    "on_page_load" : True },
                {   "output_type" : "table",
                    "output_id" : "table_id",
                    "control_id" : "update_data",
                    "tab" : "Table",
                    "on_page_load" : True }]

    def getData(self, params):
        province = params['province']
        regions = { 'Vinnytsya': 1, 'Volyn': 2, 'Dnipropetrovsk': 3, 'Donetsk': 4, 'Zhytomyr': 5, 'Transcarpathia': 6,
                    'Zaporizhzhya': 7, 'Ivano-Frankivsk': 8, 'Kiev': 9, 'Kirovohrad': 10, 'Lugansk': 11, 'Lviv': 12,
                    'Mykolayiv': 13, 'Odessa': 14, 'Poltava': 15, 'Rivne': 16, 'Sumy': 17, 'Ternopil': 18, 'Kharkiv': 19,
                    'Kherson': 20, 'Khmelnytskyy': 21, 'Cherkasy': 22, 'Chernivtsi': 23, 'Chernihiv': 24, 'Crimea': 25}
        self.region_name = province
        df = pd.read_csv('/home/alexandra/4-sem/Spec_Prog/lab1/data_new_index/vhi_id_' + str(regions.get(province)) + '_' + province + '.csv', index_col=False, header=1)
        df = df.rename(columns={'%Area_VHI_LESS_15': 'VHI<15', '%Area_VHI_LESS_35': 'VHI<35'})
        df['Date'] = df['year'].map(str) + '-' + df['week'].map(str)
        df = df.drop(['year', 'week'], axis=1)
        return df

    def getPlot(self, params):
        df = self.getData(params)
        plt_obj = df.set_index('Date').drop(['SMN', 'SMT', 'VHI<15', 'VHI<35'],axis=1).plot()
        plt_obj.set_ylabel("Index")
        plt_obj.set_title(self.region_name)
        fig = plt_obj.get_figure()
        return fig

app = Global_Vegetation_Health_Products()
app.launch(port=9093)