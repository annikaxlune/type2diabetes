import base64
import math
import random
from glob import glob

import streamlit as st
from pathlib import Path

columnColor = "orange"


def add_bg_from_url():
    background_img = """
    <style>
            [data-testid="stAppViewContainer"]{
            background-image: url("data:image/png;base64,%s");
            background-size: cover;
        }
        [data-testid="stHeader"]{
        background-color: rgb(191, 87, 0);
        text : "Hello"
        }
    </style>
    """ % img_to_bytes("images/pexels-nataliya-vaitkevich-6941883.jpg");
    st.markdown(
        background_img,
        unsafe_allow_html=True
    )
    st.markdown("""[data - testid = "stHeader"][Hello!!]""",unsafe_allow_html=True)


def get_ageGrp(age):
    if age < 18:
        return '< 18'
    elif age >= 18 and age <= 29:
        return '18-29'
    elif age >= 30 and age <= 39:
        return '30-39'
    elif age >= 40 and age <= 49:
        return '40-49'
    elif age >= 50 and age <= 64:
        return '50-64'
    elif age >= 65:
        return '65+'


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def get_trigLevel(param):
    return "No" if param < 199 else "Yes"  # clarify - what qualifies Yes


def get_glucoseLevel(param):
    return "No" if param <= 140 else "Yes"  # clarify - what qualifies Yes


def get_bmiCat(param):
    if param < 18.5:
        return "Underweight: Less than 18.5"
    elif param > 18.5 and param > 24.9:
        return "Optimum range: 18.5 to 24.9"
    elif param > 25 and param > 29.9:
        return "Overweight: 25 to 29.9"
    elif param > 30 and param > 34.9:
        return "Class I obesity: 30 to 34.9"
    elif param > 35 and param > 39.9:
        return "Class II obesity: 35 to 39.9"
    else:
        return "Class III obesity: More than 40"


def get_ht_ind(param):
    return "Yes" if param > 140 else "No"


def header(url):
    # st.markdown(f'<p style="background-color:pink;color:#33ff33;font-size:48px;border-radius:2%;">{url}</p>',
    #             unsafe_allow_html=True)
    st.markdown(
        f'<p style="font-size:35px;font-weight: 600;background-image: linear-gradient(toleft,#553c9a, '
        f'#b393d3);color: pink;">{url}</p>',
        unsafe_allow_html=True)


def write(text, color="blue"):
    st.markdown(f'<p style="color:{color};font-size:15px;border-radius:2%;">{text}</p>',
                unsafe_allow_html=True)


def title(param):
    st.markdown(
        f'<p style="font-size:95px;font-weight: 600;background-image: linear-gradient(toleft,#553c9a, '
        f'#b393d3);color: purple;">{param}</p>',
        unsafe_allow_html=True)


def displayPDF(file):
    # Opening file from file path. this is used to open the file from a website rather than local
    with open(file, 'rb') as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="1000" height="950" ' \
                  f'type="application/pdf"></iframe>'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)


