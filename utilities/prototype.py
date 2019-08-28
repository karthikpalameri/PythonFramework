import cv2
from matplotlib import pyplot as plt
import logging
from utilities import custom_logger as cl
from base.selenium_driver import SeleniumDriver
from pathlib import Path
import os


class Prototype(SeleniumDriver):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def getLocationCordinates(self, fullimage_location, templateimage_location):
        log = cl.customLogger(logLevel=logging.DEBUG)
        fullimage_location = str(fullimage_location)
        templateimage_loaction = str(templateimage_location)

        # fullimage_location = "/Users/pintu/Documents/GitHub/PythonFramework/Screenshots/test_invalidEnrollment/ToFindInThisImage.png";
        # templateimage_loaction = "/Users/pintu/Documents/GitHub/PythonFramework/Screenshots/test_invalidEnrollment/cropped.png"
        to_plot_img = cv2.imread(fullimage_location)
        fullimage = cv2.imread(fullimage_location, 0)
        fullimage_copy = fullimage.copy()

        # img3 = mpimg.imread(
        #     "/Users/pintu/Documents/GitHub/PythonFramework/Screenshots/test_invalidEnrollment/ToFindInThisImage.png")
        #
        # plt.imshow(img3)
        # plt.show()

        template_image = cv2.imread(templateimage_loaction, 0)
        w, h = template_image.shape[::-1]  # All the 6 methods for comparison in a list
        # methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
        #            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
        methods = ['cv2.TM_SQDIFF']
        for meth in methods:

            fullimage = fullimage_copy.copy()
            method = eval(meth)  # Apply template Matching
            res = cv2.matchTemplate(fullimage, template_image, method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(
                res)  # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv2.rectangle(to_plot_img, top_left, bottom_right, (165, 206, 94), lineType=8, thickness=20)
            plt.subplot(121), plt.imshow(res, cmap='gray')
            plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
            plt.subplot(122)
            plt.imshow(to_plot_img)

            plt.imshow(cv2.cvtColor(to_plot_img, cv2.COLOR_BGR2RGB))
            plt.title('Detected Point x:{} y:{}'.format(top_left[0], top_left[1])), plt.xticks([]), plt.yticks([])
            plt.suptitle(meth)
            plt.show()

            log.warning("Got the coordinated in the Screenshot as X:%s,Y:%s" % (top_left[0], top_left[1]))

            percentageX = ((top_left[0] + bottom_right[0]) / 2) / fullimage.shape[1]
            perentageY = ((top_left[1] + bottom_right[1]) / 2) / fullimage.shape[0]

            log.warning(
                "Calculated Percentage from the original Screenshot , X:{}%  , Y:{}%".format(percentageX, perentageY))

            vpw, vph = self.getViewPortWidtHeight()

            log.warning(
                "Got the ViewPort Size as  , X:{}  , Y:{}".format(vpw, vph))

            actx = vpw * percentageX
            acty = vph * perentageY

            log.warning(
                "Calculated Percentage from the ViewPort Screenshot and got  , X:{}  , Y:{}".format(actx, acty))

            # return (top_left[0], top_left[1])

            log.warning(
                "Returning Actual Co-ordinate from the ViewPort Screenshot->> X:{}  , Y:{}".format(actx, acty))

            return (actx, acty)

    def getElementFromProtoType(self, page_name, image_name):

        fullimage_location = self.getScreenShotPath()
        templateimage_location = self.getCroppedImagePath(page_name, image_name)

        x, y = self.getLocationCordinates(fullimage_location, templateimage_location)

        calculated_element = self.driver.execute_script("return document.elementFromPoint(arguments[0],arguments[1]);",
                                                        x, y)
        return calculated_element

    def getScreenShotPath(self, tempfilename="temp.png"):
        try:
            # dir_location = os.getcwd() + "/Screenshots/" + test_name + "/"
            dir_location = Path(__file__).parent.parent / 'ScreenshotsPrototypeTemp'
            # Path.mkdir(dir_location, exist_ok=True)
            os.makedirs(dir_location, exist_ok=True)
            # file_name = screenshot_instance_state.strip() + ".png"

            # file_path = os.path.join(dir_location, file_name)
            file_path = dir_location / tempfilename
            self.log.info("ProtoType::Taking Screenshot to-> {}".format(file_path))
            self.driver.save_screenshot(str(file_path))
            self.log.info("ProtoType::Screenshot taken in-> {}".format(file_path))
            return file_path
        except  Exception as e:
            self.log.error("ProtoType::Something went wrong while taking a Temp-Screenshot!!!")
            print("Exception Message->>{}".format(e))

    def getCroppedImagePath(self, page_name, image_name):
        try:
            page_name = page_name.strip()
            image_name = image_name.strip()
            file_location = Path(__file__).parent.parent / 'ImageRepository' / page_name / image_name

            if Path(file_location).exists():
                self.log.info("Cropped image found in the location:{}".format(file_location))
                return file_location
            else:
                self.log.error("Prototype::NO CROPPED IMAGE FOUND IN the location:{}".format(file_location))

        except Exception as e:
            self.log.error("Exception! in getCroppedImageFromFolder!! Prototype::NO CROPPED IMAGE FOUND IN FOLDER!!!")
            print("Exception Message->>{}".format(e))

    def getViewPortWidtHeight(self):
        try:
            vpw = self.driver.execute_script("return window.innerWidth")
            vph = self.driver.execute_script("return window.innerHeight")
            return (vpw, vph)
        except:
            self.log.error("Exception! in getViewPortWidtHeight!!")
