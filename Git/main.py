#создаю тут фоторедактор Easy Editor!
import os
from PyQt5.QtWidgets import (QApplication
    ,QWidget, QFileDialog,QLabel,
    QPushButton,QListWidget,QHBoxLayout,QVBoxLayout)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from PIL import Image
from PIL.ImageQt import ImageQt
from PIL import ImageFilter
from PIL.ImageFilter import (
    BLUR, FIND_EDGES, DETAIL, SMOOTH, SMOOTH_MORE, SHARPEN
)

app = QApplication([])
win = QWidget()
win.resize(700, 500)
win.setWindowTitle('Easy Editor')
lb_image = QLabel('Картинка')
btn_dir = QPushButton('Папка')
lw_files = QListWidget()

btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_flip = QPushButton('Зеркально')
btn_sharp = QPushButton('Резкость')
btn_bw = QPushButton('Ч/Б')
btn_blur = QPushButton('Блюр')
btn_det = QPushButton('Деталь')
btn_find = QPushButton('FIND EDGES')
btn_Smo = QPushButton('SMOOTH')
btn_Smo_M = QPushButton('MORE SMOOTH')






row = QHBoxLayout()
row2 = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(lw_files)
col2.addWidget(lb_image, 95)
row_tools = QHBoxLayout()
row2_tools = QHBoxLayout()
row2_tools.addWidget(btn_blur)
row2_tools.addWidget(btn_Smo)
row2_tools.addWidget(btn_Smo_M)
row2_tools.addWidget(btn_find)
row2_tools.addWidget(btn_det)
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)


col2.addLayout(row_tools)
col2.addLayout(row2_tools)

row.addLayout(col1, 20)
row.addLayout(col2, 80)
row2.addLayout(col1, 20)
row2.addLayout(col2, 80)
win.setLayout(row)
win.setLayout(row2)


win.show()

workdir = ''

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def chooseWorkdir():
    global workdir
    workdir=QFileDialog.getExistingDirectory()

def showFilenamesList():
    extensions = ['.png','.jpeg','.jpg','.gif','.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)

    
btn_dir.clicked.connect(showFilenamesList)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"
    
    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
    
    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def shr(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def blur(self):
        self.image = self.image.filter(BLUR)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def tet(self):
        self.image = self.image.filter(DETAIL)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def smoth(self):
        self.image = self.image.filter(SMOOTH)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def smoth_more(self):
        self.image = self.image.filter(SMOOTH_MORE)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def finf(self):
        self.image = self.image.filter(FIND_EDGES)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()

    
def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)

workimage = ImageProcessor()

lw_files.currentRowChanged.connect(showChosenImage)

btn_left.clicked.connect(workimage.left)
btn_bw.clicked.connect(workimage.do_bw)
btn_right.clicked.connect(workimage.right)
btn_flip.clicked.connect(workimage.flip)
btn_sharp.clicked.connect(workimage.shr)
btn_blur.clicked.connect(workimage.blur)
btn_det.clicked.connect(workimage.tet)
btn_find.clicked.connect(workimage.finf)
btn_Smo.clicked.connect(workimage.smoth)
btn_Smo_M.clicked.connect(workimage.smoth_more)

app.exec()