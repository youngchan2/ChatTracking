from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from utils import set_korean_font

class MessageBarCanvas(FigureCanvas):
    def __init__(self, message_counts, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)

        self.plot_bar_chart(message_counts)

    def plot_bar_chart(self, message_counts):
        set_korean_font()  # 한글 폰트 설정
        self.ax.clear()

        # 챗봇 제외
        # filtered = {k: v for k, v in message_counts.items() if k not in chat_bot}
        sorted_counts = sorted(message_counts.items(), key=lambda x: x[1], reverse=True)

        senders = [x[0] for x in sorted_counts]
        counts = [x[1] for x in sorted_counts]

        self.ax.bar(senders, counts)
        self.ax.set_title("메시지 수")
        # self.ax.set_xlabel("발신자")
        self.ax.set_ylabel("메시지 수")
        self.ax.tick_params(axis='x', rotation=45)
        self.fig.tight_layout()
        self.draw()