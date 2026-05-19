# ==========================================
# IMPORTAR LIBRERÍAS
# ==========================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ==========================================
# CONFIGURACIÓN GENERAL
# ==========================================

st.set_page_config(
    page_title="Customer Churn Analytics Dashboard",
    layout="wide"
)


# ==========================================
# ESTILO GENERAL
# ==========================================

sns.set_style("darkgrid")


# ==========================================
# CLASE POO
# ==========================================

class DataAnalyzer:

    def __init__(self, df):
        self.df = df

    def info_dataset(self):

        info = pd.DataFrame({
            "Tipo de dato": self.df.dtypes,
            "Valores nulos": self.df.isnull().sum()
        })

        return info

    def variables_numericas(self):

        return self.df.select_dtypes(include=np.number).columns.tolist()

    def variables_categoricas(self):

        return self.df.select_dtypes(include='object').columns.tolist()

    def estadisticas(self):

        return self.df.describe()

    def valores_faltantes(self):

        return self.df.isnull().sum()


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("📌 Menú de Navegación")

menu = st.sidebar.radio(
    "Selecciona una sección",
    [
        "Home",
        "Carga Dataset",
        "EDA",
        "Conclusiones"
    ]
)


# ==========================================
# HOME
# ==========================================

if menu == "Home":

    st.title("📊 Customer Churn Analytics Dashboard")

    st.write("""
    Esta aplicación interactiva permite realizar un análisis exploratorio
    de datos (EDA) sobre clientes de una empresa de telecomunicaciones,
    con el objetivo de identificar patrones asociados a la fuga de clientes.
    """)

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        label="📂 Dataset",
        value="Telco Churn"
    )

    col2.metric(
        label="📊 Variables",
        value="21"
    )

    col3.metric(
        label="🎯 Objetivo",
        value="EDA"
    )

    st.divider()

    st.subheader("👨‍💻 Datos del Autor")

    st.write("""
    - Nombre: Miguel Angel Pizarro Huaraca
    - Curso: Python for Analytics
    - Año: 2026
    """)

    st.subheader("📊 Descripción del Dataset")

    st.write("""
    El dataset contiene información sobre clientes,
    servicios contratados, tiempo de permanencia,
    facturación mensual y estado de abandono.
    """)

    st.subheader("🛠️ Tecnologías Utilizadas")

    st.write("""
    - Python
    - Pandas
    - NumPy
    - Matplotlib
    - Seaborn
    - Streamlit
    """)


# ==========================================
# CARGA DEL DATASET
# ==========================================

elif menu == "Carga Dataset":

    st.title("📂 Carga del Dataset")

    archivo = st.file_uploader(
        "Sube el archivo CSV",
        type=["csv"]
    )

    if archivo is not None:

        df = pd.read_csv(archivo)

        st.success("✅ Dataset cargado correctamente")

        st.subheader("Vista previa del Dataset")

        st.dataframe(df.head())

        filas, columnas = df.shape

        col1, col2 = st.columns(2)

        col1.metric("📄 Filas", filas)
        col2.metric("📑 Columnas", columnas)

    else:

        st.warning("⚠️ Por favor, carga un archivo CSV")


# ==========================================
# EDA
# ==========================================

