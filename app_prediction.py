import streamlit as st
from PIL import Image
import pandas as pd
import pickle
import plotly.express as px
import config

class RealEstatePredictor:
    def __init__(self):
        self.model_filename = 'model/model.pkl'
        self.image_filename = 'images/OK2.jpg'
        self.data_filename = 'data_bds/all_bds_clean.csv'
        self.loaded_model = None
        self.city_district_mapping = config.city_district_mapping
        self.types = ['Cho thuê nhà trọ phòng trọ', 'Cho thuê kho nhà xưởng',
                      'Cho thuê văn phòng', 'Cho thuê sang nhượng cửa hàng kiot',
                      'Cho thuê loại bất động sản khác']

    def load_model(self):
        try:
            with open(self.model_filename, 'rb') as file:
                self.loaded_model = pickle.load(file)
        except Exception as e:
            st.error(f"Lỗi khi tải mô hình: {str(e)}")

    def predict_price(self, selected_type, area_value, district, city):
        user_data = pd.DataFrame({'area_value': [area_value], 'district': [district], 'city': [city], 'type': [selected_type]})
        prediction = self.loaded_model.predict(user_data)
        return prediction[0]

    def run(self):
        st.set_page_config(layout="wide")
        self.load_model()

        header_image = Image.open(self.image_filename)
        st.image(header_image, use_column_width=True)

        selected_type = st.selectbox("Chọn loại hình mặt bằng:", self.types)
        selected_city = st.selectbox("Chọn Thành phố:", list(self.city_district_mapping.keys()))
        selected_district = st.selectbox("Chọn Quận:", self.city_district_mapping[selected_city])
        area_value = st.number_input("Diện tích (m2):", min_value=0.0, value=0.0)

        if st.button("Dự đoán"):
            if self.loaded_model is not None:
                try:
                    prediction = self.predict_price(selected_type, area_value, selected_district, selected_city)
                    st.success(f"Dự đoán giá mỗi mét vuông là: {prediction:,.0f} VND")
                    st.success(f"Số tiền thuê một tháng: {area_value * prediction:,.0f} VND")
                except Exception as e:
                    st.error(f"Lỗi khi dự đoán: {str(e)}")
            else:
                st.error("Lỗi: Không thể tải mô hình. Vui lòng kiểm tra lại.")

        df = pd.read_csv(self.data_filename)
        df['district'] = df['district'].replace('·\nQuận', 'Quận', regex=True)
        df['district'] = df['district'].replace('·\nTây Hồ', 'Tây Hồ', regex=True)
        df_median = df.groupby(['city', 'district'])['price_per_m2_final'].mean().reset_index()

        df_hcm = df_median[df_median['city'] == selected_city]

        fig = px.bar(df_hcm, x='district', y='price_per_m2_final', title=f"Biểu đồ giá/m2 theo quận - Thành phố {selected_city}")
        fig.update_layout(xaxis_title='Quận', yaxis_title='Trung vị giá / m2', xaxis_tickangle=-45, width=1200, height=700)
        st.plotly_chart(fig)

if __name__ == '__main__':
    predictor = RealEstatePredictor()
    predictor.run()
