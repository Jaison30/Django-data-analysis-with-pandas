from django.shortcuts import render
from django.views import generic
import pandas as pd

# Create your views here.

highcharts_data = pd.read_json('https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/world-population-density.json')


def get_data_for_map(bar_data, country_names):
    data_for_map = []
    for i in country_names:
        try:
            tempdf = highcharts_data[highcharts_data['name'] == i]
            temp = {}
            temp["code3"] = list(tempdf['code3'].values)[0]
            temp["name"] = i
            temp["value"] = bar_data[bar_data['Country/Region'] == i]['values'].sum()
            temp["code"] = list(tempdf['code'].values)[0]
            data_for_map.append(temp)
        except:
            pass
    return data_for_map


class HomeView(generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data()
        df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
                         encoding='utf-8',
                         na_values=None)
        total_cases = df[df.columns[-1]].sum()
        bar_data = df[['Country/Region', df.columns[-1]]].groupby('Country/Region').sum()
        bar_data = bar_data.reset_index()
        bar_data.columns = ['Country/Region', 'values']
        bar_data = bar_data.sort_values(by='values', ascending=False)
        country_names = bar_data['Country/Region'].values.tolist()
        values = bar_data['values'].values.tolist()
        max_values = max(values)
        data_for_map = get_data_for_map(bar_data, country_names)
        context['total_cases'] = total_cases
        context['country_names'] = country_names
        context['values'] = values
        context['data_for_map'] = data_for_map
        context['max_values'] = max_values
        return context
