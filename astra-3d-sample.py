import astra_3d_utilities as au 
import cv2 

'''
initialization has the following options:
    - devices: "color", "depth", and "ir"
      *** "color" and "ir" are unable to be used together ***

    - resolution: options are:
        (640, 480) or (320, 240)
'''

resolutionWidth = 640
resolutionHeight = 480

vw = au.Viewer3D(
    [
        "color",
        "depth",
    ],
    (resolutionWidth, resolutionHeight),
)

running = True 

while running:
    color = vw._get_color_frame()
    depth = vw._get_depth_frame()
    
    center_distance = depth[
        int(resolutionHeight / 2),
        int(resolutionWidth / 2)
    ]
    
    print(center_distance)
    
    cv2.imshow("color", color)
    cv2.imshow("depth", depth)
    
    if cv2.waitKey(15)==27: #esc to quit
        running = False
        
vw._destroy()
cv2.destroyAllWindows()