elif menu == "EDA":

    st.title("📊 Análisis Exploratorio de Datos (EDA)")

    archivo = st.file_uploader(
        "Carga el dataset para iniciar el análisis",
        type=["csv"]
    )

    if archivo is not None:

        df = pd.read_csv(archivo)

        analyzer = DataAnalyzer(df)

        tabs = st.tabs([
            "Información General",
            "Clasificación Variables",
            "Estadísticas",
            "Valores Faltantes",
            "Distribución Numéricas",
            "Variables Categóricas",
            "Numérico vs Categórico",
            "Categórico vs Categórico",
            "Análisis Dinámico",
            "Hallazgos"
        ])


        # ==========================================
        # TAB 1
        # ==========================================

        with tabs[0]:

            st.subheader("📋 Información General del Dataset")

            st.dataframe(analyzer.info_dataset())


        # ==========================================
        # TAB 2
        # ==========================================

        with tabs[1]:

            st.subheader("📌 Clasificación de Variables")

            numericas = analyzer.variables_numericas()
            categoricas = analyzer.variables_categoricas()

            col1, col2 = st.columns(2)

            with col1:

                st.write("### 🔢 Variables Numéricas")
                st.write(numericas)
                st.write(f"Cantidad: {len(numericas)}")

            with col2:

                st.write("### 🔤 Variables Categóricas")
                st.write(categoricas)
                st.write(f"Cantidad: {len(categoricas)}")


        # ==========================================
        # TAB 3
        # ==========================================

        with tabs[2]:

            st.subheader("📈 Estadísticas Descriptivas")

            st.dataframe(analyzer.estadisticas())

            st.info("""
            Las estadísticas descriptivas permiten analizar
            el comportamiento general de las variables numéricas.
            """)


        # ==========================================
        # TAB 4
        # ==========================================

        with tabs[3]:

            st.subheader("⚠️ Análisis de Valores Faltantes")

            missing = analyzer.valores_faltantes()

            st.dataframe(missing)

            fig, ax = plt.subplots(figsize=(10,5))

            missing.plot(
                kind='bar',
                color='orange',
                ax=ax
            )

            ax.set_title("Valores Faltantes por Variable")

            plt.xticks(rotation=90)

            st.pyplot(fig)


        # ==========================================
        # TAB 5
        # ==========================================

        with tabs[4]:

            st.subheader("📊 Distribución de Variables Numéricas")

            numericas = analyzer.variables_numericas()

            variable = st.selectbox(
                "Selecciona una variable numérica",
                numericas
            )

            fig, ax = plt.subplots(figsize=(8,5))

            sns.histplot(
                df[variable],
                kde=True,
                color="skyblue",
                edgecolor="black",
                ax=ax
            )

            ax.set_title(f"Distribución de {variable}")
            ax.set_xlabel(variable)
            ax.set_ylabel("Frecuencia")

            st.pyplot(fig)


        # ==========================================
        # TAB 6
        # ==========================================

        with tabs[5]:

            st.subheader("📌 Análisis de Variables Categóricas")

            categoricas = analyzer.variables_categoricas()

            variable_cat = st.selectbox(
                "Selecciona una variable categórica",
                categoricas
            )

            fig, ax = plt.subplots(figsize=(8,5))

            sns.countplot(
                data=df,
                x=variable_cat,
                palette="viridis",
                ax=ax
            )

            ax.set_title(f"Distribución de {variable_cat}")
            ax.set_xlabel(variable_cat)
            ax.set_ylabel("Cantidad")

            plt.xticks(rotation=45)

            st.pyplot(fig)


        # ==========================================
        # TAB 7
        # ==========================================

        with tabs[6]:

            st.subheader("📉 Análisis Numérico vs Categórico")

            fig, ax = plt.subplots(figsize=(8,5))

            sns.boxplot(
                data=df,
                x="Churn",
                y="MonthlyCharges",
                palette="Set2",
                ax=ax
            )

            ax.set_title("Monthly Charges vs Churn")

            st.pyplot(fig)


        # ==========================================
        # TAB 8
        # ==========================================

        with tabs[7]:

            st.subheader("📊 Análisis Categórico vs Categórico")

            fig, ax = plt.subplots(figsize=(8,5))

            sns.countplot(
                data=df,
                x="Contract",
                hue="Churn",
                palette="coolwarm",
                ax=ax
            )

            ax.set_title("Contract vs Churn")

            plt.xticks(rotation=45)

            st.pyplot(fig)


        # ==========================================
        # TAB 9
        # ==========================================

        with tabs[8]:

            st.subheader("🎛️ Análisis Dinámico")

            col1, col2 = st.columns(2)

            with col1:

                genero = st.multiselect(
                    "Selecciona Género",
                    options=df["gender"].unique(),
                    default=df["gender"].unique()
                )

            with col2:

                contrato = st.selectbox(
                    "Selecciona Tipo de Contrato",
                    options=df["Contract"].unique()
                )

            rango_tenure = st.slider(
                "Selecciona rango de permanencia (tenure)",
                int(df["tenure"].min()),
                int(df["tenure"].max()),
                (
                    int(df["tenure"].min()),
                    int(df["tenure"].max())
                )
            )

            filtrado = df[
                (df["gender"].isin(genero)) &
                (df["Contract"] == contrato) &
                (df["tenure"] >= rango_tenure[0]) &
                (df["tenure"] <= rango_tenure[1])
            ]

            st.write("### Dataset Filtrado")

            st.dataframe(filtrado)

            st.write(f"Cantidad de registros filtrados: {filtrado.shape[0]}")


        # ==========================================
        # TAB 10
        # ==========================================

        with tabs[9]:

            st.subheader("🔍 Hallazgos Clave")

            st.success("""
            ✅ Los clientes con contratos mensuales presentan mayor churn.
            """)

            st.info("""
            📌 Los clientes nuevos presentan mayor probabilidad de abandono.
            """)

            st.warning("""
            ⚠️ Los clientes con mayores cargos mensuales presentan mayor fuga.
            """)

            st.success("""
            ✅ Los clientes con mayor permanencia tienden a mantenerse en la empresa.
            """)

    else:

        st.warning("⚠️ Debes cargar un dataset para ejecutar el análisis")


# ==========================================
# CONCLUSIONES
# ==========================================

elif menu == "Conclusiones":

    st.title("📌 Conclusiones Finales")

    st.success("""
    1. Los contratos mensuales presentan mayores tasas de abandono.
    """)

    st.info("""
    2. Los clientes con poca antigüedad son más propensos a abandonar la empresa.
    """)

    st.warning("""
    3. Los clientes con cargos mensuales elevados muestran mayor churn.
    """)

    st.success("""
    4. El servicio de fibra óptica presenta una mayor proporción de fuga.
    """)

    st.info("""
    5. La retención de clientes resulta más rentable que la adquisición de nuevos clientes.
    """)