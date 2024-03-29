import torch
import numpy as np
from pytorch3d.io import load_obj
from pytorch3d.structures import Meshes
from pytorch3d.renderer import (
    look_at_view_transform,
    OpenGLPerspectiveCameras, 
    PointLights, 
    DirectionalLights, 
    Materials, 
    RasterizationSettings, 
    MeshRenderer, 
    MeshRasterizer,  
    SoftPhongShader,
    TexturesVertex
)

# Load the STL file
verts, faces, _ = load_obj("mesh.stl")
faces_idx = faces.verts_idx.to(torch.int64)

# Initialize a mesh
mesh = Meshes(
    verts=[verts],   
    faces=[faces_idx],
    textures=TexturesVertex(verts_features=torch.ones_like(verts))
)

# Initialize a camera.
R, T = look_at_view_transform(2.7, 0, 20) 
cameras = OpenGLPerspectiveCameras(device=device, R=R, T=T)

# Define the settings for rasterization and shading. Here we set the output image to be of size 512x512. 
raster_settings = RasterizationSettings(
    image_size=512, 
    blur_radius=0.0, 
    faces_per_pixel=1, 
)

# Place a point light in front of the object
lights = PointLights(device=device, location=[[1.0, 1.0, -2.0]])

# Create a phong renderer by composing a rasterizer and a shader. 
renderer = MeshRenderer(
    rasterizer=MeshRasterizer(
        cameras=cameras, 
        raster_settings=raster_settings
    ),
    shader=SoftPhongShader(
        device=device, 
        cameras=cameras,
        lights=lights
    )
)

# Render the image
images = renderer(mesh)

# Save the image
torchvision.utils.save_image(images, 'image.png')