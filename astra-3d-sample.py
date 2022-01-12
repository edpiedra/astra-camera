import astra_3d_utilities as au 
import video_analysis as va 
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

gui = va.GUI()
gui._create_windows(
    {
#        "color": {
#            "position": (100,0),
#            "flag": cv2.WINDOW_AUTOSIZE,
#        },
#        "depth": {
#            "position": (450,0),
#            "flag": cv2.WINDOW_AUTOSIZE,
#        },
        "result": {
            "position": (0,450),
            "flag": cv2.WINDOW_AUTOSIZE,
        },
        "HSV Filters": {
            "position": (0,0),
            "flag": cv2.WINDOW_NORMAL,
        }
    }
)

vd = va.VideoDeconstruction()

trackbars = {
    "HSV Filters": {
        "H min": (0,179),
        "S min": (0,255),
        "V min": (0,255),
        "H max": (179,179),
        "S max": (255,255),
        "V max": (255,255),
    }
}

vd._create_hsv_trackbars(trackbars)

running = True 

while running:
    color = vw._get_color_frame()
    depth = vw._get_depth_frame()
    
    vd._extract_hsv_inrange(
        color, "clean"
    )
    
    vd._find_circle()
    
    result = vd.result_frame.copy()
    
    if vd.ball_center is not None:
        
        center_distance = depth[
            vd.ball_center[1], vd.ball_center[0]
        ]
        
        cv2.putText(
            result,
            str(center_distance),
            vd.ball_center,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255,0,0),
            2
        )
    
#    cv2.imshow("color", color)
#    cv2.imshow("depth", depth)
    cv2.imshow("result", result)
    
    if cv2.waitKey(15)==27: #esc to quit
        running = False
        
vw._destroy()
cv2.destroyAllWindows()