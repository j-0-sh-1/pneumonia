import streamlit as st
import tensorflow as tf
import numpy as np
import cv2
import pandas as pd
import plotly.express as px
from tensorflow.keras.preprocessing import image
from io import BytesIO
import os
import gdown

# ---------------------------
# Download and load the pre-trained model from Google Drive
@st.cache_resource
def load_model():
    model_path = "model.keras"
    # If the model file doesn't exist locally, download it from Google Drive
    if not os.path.exists(model_path):
        # Google Drive share link: https://drive.google.com/file/d/1lQ6WOzuG2nyyEdCLzOR8d2Cdq6hKiB8p/view?usp=sharing
        # Extracted file ID:
        file_id = "1lQ6WOzuG2nyyEdCLzOR8d2Cdq6hKiB8p"
        url = f"https://drive.google.com/uc?id={file_id}"
        st.write("Downloading model from Google Drive...")
        gdown.download(url, model_path, quiet=False)
    model = tf.keras.models.load_model(model_path)
    return model

model = load_model()

# ---------------------------
# Integrated Gradients Function
def integrated_gradients(model, x, target_class_idx=0, baseline=None, steps=50):
    if baseline is None:
        baseline = tf.zeros(shape=x.shape, dtype=x.dtype)
    interpolated_x = [baseline + (float(i)/steps) * (x - baseline) for i in range(steps + 1)]
    interpolated_x = tf.concat(interpolated_x, axis=0)
    with tf.GradientTape() as tape:
        tape.watch(interpolated_x)
        preds = model(interpolated_x)
        outputs = preds[:, 0] if preds.shape[1] == 1 else preds[:, target_class_idx]
    grads = tape.gradient(outputs, interpolated_x)
    grads = tf.reshape(grads, (steps + 1, ) + x.shape[1:])
    avg_grads = (grads[1:] + grads[:-1]) / 2.0
    integrated_grad = tf.reduce_mean(avg_grads, axis=0)
    integrated_grad = (x - baseline) * integrated_grad
    integrated_grad = tf.reduce_sum(integrated_grad, axis=-1)
    return integrated_grad.numpy().squeeze()

# ---------------------------
# Image Processing Function
def process_image(uploaded_file):
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    cv2_img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    cv2_img = cv2.resize(cv2_img, (150,150))
    rgb_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    img_pil = image.array_to_img(rgb_img)
    img_pil = img_pil.resize((150,150))
    x = image.img_to_array(img_pil)
    x = np.expand_dims(x, axis=0)
    x /= 255.0
    return x, rgb_img

