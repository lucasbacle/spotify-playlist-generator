import base

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QBrush, QImage, QPainter, QWindow


def _mask_image(imgdata, imgtype='jpg', size=128):
    """
    Return a ``QPixmap`` from *imgdata* masked with a smooth circle.
    *imgdata* are the raw image bytes, *imgtype* denotes the image type.
    The returned image will have a size of *size* × *size* pixels.
    """
    # Load image and convert to 32-bit ARGB (adds an alpha channel):
    image = QImage.fromData(imgdata, imgtype)
    image.convertToFormat(QImage.Format_ARGB32)

    # Crop image to a square:
    imgsize = min(image.width(), image.height())
    rect = QRect(
        (image.width() - imgsize) / 2,
        (image.height() - imgsize) / 2,
        imgsize,
        imgsize,
    )
    image = image.copy(rect)

    # Create the output image with the same dimensions and an alpha channel
    # and make it completely transparent:
    out_img = QImage(imgsize, imgsize, QImage.Format_ARGB32)
    out_img.fill(Qt.transparent)

    # Create a texture brush and paint a circle with the original image onto
    # the output image:
    brush = QBrush(image)        # Create texture brush
    painter = QPainter(out_img)  # Paint the output image
    painter.setBrush(brush)      # Use the image texture brush
    painter.setPen(Qt.NoPen)     # Don't draw an outline
    painter.setRenderHint(QPainter.Antialiasing, True)  # Use AA
    painter.drawEllipse(0, 0, imgsize, imgsize)  # Actually draw the circle
    painter.end()                # We are done (segfault if you forget this)

    # Convert the image to a pixmap and rescale it.  Take pixel ratio into
    # account to get a sharp image on retina displays:
    pr = QWindow().devicePixelRatio()
    pm = QPixmap.fromImage(out_img)
    pm.setDevicePixelRatio(pr)
    size *= pr
    pm = pm.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    return pm


class LoginViewController():
    "Controller class for the login page"

    def __init__(self, view, sm, se):
        self.view = view
        self.spotify_manager = sm
        self.search_engine = se

    def login(self, username):
        if len(username) >= 3:

            self.spotify_manager.authorize(username)

            if self.spotify_manager.is_authorized():

                # Set user picture
                pixmap = _mask_image(
                    self.spotify_manager.get_current_user_pic())
                self.view.pictureLabel.setPixmap(pixmap)

                # Set user name
                self.view.usernameLabel.setText(
                    self.spotify_manager.get_current_user_name())

                # Initialize the search engine
                self.search_engine.initialize()

                # Switch to the search page
                self.view.stackedWidget.setCurrentIndex(base.SEARCH_PAGE)
