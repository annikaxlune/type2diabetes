import base64
import math

import streamlit as st


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


class T2(object):
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

    def set_sidebar(self):
        st.sidebar.header("Press Submit after answering the below questions :")
        self.race = float(self.race_dict[st.sidebar.radio("Your race:", tuple(self.race_dict.keys()), help="Race")])
        self.gender = float(self.sex_dict[st.sidebar.radio("Your gender:", tuple(self.sex_dict.keys()),
                                                           help="Enter your biological gender")])
        # self.age_grp = float(self.age_grp[st.sidebar.radio("Your age group:", tuple(self.age_grp.keys()))])
        self.age_grp = float(self.age_grp[get_ageGrp(st.sidebar.number_input(label="Your age:", min_value=1,
                                                                             max_value=100, step=1))])

        self.LDL_level = float(self.ldl_dict["Yes" if (st.sidebar.slider(label="Your LDL (mg/dL) ?:", min_value=0,
                                                                         max_value=250)) < 150 else "No"])
        # self.hypertension = float(self.ht_dict[st.sidebar.radio("Blood pressure over 140 mmHg ?",
        #                                                         tuple(self.ht_dict.keys()))])

        self.hypertension = float(
            self.ht_dict[get_ht_ind((st.sidebar.number_input("Enter your blood pressure level (mmHg): ",
                                                             min_value=0, max_value=500)))])

        self.trig = float(self.trig_dict[get_trigLevel(st.sidebar.number_input("Enter triglycerides:", ))])
        self.hglycemia = float(self.hg_dict[get_glucoseLevel(st.sidebar.number_input("Glucose level per latest test :",
                                                                                     min_value=90,
                                                                                     max_value=400))])
        self.height = float(
            st.sidebar.number_input('Enter your height in feet:', min_value=2.0, max_value=10.0, step=.25))
        self.weight = float(st.sidebar.number_input("Enter your weight in LBs:", min_value=10.0, max_value=600.0,
                                                    step=.5))
        self.bmi = self.bmi_dict[get_bmiCat(703 * self.weight / ((self.height * 12) ** 2))]

    #         self.bmi = float(
    #             self.bmi_dict[st.sidebar.selectbox("Your bmi level?:", tuple(self.bmi_dict.keys()), help="BMI " \
    #                                                                                                      "Categories: \
    # Underweight = <18.5;  \
    # Normal weight = 18.5–24.9; \n \
    # Overweight = 25–29.9; \n \
    # Obesity = BMI of 30 or greater"
    #                                                )])

    def calc_probability(self):
        s = self.intercept + self.race + self.gender + self.age_grp + self.LDL_level + self.hypertension + self.trig + self.hglycemia \
            + self.bmi
        prob = round(100 / (1 + (1 / math.exp(s))), 2)
        # st.write(f"Sum: {s}")
        original_title = f'<h3 style="color:White; font-size: 20px;">The probability of type II ' \
                         f'diabetes is: <span style=color:Orange>{prob}</span> % </h3>'
        st.markdown(original_title, unsafe_allow_html=True)
        with open('images/dia1.jpg', "rb") as image_file:
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
        c1, c2 = st.columns([1, 5])
        # c1.image()
        title = '<title style="color:White; font-size: 20px;">A project by Dr. Truong and Annika Mondal  </title>'
        st.markdown(title, unsafe_allow_html=True)
        # c2.header("A project by Dr. Truong and Annika Mondal")
        st.write(
            "Check out profile of Annika [link]("
            "www.google.com)")
        st.markdown("""---""")


if __name__ == '__main__':
    t2 = T2()
    t2.set_sidebar()
    t2.set_title_header()
    t2.calc_probability()
