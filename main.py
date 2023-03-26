import math

import streamlit as st


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

    def set_sidebar(self):
        st.sidebar.header("Press Submit after answering the below questions :")
        self.race = float(self.race_dict[st.sidebar.radio("Your race:", tuple(self.race_dict.keys()), help="Race")])
        self.gender = float(self.sex_dict[st.sidebar.radio("Your gender:", tuple(self.sex_dict.keys()))])
        self.age_grp = float(self.age_grp[st.sidebar.radio("Your age group:", tuple(self.age_grp.keys()))])
        self.LDL_level = float(self.ldl_dict["Yes" if (st.sidebar.slider(label="Your LDL (mg/dL) ?:", min_value=0,
                                                                         max_value=250)) < 150 else "No"])
        self.hypertension = float(self.ht_dict[st.sidebar.radio("You have hypertension?:", tuple(self.ht_dict.keys()))])
        self.trig = float(self.trig_dict[st.sidebar.radio("You have trig?:", tuple(self.trig_dict.keys()))])
        self.hglycemia = float(self.hg_dict[st.sidebar.radio("You have hyperglycemia?:", tuple(self.hg_dict.keys()))])
        self.bmi = float(
            self.bmi_dict[st.sidebar.selectbox("Your bmi level?:", tuple(self.bmi_dict.keys()), help="BMI is "
                                                                                                     "measured as weight over squared-height"
                                                                                                     "")])

    def calc_probability(self):
        s = self.intercept + self.race + self.gender + self.age_grp + self.LDL_level + self.hypertension + self.trig + self.hglycemia \
            + self.bmi
        prob = round(100 / (1 + (1 / math.exp(s))), 2)
        # st.write(f"Sum: {s}")
        original_title = f'<h3 style="color:Grey; font-size: 20px;">The probability of type II ' \
                         f'diabetes is: <span style=color:Orange>{prob}</span> % </h3>'
        st.markdown(original_title, unsafe_allow_html=True)
        st.markdown("""---""")

    def set_title_header(self):
        c1, c2 = st.columns([1, 5])
        # c1.image()
        c2.header("A project by Dr. Truong and Annika Mondal")
        st.write(
            "Check out profile of Annika [link]("
            "www.google.com)")
        st.markdown("""---""")


if __name__ == '__main__':
    t2 = T2()
    t2.set_sidebar()
    t2.set_title_header()
    t2.calc_probability()
