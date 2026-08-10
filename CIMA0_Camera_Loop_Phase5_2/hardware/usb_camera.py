import cv2

class USBCamera:
    """
    USB camera hardware adapter.
    Responsibility: hardware access only
    No: image processing sampling computation interpretation
    """
    def __init__( self, device_id=0 ):
        self.camera = None
        
        # ✨ 核心修复：依次测试 0 到 5 号索引，并强制使用 Windows 现代 MSMF 后端
        for index in range(0, 6):
            print(f"📡 正在尝试通过 MSMF 后端打开摄像头索引: {index} ...")
            cap = cv2.VideoCapture( index, cv2.CAP_MSMF )
            if cap.isOpened():
                # 检查是否真的能读到帧，防止部分虚拟设备占位
                ok, _ = cap.read()
                if ok:
                    self.camera = cap
                    print(f"✅ [成功] 已成功连接到实体摄像头，当前有效索引为: {index}")
                    break
            cap.release()
        
        # 备用方案：如果 MSMF 全失败，让 OpenCV 自己盲猜底层驱动
        if self.camera is None or not self.camera.isOpened():
            print("⚠️ MSMF 失败，正在尝试系统默认盲猜模式(不带后端参数)...")
            self.camera = cv2.VideoCapture( device_id )

    def read(self):
        """
        Read raw camera frame.
        Return: raw frame
                None if failed
        """
        if self.camera is None or not self.camera.isOpened():
            return None
            
        ok, frame = self.camera.read()
        if not ok:
            return None
        return frame

    def release(self):
        """
        Release hardware resource.
        """
        if self.camera is not None and self.camera.isOpened():
            self.camera.release()
