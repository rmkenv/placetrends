import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def load_csv(url):
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Failed to load CSV: {e}")
        return None

def main():
    st.title("Customizable Interactive Dashboard")
    
    # Step 1: Input GitHub URL
    st.sidebar.header("Step 1: Provide GitHub CSV URL")
    github_url = st.sidebar.text_input(
        "Enter the URL of the CSV file hosted on GitHub:",
        value="https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv",
    )

    if github_url:
        df = load_csv(github_url)

        if df is not None:
            # Step 2: Select columns to display
            st.sidebar.header("Step 2: Select Headers")
            headers = st.sidebar.multiselect(
                "Choose columns to include:",
                options=df.columns.tolist(),
                default=df.columns.tolist()
            )

            if headers:
                filtered_df = df[headers]
                st.write("### Filtered Data")
                st.dataframe(filtered_df)

                # Step 3: Data filtering
                st.sidebar.header("Step 3: Filter Data")
                for col in headers:
                    if pd.api.types.is_numeric_dtype(df[col]):
                        min_val, max_val = st.sidebar.slider(
                            f"Filter {col} range:",
                            float(df[col].min()),
                            float(df[col].max()),
                            (float(df[col].min()), float(df[col].max()))
                        )
                        filtered_df = filtered_df[(filtered_df[col] >= min_val) & (filtered_df[col] <= max_val)]
                    elif pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_categorical_dtype(df[col]):
                        unique_values = df[col].dropna().unique().tolist()
                        selected_values = st.sidebar.multiselect(
                            f"Filter {col} values:",
                            unique_values,
                            default=unique_values
                        )
                        filtered_df = filtered_df[filtered_df[col].isin(selected_values)]
                
                st.write("### Filtered Data After Customization")
                st.dataframe(filtered_df)

                # Step 4: Custom Visualizations
                st.sidebar.header("Step 4: Visualizations")
                if len(headers) >= 2:
                    x_col = st.sidebar.selectbox("Select X-axis:", headers)
                    y_col = st.sidebar.selectbox("Select Y-axis:", headers)
                    
                    if pd.api.types.is_numeric_dtype(df[x_col]) and pd.api.types.is_numeric_dtype(df[y_col]):
                        chart_type = st.sidebar.radio(
                            "Select Chart Type:",
                            ("Scatter Plot", "Line Plot", "Bar Plot")
                        )
                        st.write("### Visualization")
                        fig, ax = plt.subplots()
                        if chart_type == "Scatter Plot":
                            ax.scatter(filtered_df[x_col], filtered_df[y_col])
                            ax.set_xlabel(x_col)
                            ax.set_ylabel(y_col)
                            ax.set_title(f"{chart_type} of {x_col} vs {y_col}")
                        elif chart_type == "Line Plot":
                            ax.plot(filtered_df[x_col], filtered_df[y_col])
                            ax.set_xlabel(x_col)
                            ax.set_ylabel(y_col)
                            ax.set_title(f"{chart_type} of {x_col} vs {y_col}")
                        elif chart_type == "Bar Plot":
                            ax.bar(filtered_df[x_col], filtered_df[y_col])
                            ax.set_xlabel(x_col)
                            ax.set_ylabel(y_col)
                            ax.set_title(f"{chart_type} of {x_col} vs {y_col}")
                        st.pyplot(fig)
                else:
                    st.info("Please select at least two columns for visualizations.")

                # Step 5: Summary Statistics
                st.sidebar.header("Step 5: Summary Statistics")
                stats_columns = st.sidebar.multiselect(
                    "Choose columns for summary statistics:",
                    options=headers,
                    default=headers
                )
                if stats_columns:
                    st.write("### Summary Statistics")
                    st.write(filtered_df[stats_columns].describe())
            else:
                st.warning("Please select at least one header to display the data.")
        else:
            st.warning("No data loaded yet. Check the CSV URL or format.")

if __name__ == "__main__":
    main()
