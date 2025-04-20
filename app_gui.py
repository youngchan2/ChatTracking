import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QLabel, QTextEdit
)
from datetime import datetime
from utils import get_combined_message_counts, display_message_counts, set_korean_font
from plot_figure import MessageBarCanvas

class ChatAnalyzerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("카카오톡 채팅 분석기")
        self.setGeometry(100, 100, 500, 400)

        self.layout = QVBoxLayout()

        # 버튼, 레이블, 출력창 생성
        self.select_btn = QPushButton("채팅 폴더 선택")
        self.select_btn.clicked.connect(self.select_folder)
        self.layout.addWidget(self.select_btn)

        self.analyze_btn = QPushButton("분석")
        self.analyze_btn.clicked.connect(self.plot_message_count)
        self.analyze_btn.setEnabled(False)
        self.layout.addWidget(self.analyze_btn)

        self.path_label = QLabel(f"선택할 채팅 데이터 폴더 이름은 날짜로 해주세요 (ex:{datetime.now().strftime('%y.%m.%d')})")
        self.layout.addWidget(self.path_label)

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.layout.addWidget(self.result_area)

        self.setLayout(self.layout)

        self.current_message_counts = {}

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "채팅 폴더 선택")
        if folder_path:
            self.path_label.setText(f"선택된 날짜: {os.path.basename(os.path.normpath(folder_path))}")
            result_text = self.analyze_folder(folder_path)
            self.result_area.setText(result_text)

    def analyze_folder(self, folder_path):
        try:
            self.current_message_counts = get_combined_message_counts(folder_path)
            self.analyze_btn.setEnabled(True)
            return display_message_counts(self.current_message_counts)
        except Exception as e:
            return f"분석 중 오류 발생: {str(e)}"

    def plot_message_count(self):
        if self.current_message_counts:
            canvas = MessageBarCanvas(self.current_message_counts, self)
            canvas.setMinimumHeight(300)

            self.layout.addWidget(canvas)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatAnalyzerApp()
    window.show()
    sys.exit(app.exec_())