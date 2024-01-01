from upload import *
from model import *
from streamlit_pandas_profiling import st_profile_report
from ydata_profiling import ProfileReport
import os


# Check if dataset.csv exists in the current directory
if os.path.exists('./dataset.csv'):
    df = pd.read_csv('dataset.csv', index_col=None)
else:
    df = pd.DataFrame()  # Initialize an empty DataFrame if dataset.csv doesn't exist

with st.sidebar:
    st.image("https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png")
    st.title("BioTech")
    choice = st.radio("Navigation", ["Upload",
                                     "Profiling", "Modelling", "Download"])
    st.info("This project application helps you build and explore your data.")

# Choice handling
if choice == "Upload":
    st.title("Data Input")
    st.markdown("Preprocessing the datasets")
    file = st.file_uploader("Upload your OTU, Tax and Metadata Tables", accept_multiple_files=True)
    if file:
        uploaded_files = {obj.name: obj for obj in file}

        with st.expander("Choose the OTU table"):
            otu_filename = st.radio("Select OTU table:", list(uploaded_files.keys()))

        with st.expander("Choose the tax table"):
            tax_filename = st.radio("Select tax table:", list(uploaded_files.keys()))

        with st.expander("Choose the metadata table"):
            metadata_filename = st.radio("Select metadata table:", list(uploaded_files.keys()))

        if st.toggle("Upload"):
            df = process_csv(uploaded_files[otu_filename])
            tax = process_csv(uploaded_files[tax_filename])
            metadata = pd.read_csv(uploaded_files[metadata_filename], sep="\t")
            metadata.rename(columns={metadata.columns[0]: "Sample"}, inplace=True)
            with st.form("Transform"):
                st.header("Merging the datasets")
                choice_of_index = st.selectbox('Choose your index', list(tax.columns))
                target = st.selectbox('Choose your target', list(metadata.columns))
                if st.form_submit_button("Transform"):
                    df = merge_operations(df, tax)
                    df = drop_columns(df, list(tax.columns), choice_of_index)
                    df = merge_operations(df, metadata[['Sample', target]])
                    df = df.rename(columns={target: 'Target'})
                    del metadata
                    del tax
                    df.set_index('Sample', inplace=True)
                    df.to_csv('dataset.csv')
                    st.header("Final Dataset")
                    st.dataframe(df, use_container_width=True)

elif choice == "Profiling":
    st.title("Exploratory Data Analysis")
    if not df.empty:
        profile_df = ProfileReport(df, progress_bar=True)
        st_profile_report(profile_df)
    else:
        st.warning("Please upload a dataset first!")

elif choice == "Modelling":
    st.title("Predictive Modeling")
    st.markdown("Choose whether to build a custom classification model or compare classification models")
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        classification = st.radio("Choice of Build", ['Custom Model', "Compare Models"], horizontal=True)
        if classification == "Custom Model":
            classifiers = {
                'Logistic Regression': 'lr',
                'K Neighbors Classifier': 'knn',
                'Naive Bayes': 'nb',
                'Decision Tree Classifier': 'dt',
                'SVM - Linear Kernel': 'svm',
                'SVM - Radial Kernel': 'rbfsvm',
                'Gaussian Process Classifier': 'gpc',
                'MLP Classifier': 'mlp',
                'Ridge Classifier': 'ridge',
                'Random Forest Classifier': 'rf',
                'Quadratic Discriminant Analysis': 'qda',
                'Ada Boost Classifier': 'ada',
                'Gradient Boosting Classifier': 'gbc',
                'Linear Discriminant Analysis': 'lda',
                'Extra Trees Classifier': 'et',
                'Extreme Gradient Boosting': 'xgboost',
                'Light Gradient Boosting Machine': 'lightgbm',
                'CatBoost Classifier': 'catboost'
            }

            choice_of_model = st.selectbox('Choose the predictive model', list(classifiers.keys()))
            if st.button('Run Modelling'):
                if choice_of_model:
                    if st.toggle("Include Cross Validation"):
                        build_model(df, classifiers[choice_of_model], True)
                    else:
                        build_model(df, classifiers[choice_of_model], False)

        if classification == "Compare Models":
            if st.button('Run Modelling'):
                compare_model(df)
    else:
        st.warning("Please upload a dataset first!")

elif choice == "Download":
    if os.path.exists('best_model.pkl'):
        with open('best_model.pkl', 'rb') as f:
            st.download_button('Download Model', f, file_name="best_model.pkl")
    else:
        st.warning("No model file found to download!")