# ---------------------------
# Streamlit Web App
st.title("Pneumonia X-ray Analysis")
st.write("Upload your X-ray image. The app will classify the image and highlight regions contributing to the model's decision.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], key="unique_file_uploader")

if uploaded_file is not None:
    x, orig_img = process_image(uploaded_file)
    st.image(orig_img, caption='Uploaded X-ray Image', use_column_width=True)
    
    # ---------------------------
    # Classification Prediction
    preds = model.predict(x)
    # Assuming binary classification:
    if preds.shape[1] == 1:
        # Using a sigmoid activation output
        class_idx = 0 if preds[0][0] < 0.5 else 1
        classes = ["Pneumonia", "Normal"]
        confidence = (1 - preds[0][0]) if preds[0][0] < 0.5 else preds[0][0]
    else:
        class_idx = np.argmax(preds)
        classes = ["Pneumonia", "Normal"]
        confidence = preds[0][class_idx]
    
    st.write(f"**Classification Result:** {classes[class_idx]} (Confidence: {confidence:.2f})")
    
    # ---------------------------
    # Compute Integrated Gradients with predicted class as target
    st.write("Computing Integrated Gradients...")
    ig_map = integrated_gradients(model, x, target_class_idx=class_idx, steps=50)
    
    # Normalize and Clip IG Map for Better Visualization
    lower, upper = np.percentile(ig_map, [1, 99])
    ig_map_clipped = np.clip(ig_map, lower, upper)
    ig_map_norm = (ig_map_clipped - lower) / (upper - lower + 1e-8)
    
    # Create a Heatmap Overlay
    heatmap = np.uint8(255 * ig_map_norm)
    heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_HOT)
    heatmap_color = cv2.resize(heatmap_color, (150,150))
    
    orig_bgr = cv2.cvtColor(orig_img, cv2.COLOR_RGB2BGR)
    superimposed_img = cv2.addWeighted(heatmap_color, 0.4, orig_bgr, 0.6, 0)
    superimposed_img = cv2.cvtColor(superimposed_img, cv2.COLOR_BGR2RGB)
    
    st.image(superimposed_img, caption="Integrated Gradients Overlay", use_column_width=True)
    
    # Create an Interactive Plotly Scatter Plot
    height, width, _ = superimposed_img.shape
    flat_img = superimposed_img.reshape(-1, 3)
    flattened_heatmap = ig_map_norm.flatten()
    df = pd.DataFrame({
        'R': flat_img[:, 0],
        'G': flat_img[:, 1],
        'B': flat_img[:, 2],
        'Importance': flattened_heatmap
    })
    df['Row'] = [i // width for i in range(height * width)]
    df['Col'] = [i % width for i in range(height * width)]
    
    fig = px.scatter(
        df,
        x='Col',
        y='Row',
        color='Importance',
        color_continuous_scale='Jet',
        hover_data=['Importance'],
        title='Interactive Overlay (Pixel-level Hover)'
    )
    fig.update_yaxes(autorange='reversed')
    fig.update_layout(height=600, width=600)
    st.plotly_chart(fig)
    
    st.write("Regions with higher importance (hot colors) indicate areas that contributed more to the model’s decision.")
import streamlit as st
import tensorflow as tf
import numpy as np
import cv2
import pandas as pd
import plotly.express as px
from tensorflow.keras.preprocessing import image
from io import BytesIO
import os
import gdown

# ---------------------------
# Download and load the pre-trained model from Google Drive
@st.cache_resource
def load_model():
    model_path = "model.keras"
    # If the model file doesn't exist locally, download it from Google Drive
    if not os.path.exists(model_path):
        # Google Drive share link: https://drive.google.com/file/d/1lQ6WOzuG2nyyEdCLzOR8d2Cdq6hKiB8p/view?usp=sharing
        # Extracted file ID:
        file_id = "1lQ6WOzuG2nyyEdCLzOR8d2Cdq6hKiB8p"
        url = f"https://drive.google.com/uc?id={file_id}"
        st.write("Downloading model from Google Drive...")
        gdown.download(url, model_path, quiet=False)
    model = tf.keras.models.load_model(model_path)
    return model

model = load_model()

# ---------------------------
# Integrated Gradients Function
def integrated_gradients(model, x, target_class_idx=0, baseline=None, steps=50):
    if baseline is None:
        baseline = tf.zeros(shape=x.shape, dtype=x.dtype)
    interpolated_x = [baseline + (float(i)/steps) * (x - baseline) for i in range(steps + 1)]
    interpolated_x = tf.concat(interpolated_x, axis=0)
    with tf.GradientTape() as tape:
        tape.watch(interpolated_x)
        preds = model(interpolated_x)
        outputs = preds[:, 0] if preds.shape[1] == 1 else preds[:, target_class_idx]
    grads = tape.gradient(outputs, interpolated_x)
    grads = tf.reshape(grads, (steps + 1, ) + x.shape[1:])
    avg_grads = (grads[1:] + grads[:-1]) / 2.0
    integrated_grad = tf.reduce_mean(avg_grads, axis=0)
    integrated_grad = (x - baseline) * integrated_grad
    integrated_grad = tf.reduce_sum(integrated_grad, axis=-1)
    return integrated_grad.numpy().squeeze()

# ---------------------------
# Image Processing Function
def process_image(uploaded_file):
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    cv2_img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    cv2_img = cv2.resize(cv2_img, (150,150))
    rgb_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    img_pil = image.array_to_img(rgb_img)
    img_pil = img_pil.resize((150,150))
    x = image.img_to_array(img_pil)
    x = np.expand_dims(x, axis=0)
    x /= 255.0
    return x, rgb_img

# ---------------------------
# Streamlit Web App
st.title("Pneumonia X-ray Analysis")
st.write("Upload your X-ray image. The app will classify the image and highlight regions contributing to the model's decision.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    x, orig_img = process_image(uploaded_file)
    st.image(orig_img, caption='Uploaded X-ray Image', use_column_width=True)
    
    # ---------------------------
    # Classification Prediction
    preds = model.predict(x)
    # Assuming binary classification:
    if preds.shape[1] == 1:
        # Using a sigmoid activation output
        class_idx = 0 if preds[0][0] < 0.5 else 1
        classes = ["Pneumonia", "Normal"]
        confidence = (1 - preds[0][0]) if preds[0][0] < 0.5 else preds[0][0]
    else:
        class_idx = np.argmax(preds)
        classes = ["Pneumonia", "Normal"]
        confidence = preds[0][class_idx]
    
    st.write(f"**Classification Result:** {classes[class_idx]} (Confidence: {confidence:.2f})")
    
    # ---------------------------
    # Compute Integrated Gradients with predicted class as target
    st.write("Computing Integrated Gradients...")
    ig_map = integrated_gradients(model, x, target_class_idx=class_idx, steps=50)
    
    # Normalize and Clip IG Map for Better Visualization
    lower, upper = np.percentile(ig_map, [1, 99])
    ig_map_clipped = np.clip(ig_map, lower, upper)
    ig_map_norm = (ig_map_clipped - lower) / (upper - lower + 1e-8)
    
    # Create a Heatmap Overlay
    heatmap = np.uint8(255 * ig_map_norm)
    heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_HOT)
    heatmap_color = cv2.resize(heatmap_color, (150,150))
    
    orig_bgr = cv2.cvtColor(orig_img, cv2.COLOR_RGB2BGR)
    superimposed_img = cv2.addWeighted(heatmap_color, 0.4, orig_bgr, 0.6, 0)
    superimposed_img = cv2.cvtColor(superimposed_img, cv2.COLOR_BGR2RGB)
    
    st.image(superimposed_img, caption="Integrated Gradients Overlay", use_column_width=True)
    
    # Create an Interactive Plotly Scatter Plot
    height, width, _ = superimposed_img.shape
    flat_img = superimposed_img.reshape(-1, 3)
    flattened_heatmap = ig_map_norm.flatten()
    df = pd.DataFrame({
        'R': flat_img[:, 0],
        'G': flat_img[:, 1],
        'B': flat_img[:, 2],
        'Importance': flattened_heatmap
    })
    df['Row'] = [i // width for i in range(height * width)]
    df['Col'] = [i % width for i in range(height * width)]
    
    fig = px.scatter(
        df,
        x='Col',
        y='Row',
        color='Importance',
        color_continuous_scale='Jet',
        hover_data=['Importance'],
        title='Interactive Overlay (Pixel-level Hover)'
    )
    fig.update_yaxes(autorange='reversed')
    fig.update_layout(height=600, width=600)
    st.plotly_chart(fig)
    
    st.write("Regions with higher importance (hot colors) indicate areas that contributed more to the model’s decision.")
