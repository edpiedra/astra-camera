from openni import openni2 
from openni import _openni2 as c_api
import sys, cv2 
import numpy as np


class Viewer3D():
    def __init__(self, sensors, resolution):
        self.width, self.height = resolution
        self.fps = 30
        
        if ("color" in sensors) and ("ir" in sensors):
            print("[ERROR] cannot initiate color and ir sensors at the same time...")
            sys.exit()
        
        print("[INFO] initializing openni...")    
        openni2.initialize()
        
        print("[INFO] opening device...") 
        dev = openni2.Device.open_any()
        
        # pixelFormat can also be "ONI_PIXEL_FORMAT_DEPTH_1_MM"
        if "depth" in sensors:
            print("[INFO] creating depth stream...")
            self.depth_stream = dev.create_depth_stream()
            self.depth_stream.set_video_mode(
                c_api.OniVideoMode(
                    pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM, 
                    resolutionX = self.width, 
                    resolutionY = self.height, 
                    fps = self.fps, 
                )
            )
            self.depth_stream.start() 
            
        if "ir" in sensors:
            print("[INFO] creating ir stream...")
            self.ir_stream = dev.create_ir_stream()
            self.ir_stream.set_video_mode(
                c_api.OniVideoMode(
                    pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_GRAY16,
                    resolutionX = self.width, 
                    resolutionY = self.height, 
                    fps = self.fps, 
                )
            )
            self.ir_stream.start()
            
        if "color" in sensors:
            print("[INFO] creating color stream...")
            self.color_stream = dev.create_color_stream()
            self.color_stream.set_video_mode(
                c_api.OniVideoMode(
                    pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888, 
                    resolutionX = self.width, 
                    resolutionY = self.height, 
                    fps = self.fps, 
                )
            )
            self.color_stream.start()
            
        if ("color" in sensors) and ("depth" in sensors):
            print("[INFO] synchronizong color and depth sensors...")
            dev.set_image_registration_mode(openni2.IMAGE_REGISTRATION_DEPTH_TO_COLOR)
            dev.set_depth_color_sync_enabled(True)
            
        self.sensors = sensors
            
    def _get_depth_frame(self):
        frame = self.depth_stream.read_frame()
        frame_data = frame.get_buffer_as_uint16()
        img = np.frombuffer(frame_data, dtype=np.uint16) 
        img.shape = (self.height, self.width)
        img = cv2.medianBlur(img, 3)
        img = cv2.flip(img, 1)
        
        return img
    
    def _get_ir_frame(self):
        frame = self.ir_stream.read_frame()
        frame_data = frame.get_buffer_as_uint16()
        img = np.frombuffer(frame_data, dtype=np.uint16) 
        img.shape = (self.height, self.width)
        img = np.multiply(img, int(65535/1023))
        img = cv2.GaussianBlur(img, (5,5), 0)
        img = cv2.flip(img, 1)
        
        return img
    
    def _get_color_frame(self):
        frame = self.color_stream.read_frame()
        frame_data = frame.get_buffer_as_uint8()
        img = np.frombuffer(frame_data, dtype=np.uint8) 
        img.shape = (self.height, self.width, 3)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.flip(img, 1)
        
        return img
    
    def _destroy(self):
        if "depth" in self.sensors: self.depth_stream.stop()
        if "ir" in self.sensors: self.ir_stream.stop()
        if "color" in self.sensors: self.color_stream.stop()
        
        openni2.unload()