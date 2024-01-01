from pycaret.classification import *
import streamlit as st


@st.cache_data(ttl=3600)
def build_model(data, model_choice):
    setup(data=data, target="Target")
    st.dataframe(pull(), hide_index=True, use_container_width=True)
    mod = create_model(model_choice,return_train_score=True)
    evaluate_model(mod)
    st.dataframe(pull(), use_container_width=True)
    plot_model(mod, plot='confusion_matrix', display_format='streamlit')
    plot_model(mod, plot='auc', display_format='streamlit')
    plot_model(mod, plot='feature', display_format='streamlit', save=True)


@st.cache_data(ttl=3600)
def compare_model(data):
    # Initialize PyCaret setup
    setup(data=data, target="Target")
    st.dataframe(pull(), hide_index=True, use_container_width=True)
    best_model = compare_models()
    st.dataframe(pull(), hide_index=True, use_container_width=True)
    save_model(best_model, 'best_model')

    # Create and plot the best model
    plot_model(best_model, plot='auc')
    plot_model(best_model, plot='confusion_matrix')
    plot_model(best_model, plot='feature')
