import inspect
import traceback

import cv2
from matplotlib import pyplot as plt
import logging
from utilities import custom_logger as cl
from base.selenium_driver import SeleniumDriver
from pathlib import Path
import os
from PIL import Image


class Prototype(SeleniumDriver):
    log = cl.customLogger(logLevel=logging.DEBUG)
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def getLocationCordinates(self, fullimage_location, templateimage_location):

        fullimage_location = str(fullimage_location)
        templateimage_loaction = str(templateimage_location)

        to_plot_img = cv2.imread(fullimage_location)
        fullimage = cv2.imread(fullimage_location, 0)
        fullimage_copy = fullimage.copy()

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
            plt.subplot(121)
            plt.imshow(res, cmap='gray')
            plt.title('Original Image')
            plt.xticks([]), plt.yticks([])
            plt.subplot(122)
            plt.imshow(to_plot_img)

            plt.imshow(cv2.cvtColor(to_plot_img, cv2.COLOR_BGR2RGB))
            plt.title('Detected Point x:{} y:{}'.format(top_left[0], top_left[1])), plt.xticks([]), plt.yticks([])
            plt.suptitle(meth)
            plt.show()

            plt.savefig(self.directoryToSave(), bbox_inches='tight')  # saves the plot in directory

            self.log.info("Got the coordinated in the Screenshot as X:%s,Y:%s" % (top_left[0], top_left[1]))

            percentageX = ((top_left[0] + bottom_right[0]) / 2) / fullimage.shape[1]
            perentageY = ((top_left[1] + bottom_right[1]) / 2) / fullimage.shape[0]

            self.log.info(
                "Calculated Percentage from the original Screenshot , X:{}%  , Y:{}%".format(percentageX, perentageY))

            vpw, vph = self.getViewPortWidtHeight()

            self.log.info(
                "Got the ViewPort Size as  , X:{}  , Y:{}".format(vpw, vph))

            actx = vpw * percentageX
            acty = vph * perentageY

            self.log.info(
                "Calculated Percentage from the ViewPort Screenshot and got  , X:{}  , Y:{}".format(actx, acty))

            # return (top_left[0], top_left[1])

            self.log.info(
                "Returning Actual Co-ordinate from the ViewPort Screenshot->> X:{}  , Y:{}".format(actx, acty))

            return (actx, acty)

    def getElementFromProtoType(self, page_name, image_name):

        fullimage_location = self.getViewPortResizedScreenShotAndItsPath()
        templateimage_location = self.getCroppedImagePath(page_name, image_name)

        x, y = self.getLocationCordinates(fullimage_location, templateimage_location)

        calculated_element = self.driver.execute_script("return document.elementFromPoint(arguments[0],arguments[1]);",
                                                        x, y)
        return calculated_element

    def getScreenShotAndItsPath(self, tempfilename="temp1.png"):
        """Takes screenshot and returns the path of the ssTrain"""
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
            traceback.print_exc()

    def getViewPortResizedScreenShotAndItsPath(self, tempfilename="tempViewPortSS.png"):
        """Takes screenshot and Resizing it to the viewport resolution  and  returns the path of the screenshot"""
        try:
            dir_location = Path(__file__).parent.parent / 'ScreenshotsPrototypeTemp'
            os.makedirs(dir_location, exist_ok=True)
            file_path = dir_location / tempfilename
            self.log.info("ProtoType::Taking Screenshot to-> {}".format(file_path))
            self.driver.save_screenshot(str(file_path))
            self.log.info("ProtoType::Taken Screenshot to-> {}".format(file_path))
            self.log.info("ProtoType::Taking Screenshot and Resizing it to ViewPort from -> {}".format(file_path))
            self.doResizeToViewPortSize(file_path)

            self.log.info("ProtoType::ViewPortResizedScreenshot taken in-> {}".format(file_path))
            return file_path
        except  Exception as e:
            self.log.error("ProtoType::Something went wrong while taking a tempViewPortSS-Screenshot!!!")
            print("Exception Message->>{}".format(e))
            traceback.print_exc()

    def doResizeToViewPortSize(self, file_path):
        try:
            vpw, vph = self.getViewPortWidtHeight()
            img = Image.open(file_path)
            resized_img = img.resize((vpw, vph), Image.ANTIALIAS)
            resized_img.save(file_path)
            self.log.info(
                "ProtoType::doing ResizeToViewPortSize-> ViewPortResizedScreenshot taken in-> {}".format(file_path))
        except  Exception as e:
            self.log.error("ProtoType::Something went wrong while taking a Temp-tempViewPortSS!!!")
            print("Exception Message->>{}".format(e))
            traceback.print_exc()

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
            traceback.print_exc()

    def getViewPortWidtHeight(self):
        try:
            vpw = self.driver.execute_script("return window.innerWidth")
            vph = self.driver.execute_script("return window.innerHeight")
            return (vpw, vph)
        except Exception as e:
            print("Exception message ->{}".format(e))
            self.log.error("Exception! in getViewPortWidtHeight!! \n Exception message->{}".format(e))
            traceback.print_exc()

    def cropElement(self, page_name,
                    image_name, elementToCrop_locator, elementToCrop_locatorType="xpath",
                    element=None, cropped_image_file_path=None, ):
        """
        Crop the given element and save it

        :param page_name: diretory name to
        :param image_name:
        :param elementToCrop_locator:
        :param elementToCrop_locatorType:
        :param element:
        :param cropped_image_file_path:
        :return:
        """
        try:
            if elementToCrop_locator:
                element = self.getElement(locator=elementToCrop_locator, locatorType=elementToCrop_locatorType)
            x, y = element.location['x'], element.location['y']
            w, h = element.size['width'], element.size['height']

            left = x
            top = y
            right = x + w
            bottom = y + w

            self.log.info(
                "Got the box co-ordinates as left:{} right:{} top:{} bottom:{}\n Now Getting screenshot and croping".format(
                    left, right, top, bottom))
            self.log.info("Getting screenshot to crop the element in it")
            screenshot_path = self.getScreenShotAndItsPath(tempfilename="temp2.png")

            vpw, vph = self.getViewPortWidtHeight()
            self.log.info("Got the Vieport width::{} and Viewport Height::{}".format(vpw, vph))
            img = Image.open(screenshot_path)
            img = img.resize((vpw, vph), Image.ANTIALIAS)
            img = img.save(screenshot_path, "PNG")

            self.log.info("Trying to Crop the Screenshot ")
            img = Image.open(screenshot_path)

            self.log.info(
                "Opening the Screenshot file->{} image information-> img.format::{},img.size::{},img.mode::{}".format(
                    screenshot_path, img.format,
                    img.size,
                    img.mode))
            if img.format is None:
                self.log.error("Opening Cropped FAILED!, image might have not read from the file")

            else:
                cropped_image = img.crop((left, top, right, bottom))
                cropped_image_file_name = str(image_name) + ".png"
                if cropped_image_file_path is None:
                    framework_path = Path.cwd().parent.parent / "ImageRepository" / page_name
                    Path(framework_path).mkdir(parents=True, exist_ok=True)
                    cropped_image_file_path = framework_path / cropped_image_file_name

                cropped_image.save(cropped_image_file_path)
                self.log.info("Saved the Cropped screenshot to Location::{}".format(cropped_image_file_path))

        except Exception as e:
            print("Exception message ->{}".format(e))
            self.log.error("Exception! in {}!! \n Exception message->{} ->{}".format(inspect.stack()[0][3], e,
                                                                                     traceback.print_exc()))

    def directoryToSave(self, file_path=None):
        """
        If filepath is passed will create the directories recursively and returns the path
        If filepath is not given it will create a directory accordingly to framework and returns the path
        :param file_path:
        :return:
        """
        if file_path is None:
            file_path = Path.cwd().parent.parent / "ImageRepository" / "ImageLogs"
            self.log("File path is NOT given so returning framework directory as->{}".format(file_path))
        Path(file_path).mkdir(parents=True, exist_ok=True)
        file_path = str(file_path)
        self.log("Created the directories recursively in {} ".format(file_path))
        return file_path