class Diabetes(object):
    def __init__(self):
        self.intercept = -5.2959
        self.sex_dict = {'Female': -0.2132, 'Male': 0}
        self.race_dict = {'White': 0,
                          'Black': 0.4573,
                          'Asian': 0.6543,
                          'Hispanic': 0.6674,
                          'Unknown': 0.3682
                          }
        self.age_grp = {'< 18': -1.7414,
                        '18-29': 0,
                        '30-39': 0.7857,
                        '40-49': 1.4746,
                        '50-64': 2.0259,
                        '65+': 2.4531}
        self.ldl_dict = {"Yes": 0.1744, "No": 0}
        self.ht_dict = {"Yes": 1.660, "No": 0}
        self.trig_dict = {"Yes": 0.7368, "No": 0}
        self.hg_dict = {"Yes": 0.6169, "No": 0}
        self.bmi_dict = {"Underweight: Less than 18.5": 0.4982,
                         "Optimum range: 18.5 to 24.9": 0,
                         "Overweight: 25 to 29.9": 0.2816,
                         "Class I obesity: 30 to 34.9": 0.6674,
                         "Class II obesity: 35 to 39.9": 1.0161,
                         "Class III obesity: More than 40": 1.231
                         }
        # st.image('images/dia1.jpg')

    def set_columns(self):
        st.header("Press Submit after answering the below questions :")
        col1, col2, col3 = st.columns(3)
        with col1:
            # st.write("Demographic information")
            self.race = float(self.race_dict[st.radio(f":{columnColor}[**Your race:**]", tuple(self.race_dict.keys()),
                                                      help=f":{columnColor}[**Race**]",
                                                      )])
            self.gender = float(self.sex_dict[st.radio(f":{columnColor}[**Your gender:**]",
                                                       tuple(self.sex_dict.keys()),
                                                       help=f":{columnColor}[**Enter your biological gender:**]")])
            # self.age_grp = float(self.age_grp[st.radio("Your age group:", tuple(self.age_grp.keys()))])
            c1, c2, c3 = st.columns(3)
            with c1:
                self.age_grp = float(self.age_grp[get_ageGrp(st.number_input(label=f":{columnColor}[**Your age:**]",
                                                                             value=35, min_value=1,
                                                                             max_value=100, step=1))])

        # self.hypertension = float(self.ht_dict[st.radio("Blood pressure over 140 mmHg ?",
        #                                                         tuple(self.ht_dict.keys()))])
        with col2:
            c1, c2, c3 = st.columns(3)
            with c1:
                self.LDL_level = float(self.ldl_dict["Yes" if (st.slider(label=f":{columnColor}[**Your LDL (mg/dL) "
                                                                               "?:**]", min_value=0,
                                                                         max_value=250)) < 150 else "No"])
                self.hypertension = float(
                    self.ht_dict[get_ht_ind((st.number_input(f":{columnColor}[**Enter your blood pressure level ("
                                                             "mmHg):**] ",
                                                             value=120, min_value=0, max_value=500)))])

                self.trig = float(self.trig_dict[get_trigLevel(st.number_input(f":{columnColor}[**Enter "
                                                                               "triglycerides:**]", value=90))])

        with col3:
            c1, c2, c3 = st.columns(3)
            with c1:
                self.hglycemia = float(self.hg_dict[get_glucoseLevel(
                    st.number_input(f":{columnColor}[**Glucose level per latest test :**]",
                                    min_value=90,
                                    max_value=400))])
                self.height = float(
                    st.number_input(f":{columnColor}[**Enter your height in feet:**]", min_value=2.0, max_value=10.0,
                                    step=.25))
                self.weight = float(st.number_input(f":{columnColor}[**Enter your weight in LBs:**]", min_value=10.0,
                                                    max_value=600.0,
                                                    step=.5))
                self.bmi = self.bmi_dict[get_bmiCat(703 * self.weight / ((self.height * 12) ** 2))]

    def calc_probability(self):
        s = self.intercept + self.race + self.gender + self.age_grp + self.LDL_level + self.hypertension + self.trig + self.hglycemia \
            + self.bmi
        prob = round(100 / (1 + (1 / math.exp(s))), 2)
        # st.write(f"Sum: {s}")
        # original_title = f'<h3 style="color:black; font-size: 20px;">The probability of type II ' \
        #                  f'diabetes is: <span style=color:Orange>{prob}</span> % </h3>'
        # st.markdown(original_title, unsafe_allow_html=True)
        # self.show_image()
        self.result = prob

    def show_bg_image(self):
        with open(random.choice(glob('images/*')), "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        st.markdown(
            f"""
        <style>
          .stApp
        {{
            background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style >
        """,
            unsafe_allow_html=True)
        st.markdown("""---""")

    def set_title_header(self):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<h2 style='text-align: right; color: rgb(191, 87, 0);'>PREDICTIVE MODEL FOR CALCULATING "
                        "INDIVIDUAL'S RISK OF TYPE 2 DIABETES</h2>",
                        unsafe_allow_html=True)
        with c2:
            st.markdown(
                '''[<img src='data:image/png;base64,{}' class='img-fluid' width=128 height=128 style="float:right">](
                https://sph.uth.edu/campuses/houston)'''.format(
                    img_to_bytes("images/UTHealth_SPH_Logo.jpg")), unsafe_allow_html=True)


if __name__ == '__main__':
    # streamlit_style = """
    # 			<style>
    # 			@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap');
    # 			html, body, [class*="css"]  {
    # 			font-family: 'Roboto', sans-serif;
    # 			}
    # 			</style>
    # 			"""
    # st.markdown(streamlit_style, unsafe_allow_html=True)
    # st.set_page_config(layout="wide")
    st.set_page_config(
        page_title='Type 2 Diabetes',
        layout="wide",
        initial_sidebar_state="expanded",
    )
    css = r'''
        <style>
            [data-testid="stForm"] {border: 0px}
        </style>
    '''
    # add_bg_from_url()

    st.markdown(css, unsafe_allow_html=True)
    diabetes = Diabetes()
    diabetes.set_title_header()

    expander = st.expander(label=f"**Find out probability of having diabetes**",expanded=True)
    with expander:
        with st.form(key="my_form"):
            diabetes.set_columns()
            submit_button = st.form_submit_button(label='Submit', on_click=diabetes.calc_probability())
            # write(submit_button)
        write(f"The probability of having type 2 diabetes : {round(diabetes.result, 2)}%", "green" if float(
            diabetes.result) < .5 else
        "red")

    # with diabetes.tab3:
    with st.expander(f"**Project Detail**"):
        displayPDF('resources/t2dposter_v1.pdf')
