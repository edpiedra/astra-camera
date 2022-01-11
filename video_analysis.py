import cv2 
import numpy as np 

class GUI():
    def _create_windows(self, windows):
        for window in windows:
            position = windows[window]["position"]
            flag = windows[window]["flag"]
            
            self._create_window(window, position, flag)
            
    def _create_window(self, title, position, flag):
        cv2.namedWindow(title, flag)
        cv2.moveWindow(title, position[0], position[1])
        
class VideoDeconstruction():
    def _nothing(self, x):
        pass
    
    def _create_hsv_trackbars(self, trackbars):
        for window in trackbars:
            for trackbar in trackbars[window]:
                count = trackbars[window][trackbar]
                
                cv2.createTrackbar(
                    trackbar,
                    window, 
                    count[0],
                    count[1],
                    self._nothing
                )
                
    def _extract_hsv_inrange(self, frame, filter):
        h_min = cv2.getTrackbarPos("H min", "HSV Filters")
        s_min = cv2.getTrackbarPos("S min", "HSV Filters")
        v_min = cv2.getTrackbarPos("V min", "HSV Filters")
        h_max = cv2.getTrackbarPos("H max", "HSV Filters")
        s_max = cv2.getTrackbarPos("S max", "HSV Filters")
        v_max = cv2.getTrackbarPos("V max", "HSV Filters")
        
        self.lower_range = np.array([h_min, s_min, v_min])
        self.upper_range = np.array([h_max, s_max, v_max])
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        
        mask = cv2.inRange(hsv, self.lower_range, self.upper_range)
        
        if filter=="clean":
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
        
        result = cv2.bitwise_and(frame, frame, mask=mask)
        
        self.hsv_min = "MIN H:{} S:{} V:{}".format(h_min, s_min, v_min)
        self.hsv_max = "MAX H:{} S:{} V:{}".format(h_max, s_max, v_max)
        
        cv2.putText(result, self.hsv_min, (5,10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        cv2.putText(result, self.hsv_max, (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        
        self.hsv_mask = mask.copy()
        self.result_frame = result.copy()
        
        return result, mask