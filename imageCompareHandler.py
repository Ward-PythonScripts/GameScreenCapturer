import cv2
from win32api import GetSystemMetrics

class ImageScaleHandler:
    def __init__(self,screenshot) -> None:
       
        
        x_scale,y_scale = self.get_scale_image(screenshot)
        self.x_scale = x_scale
        self.y_scale = y_scale
        
        # CONTINUE_ARROW_IMAGE = cv2.imread("resources\continue_arrow.PNG", cv2.IMREAD_UNCHANGED)
        # new_size = (round(CONTINUE_ARROW_IMAGE.shape[0]*x_scale),round(CONTINUE_ARROW_IMAGE.shape[1]*y_scale))
        # self.CONTINUE_ARROW_IMAGE = cv2.resize(CONTINUE_ARROW_IMAGE,dsize=(new_size[1],new_size[0]))
        
    def get_x_and_y_scale(self):
        return (self.x_scale,self.y_scale)
        
    
    def get_scale_image(self,screenshot):
        shape_new = screenshot.shape[:2]
        
        shape_old = [GetSystemMetrics(0), GetSystemMetrics(1)]
        print("Scaling for a screen of resolution " , shape_old)
        
        x_scale = shape_old[0]/shape_new[0]
        y_scale = shape_old[1]/shape_new[1]
        return x_scale,y_scale