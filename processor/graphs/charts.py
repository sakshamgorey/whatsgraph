
import logging
from typing import Any
from collections import Counter
import numpy as np
import pandas as pd
import plotly.express as px
from textblob import TextBlob
import matplotlib.pyplot as plt





def pie_display_emojis(data_frame: pd.DataFrame):
    total_emojis_list = list(set([a for b in data_frame.emojis for a in b]))
    total_emojis_list = (a for b in data_frame.emojis for a in b)
    emoji_dict = dict(Counter(total_emojis_list))
    emoji_dict = sorted(
        emoji_dict.items(), key=lambda x: x[1], reverse=True)
    emoji_df = pd.DataFrame(emoji_dict, columns=['emojis', 'count'])
    fig = px.pie(emoji_df, values='count', names='emojis')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig


def time_series_plot(data_frame: pd.DataFrame):
    z_value = data_frame['date'].value_counts()
    z_dict = z_value.to_dict()  # converts to dictionary
    data_frame['msg_count'] = data_frame['date'].map(z_dict)
    fig = px.line(x=data_frame['date'], y=data_frame['msg_count'])
    fig.update_layout(
        xaxis_title='Time Stamp',
        yaxis_title='Number of Messages')
    fig.update_xaxes(nticks=60)
    return fig


def plot_data(data_string):
    fig, ax_value = plt.subplots()
    bars = ax_value.bar(
        x=np.arange(data_string.get('x_value')),
        height=data_string.get('y_value'),
        tick_label=data_string.get('tick_label'),
        color="#0077b6"
    )
    ax_value.spines['top'].set_visible(False)
    ax_value.spines['right'].set_visible(False)
    ax_value.spines['left'].set_visible(False)
    ax_value.spines['bottom'].set_color('#0077b6')
    ax_value.tick_params(bottom=False, left=False)
    ax_value.tick_params(axis='x', labelrotation=90)
    ax_value.set_axisbelow(True)
    ax_value.yaxis.grid(True, color='#EEEEEE')
    ax_value.xaxis.grid(False)
    # Grab the color of the bars so we can make the
    # text the same color.
    # bar_color = bars[0].get_facecolor()
    # Add text annotations to the top of the bars.
    # Note, you'll have to adjust this slightly (the 0.3)
    # with different data.
    for bar_value in bars:
        ax_value.text(
            bar_value.get_x() + bar_value.get_width() / 2,
            bar_value.get_height(),
            round(bar_value.get_height(), 1),
            horizontalalignment='center',
            color='green',  # bar_color
            # weight='bold'
        )
    ax_value.set_xlabel(
        data_string.get('x_label'), labelpad=15, color='#333333')
    ax_value.set_ylabel(
        data_string.get('y_label'), labelpad=15, color='#333333')
    ax_value.set_title(
        data_string.get('title'), pad=15, color='#333333')
    return fig


def max_words_used(data_frame: pd.DataFrame):
    
    logging.info("WhatsApp/max_words_used()")
   
    max_words = data_frame[['name', 'word_count']].groupby('name').sum()
    m_w = max_words.sort_values('word_count', ascending=False).head(10)
    return plot_data({
            'x_value': m_w.size,
            'y_value': m_w.word_count,
            'tick_label': m_w.index,
            'x_label': 'Name of Group Member',
            'y_label': 'Number of Words in Group Chat',
           
        })


def most_active_member(data_frame: pd.DataFrame):

    logging.info("WhatsApp/most_active_member()")
    mostly_active = data_frame['name'].value_counts()
    # Top 10 peoples that are mostly active in our Group
    m_a = mostly_active.head(20)
    return plot_data({
            'x_value': m_a.size,
            'y_value': m_a,
            'tick_label': m_a.index,
            'x_label': 'Name of Group Member',
            'y_label': 'Number of Group Messages',
            
        })


def most_active_day(data_frame: pd.DataFrame):
    logging.info("WhatsApp/most_active_day()")
    active_day = data_frame['day'].value_counts()
    a_d = active_day.head(10)
    return plot_data({
            'x_value': a_d.size,
            'y_value': a_d,
            'tick_label': a_d.index,
            'x_label': 'Name of Group Member',
            'y_label': 'Number of Group Messages',
            
        })


def top_media_contributor(data_frame: pd.DataFrame):

    logging.info("WhatsApp/top_media_contributor()")
    max_media = data_frame[['name', 'media']].groupby('name').sum()
    m_m = max_media.sort_values(
        'media', ascending=False).head(10)
    return plot_data({
            'x_value': m_m.size,
            'y_value': m_m.media,
            'tick_label': m_m.index,
            'x_label': 'Name of Group Member',
            'y_label': 'Number of Media Shared in Group',
        
        })


def who_shared_links(data_frame: pd.DataFrame):
    logging.info("WhatsApp/who_shared_links()")

    max_words = data_frame[['name', 'urlcount']].groupby('name').sum()
    m_w = max_words.sort_values('urlcount', ascending=False).head(10)
    return plot_data({
            'x_value': m_w.size,
            'y_value': m_w.urlcount,
            'tick_label': m_w.index,
            'x_label': 'Name of Group Member',
            'y_label': 'Number of Links Shared in Group'
        })


def time_when_group_active(data_frame: pd.DataFrame):

    logging.info("WhatsApp/time_when_group_active()")
    active_time = data_frame.datetime.dt.time.value_counts().head(10)
    return plot_data({
            'x_value': active_time.size,
            'y_value': active_time.values,
            'tick_label': active_time.index,
            'x_label': 'Time',
            'y_label': 'Number of Messages',
            'title': 'Analysis of time when group was highly active'
        })


def most_suitable_hour(data_frame: pd.DataFrame):
    logging.info("WhatsApp/most_suitable_hour()")
    active_hour = data_frame.datetime.dt.hour.value_counts().head(20)
    return plot_data({
            'x_value': active_hour.size,
            'y_value': active_hour.values,
            'tick_label': active_hour.index,
            'x_label': 'Hour',
            'y_label': 'Number of Messages',
            'title': 'Analysis of hour when group was highly active'
        })


def most_suitable_day(data_frame: pd.DataFrame):
    logging.info("WhatsApp/most_suitable_day()")
    active_day = data_frame.datetime.dt.day.value_counts().head(20)
    return plot_data({
            'x_value': active_day.size,
            'y_value':  active_day.values,
            'tick_label': active_day.index,
            'x_label': 'Day',
            'y_label': 'Number of Messages',
            'title': 'Analysis of Day when group was highly active'
        })


