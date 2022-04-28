import re
import os
import time
import warnings
import logging
import logging.config
import yaml
from typing import Dict, Any
import streamlit as st
from numpy import sum as npsum
import matplotlib.pyplot as plt
from processor.transformers.chat_eda import WhatsAppProcess, sorted_authors_df,\
    statistics, process_data, WhatsAppConfig
from processor.graphs.charts import pie_display_emojis, time_series_plot,\
   most_active_member, most_active_day,max_words_used, top_media_contributor, who_shared_links,most_suitable_day, most_suitable_hour

st.set_page_config(page_title="Whatsgraph",page_icon='💬')
st.title("Whatsgraph💬")
st.header("Your messages as stats")
def display_statistics(stats):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "Total Messages", stats.get('total_messages'))
    col2.metric(
        "Total Members", stats.get('total_members'))
    col3.metric(
        "Total Media", stats.get('media_message'))
    col4.metric(
        "Link shared", int(stats.get('link_shared')))
    st.text("")
    


def chart_display(data_frame):
    st.header("How much time is spent here?⏰")
    st.write(time_series_plot(data_frame))

    st.header("Who is the Most Active Member?📈")
    st.pyplot(most_active_member(data_frame))

        
    st.header("Which day is the Most Active Day?⌛")
    st.pyplot(most_active_day(data_frame))

        
    st.header("Who uses most words in sentences?🔤")
    st.pyplot(max_words_used(data_frame))

        
    st.header("Who shares the most links?🔗 ")
    st.pyplot(who_shared_links(data_frame))

        
    st.header("Which is the Most Active Day in month?🗓️")
    st.pyplot(most_suitable_day(data_frame))

        
    st.header("Which is the Most Active Hour?⌚")
    st.pyplot(most_suitable_hour(data_frame))

    st.header("Curious about Emoji's ?")
    pie_display = pie_display_emojis(data_frame)
    st.plotly_chart(pie_display)


def file_process(data, config):
    """
    Regex passed message format frocessing function
    """
    # reading source configuration
    source_config = WhatsAppConfig(**config['whatsapp'])
    whatsapp = WhatsAppProcess(source_config)
    message = whatsapp.apply_regex(data)
    raw_df = process_data(message)
    data_frame = whatsapp.get_dataframe(raw_df)
    stats = statistics(raw_df, data_frame)

    st.markdown(f'# {stats.get("group_name")}')
    display_statistics(stats)
    cloud_df = whatsapp.cloud_data(raw_df)
    st.header("Individuals Stats")
    sorted_authors = sorted_authors_df(cloud_df)
    select_author = []
    select_author.append(st.selectbox('', sorted_authors))
    dummy_df = cloud_df[cloud_df['name'] == select_author[0]]
    text = " ".join(review for review in dummy_df.message)

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Posted Messages",
        dummy_df[dummy_df['name'] == select_author[0]].shape[0])
    col2.metric(
        "Emoji's Shared", sum(
            data_frame[data_frame.name.str.contains(
                select_author[0][-5:])].emojis.str.len()))
    col3.metric("Link Shared", int(
        data_frame[data_frame.name == select_author[0]].urlcount.sum()))
    col4.metric("Total Words", int(
        data_frame[data_frame.name == select_author[0]].word_count.sum()))
    user_df = data_frame[data_frame.name.str.contains(
        select_author[0][-5:])]
    average = round(npsum(user_df.word_count)/user_df.shape[0], 2)
    col5.metric("Average words/Message", average)
    whatsapp.day_analysis(data_frame)
    chart_display(data_frame)

        
    st.header("Who is the top Media Contributor?")
    st.pyplot(top_media_contributor(raw_df))
    st.header("Whatsgraph💬 V1.0 log")
    st.text(''' 
    version 1 of Whatsgraph contains basic graphing functions
    In version 2 we would like to do sentiment,toxicty analysis
    and improve on the graphing capabilities 
    ''')
    st.text(''' 
    Project for Data Science
    built by
    Saksham Gorey - 19124043
    Shreesh - 19124051
    Bansi Parekhiya- 19124071
    ''')

def main():
    config = 'configs/app_configuration.yml'
    config = yaml.safe_load(open(config))
    log_config = config['logging']
    logging.config.dictConfig(log_config)
    logger = logging.getLogger(__name__)

    c1, c2 = st.columns([3, 1])

    uploaded_file = c1.file_uploader(
        "Choose a TXT file only",
        type=['txt'],
        accept_multiple_files=False)

    if uploaded_file is not None:
        data = uploaded_file.getvalue().decode("UTF8")
        file_process(data, config)
        

if __name__ == "__main__":
    main()
