# app.py
import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

#st.title("My Streamlit App")
#st.write("Hello, Streamlit!")


#cd "/Users/gsaxton/Dropbox/National-level Studies"


# Function to read the edge list and create a graph
def load_graph_from_edgelist(file_path):
    try:
        G = nx.read_weighted_edgelist(file_path, delimiter=';', create_using=nx.Graph())
        return G
    except Exception as e:
        st.error(f"Error loading graph: {e}")
        return None
        
        
# Function to create edges_df from the graph
def create_edges_df(G):
    edges_data = [(u, v, d['weight']) for u, v, d in G.edges(data=True)]
    edges_df = pd.DataFrame(edges_data, columns=['Source', 'Target', 'Weight'])
    edges_df = edges_df.sort_values('Weight', ascending=False)
    print(len(edges_df))
    return edges_df
            
                      
# Function to create and plot the subnetwork based on a search term
def create_subnetwork(G, search_term):
    # Filter edges where the search term is found in either node
    filtered_edges = [(u, v, d) for u, v, d in G.edges(data=True)
                      if search_term.lower() in u.lower() or search_term.lower() in v.lower()]

    # Create a subgraph with the filtered edges
    subG = nx.DiGraph()
    subG.add_edges_from(filtered_edges)

    # Plot the graph
    if subG.number_of_nodes() > 0:
        plt.figure(figsize=(12, 8))
        #fig, ax = plt.subplots(figsize=(10, 8))
        pos = nx.spring_layout(subG, k=2.75, iterations=75)
        nx.draw_networkx(subG, 
                pos, 
                with_labels=True, 
                node_size=1500, 
                node_color='skyblue',
                # font_weight='bold',  
                font_size=10, 		    
                arrowsize=17.5,       # Set arrow size for directed graphs        
                edge_color='gray',  # Set edge color
                width=2, 			# Set edge thickness
                )
        plt.title(f"Subnetwork containing '{search_term}'")
        st.pyplot(plt)
        plt.close()
    else:
        st.warning("No matching nodes or edges found for the given search term.")


# Streamlit app layout
st.title("Subnetwork Search App")
st.write("Enter a term to search for in the network:")

# Load the graph from the weighted edge list file
file_path = "relationships.weighted.edgelist"  # Make sure this path is correct
G = load_graph_from_edgelist(file_path)


# Check if the graph was loaded successfully
if G:
    # Create the edges DataFrame from the graph
    edges_df = create_edges_df(G)

    # Display the first few rows of the DataFrame
    st.write("Edges DataFrame - first 5 rows:")
    st.dataframe(edges_df.head())

    # Input for the search term
    search_term = st.text_input("Search Term", "")

    # Button to trigger the search
    if st.button("Search"):
        if search_term:
            create_subnetwork(G, search_term)
        else:
            st.warning("Please enter a search term.")
else:
    st.error("Failed to load the graph. Please check the file path and format.")
