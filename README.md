# Jesse’s Cube – 3D Transformations with OpenGL

This project is developed as part of the **Bilgisayar Grafiği (YZ003)** course.  
It is a desktop application that demonstrates **fundamental 3D transformations** on a cube using **OpenGL** and **PyQt5**.



## 🎯 Project Objective

The objective of this assignment is to understand and implement core **3D geometric transformations** and visualize their effects interactively.

The project focuses on:
- Transformation matrices
- Order of transformations
- Coordinate systems
- User interaction in 3D graphics



## 🧱 Features

### 🔹 Translation (Pixel-Based)
- Translate the cube along **X, Y, Z axes**
- All translation values are **pixel-based (px)**
- Applied incrementally using spin boxes



### 🔹 Rotation
Rotation is divided into **two separate parts**:

#### 1. Rotation – Angle
- Rotate around **X, Y, Z axes**
- Values are entered as angles (degrees)
- Incremental (+ / −) control

#### 2. Rotation – Point (Arbitrary Rotation)
- Rotate the cube around an **arbitrary point**
- Defined by **X, Y, Z coordinates**
- When enabled:
  - Cube is translated to origin
  - Rotated
  - Translated back to the specified point
- Controlled using an **Arbitrary checkbox**



### 🔹 Scaling
- Scale independently along **X, Y, Z**
- Supports **Keep Aspect Ratio**
  - When enabled, scaling is uniform
- Scaling is applied incrementally



### 🔹 Mirroring
- Mirror the cube along:
  - X-axis
  - Y-axis
  - Z-axis
- Implemented using negative scaling

---

### 🔹 Shearing
- Shear transformation along:
  - X-axis
  - Y-axis
  - Z-axis
- Implemented using a **custom shear matrix**



### 🔹 Rendering Options
- **Wireframe / Solid mode**
- **Perspective / Orthographic projection**
- Depth testing enabled



### 🔹 Mouse Interaction
- **Mouse drag** → Rotate the cube
- **Mouse wheel** → Zoom in / Zoom out



### 🔹 Reset
- Resets all transformations and camera settings to default



## 🖥️ Technologies Used

- **Python 3**
- **PyQt5**
- **PyOpenGL**
- **OpenGL (Immediate Mode)**



## 📂 Project Structure

- `CubeGL`  
  Handles OpenGL rendering and transformation logic

- `MainWindow`  
  User interface and control panel (OPTIONS)



## 📌 Course Information

- **Course Name:** Computer Graphics  
- **Course Code:** YZ003  
- **Student:** Zeynep Çöl  

