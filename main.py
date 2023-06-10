from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QFileDialog, QListWidget, QWidget
from PyQt5.QtCore import Qt
import markdown
import re


class MarkdownParser(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Markdown上传")
        self.setStyleSheet("font-size:16px;")
        layout = QVBoxLayout(self)

        # 添加打开文件按钮
        btn_openfile = QPushButton("选择文件")
        btn_openfile.clicked.connect(self.open_files)
        layout.addWidget(btn_openfile, alignment=Qt.AlignCenter)

        # 添加结果列表
        self.list_results = QListWidget()
        layout.addWidget(self.list_results, stretch=1)

    def open_files(self):
        # 打开文件选择对话框并获取文件路径列表
        filenames, _ = QFileDialog.getOpenFileNames(self, "Open file", "", "Markdown files (*.md)")

        if not filenames:
            return

        headers = []
        imgs = []

        for filename in filenames:
            with open(filename, encoding="utf-8") as f:
                content = f.read()
                html = markdown.markdown(content)  # 将 Markdown 转为 HTML

                # 正则表达式匹配 h1-h6 标题和图片路径
                header_regex = r'<h([1]).*>(.*)</h\1>'
                img_regex = r'<img.*src="(.*?)".*>'

                # 提取标题和图片路径并添加到数组中
                matches = re.findall(header_regex, html)
                headers.extend([f"{match[0]}. {match[1]}" for match in matches])
                matches = re.findall(img_regex, html)
                imgs.extend(matches)

        # 将标题和图片路径分别添加到列表中
        self.list_results.clear()
        self.list_results.addItems(["<b>Titles:</b>"] + headers)
        self.list_results.addItems(["<b>Image Paths:</b>"] + imgs)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    parser = MarkdownParser()
    parser.show()
    sys.exit(app.exec_())
