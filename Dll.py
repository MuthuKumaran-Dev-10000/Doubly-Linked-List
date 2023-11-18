
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout,QButtonGroup, QHBoxLayout, QPushButton, QLabel, QLineEdit, QRadioButton  , QListWidget, QMessageBox, QInputDialog
from PyQt5.QtCore import Qt
from pyttsx3 import init as pyttsx_init
import random
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QPainter,QFont


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def insert_beginning(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
            new_node.prev = current


    def insert_at_position(self, data, position):
        new_node = Node(data)
        current = self.head
        for _ in range(position - 1):
            if current is None:
                return
            current = current.next

        if current is None:
            return

        new_node.next = current.next
        new_node.prev = current
        if current.next:
            current.next.prev = new_node
        current.next = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
            
    def delete_beginning(self):
        if self.head:
            current = self.head
            while current.next:
                current = current.next
            if current.prev:
                current.prev.next = None
            else:
                self.head = None
                

    def delete_at_position(self, position):
        current = self.head
        for _ in range(position - 1):
            if current is None:
                return
            current = current.next

        if current is None:
            return

        if current.prev:
            current.prev.next = current.next
        if current.next:
            current.next.prev = current.prev

    def delete_end(self):
        if self.head:
            if self.head.next:
                self.head = self.head.next
                self.head.prev = None
            else:
                self.head = None

    def reverse(self):
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            current.prev = next_node
            prev = current
            current = next_node
        self.head = prev

    def search(self, data):
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False
    
    
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget, QMessageBox, QInputDialog
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QPainter
from pyttsx3 import init as pyttsx_init
import random
import sys
class ArrowWidget(QWidget):
    def __init__(self, parent=None):
        super(ArrowWidget, self).__init__(parent)
        self.arrow_x = 0
        self.arrow_direction = 1  # 1 for right, -1 for left

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawText(self.arrow_x, 100, "$")  # Display the arrow as "$"

    def move_arrow(self):
        self.arrow_x += 10 * self.arrow_direction  # Adjust the movement distance
        if self.arrow_x > self.width():
            self.arrow_direction = -1
        elif self.arrow_x < 0:
            self.arrow_direction = 1
        self.update()

from PyQt5.QtCore import QTimer

class DLLApp(QWidget):
    def __init__(self):
        super().__init__()
        self.dll = DoublyLinkedList()
        self.arrow_x = 0
        self.arrow_direction = 1  # 1 for right, -1 for left
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_arrow)
        self.timer.start(1000)  # Adjust the speed of the arrow movement
        self.initUI()
        

    
    def insert_beginning(self):
        value = self.value_entry.text()
        if value:
            self.dll.insert_beginning(value)
            self.update_output_label()
            self.operation_list.addItem(f"Insert at the beginning: {value}")
            self.value_entry.clear()
            self.speak("Inserted at the beginning:", value)

    def insert_at_position(self):
        value = self.value_entry.text()
        if value:
            position, ok = self.get_position_input()
            if ok:
                self.dll.insert_at_position(value, position)
                self.update_output_label()
                self.operation_list.addItem(f"Insert at position {position}: {value}")
                self.value_entry.clear()
                self.speak("Inserted at position:", value)

    def insert_at_end(self):
        value = self.value_entry.text()
        if value:
            self.dll.insert_at_end(value)
            self.update_output_label()
            self.operation_list.addItem(f"Insert at the end: {value}")
            self.value_entry.clear()
            self.speak("Inserted at the end:", value)

    def delete_beginning(self):
        self.dll.delete_beginning()
        self.update_output_label()
        self.operation_list.addItem("Delete at the beginning")
        self.speak("Deleted at the beginning:", "")

    def delete_at_position(self):
        position, ok = self.get_position_input()
        if ok:
            self.dll.delete_at_position(position)
            self.update_output_label()
            self.operation_list.addItem(f"Delete at position {position}")
            self.speak("Deleted at position:", position)

    def delete_end(self):
        self.dll.delete_end()
        self.update_output_label()
        self.operation_list.addItem("Delete at the end")
        self.speak("Deleted at the end:", "")
        
    def initUI(self):
        self.setWindowTitle("Doubly Linked List Operations")
        self.setGeometry(100, 100, 400, 500)

        self.output_label = QLabel()
        self.output_label.setAlignment(Qt.AlignCenter)
        
        #self.output_label.setStyleSheet("font-size: 50px;")
        #self.output_label.setFont(QFont("Arial", 150))
        font = QFont("Arial", 500)  # Adjust font family and size as needed
        self.output_label.setFont(font)
        
        
        
        


        self.value_label = QLabel("Value:")
        self.value_entry = QLineEdit()
        
        self.insert_begin_button = QPushButton("Insert at Begin")
        self.insert_position_button = QPushButton("Insert at Position")
        self.insert_end_button = QPushButton("Insert at End")
        self.delete_begin_button = QPushButton("Delete at Begin")
        self.delete_position_button = QPushButton("Delete at Position")
        self.delete_end_button = QPushButton("Delete at End")
        self.reverse_button = QPushButton("Reverse")
        self.search_button = QPushButton("Search")
        self.display_label = QLabel("Output:")

        self.operation_list = QListWidget()

        self.insert_begin_button.clicked.connect(self.insert_beginning)
        self.insert_position_button.clicked.connect(self.insert_at_position)
        self.insert_end_button.clicked.connect(self.insert_at_end)
        self.delete_begin_button.clicked.connect(self.delete_beginning)
        self.delete_position_button.clicked.connect(self.delete_at_position)
        self.delete_end_button.clicked.connect(self.delete_end)
        self.reverse_button.clicked.connect(self.reverse)
        self.search_button.clicked.connect(self.search)
        self.output_label = QLabel()
        self.output_label.setAlignment(Qt.AlignCenter)

        self.arrow_label = QLabel("$")  # Use "$" as the arrow
        self.arrow_label.setAlignment(Qt.AlignCenter)
        self.arrow_label.setStyleSheet("font-size: 24px")  # Adjust the font size
        self.arrow_label.setGeometry(self.arrow_x, 300, 30, 30)  # Adjust initial position


        quiz_button = QPushButton("Take Quiz")
        quiz_button.clicked.connect(self.start_quiz)

        main_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        button_layout2 = QHBoxLayout()
        
        main_layout.addWidget(self.output_label)
        self.arrow_widget = ArrowWidget()
        main_layout.addWidget(self.arrow_widget)
        main_layout.addWidget(self.display_label)

        input_layout.addWidget(self.value_label)
        input_layout.addWidget(self.value_entry)
        button_layout.addWidget(self.insert_begin_button)
        button_layout.addWidget(self.insert_position_button)
        button_layout.addWidget(self.insert_end_button)
        button_layout.addWidget(self.delete_begin_button)
        button_layout.addWidget(self.delete_position_button)
        button_layout.addWidget(self.delete_end_button)
        button_layout2.addWidget(self.reverse_button)
        button_layout2.addWidget(self.search_button)
        
        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(button_layout2)
        main_layout.addWidget(self.operation_list)
        main_layout.addWidget(quiz_button)

        self.setLayout(main_layout)

    """def insert_beginning(self):
        value = self.value_entry.text()
        if value:
            self.dll.insert_beginning(value)
            self.update_output_label()
            self.operation_list.addItem(f"Insert at the beginning: {value}")
            self.value_entry.clear()
            self.speak(f"{value} is inserted at the beginning")
    
    def insert_at_position(self):
        value = self.value_entry.text()
        if value:
            position, ok = self.get_position_input()
            if ok:
                self.dll.insert_at_position(value, position)
                self.update_output_label()
                self.operation_list.addItem(f"Insert at position {position}: {value}")
                self.value_entry.clear()
                self.speak(f"{value} is inserted at position {position}")
    
    def insert_at_end(self):
        value = self.value_entry.text()
        if value:
            self.dll.insert_at_end(value)
            self.update_output_label()
            self.operation_list.addItem(f"Insert at the end: {value}")
            self.value_entry.clear()
            self.speak(f"{value} is inserted at the end")

    def delete_beginning(self):
        self.dll.delete_beginning()
        self.update_output_label()
        self.operation_list.addItem("Delete at the beginning")
        self.speak("Item is deleted from the beginning")

    def delete_at_position(self):
        position, ok = self.get_position_input()
        if ok:
            self.dll.delete_at_position(position)
            self.update_output_label()
            self.operation_list.addItem(f"Delete at position {position}")
            self.speak(f"Item is deleted at position {position}")
    
    def delete_end(self):
        self.dll.delete_end()
        self.update_output_label()
        self.operation_list.addItem("Delete at the end")
        self.speak("Item is deleted from the end")"""
        
    def move_arrow(self):
        self.arrow_x += 10 * self.arrow_direction  # Adjust the movement distance
        if self.arrow_x > self.width():
            self.arrow_direction = -1
        elif self.arrow_x < 0:
            self.arrow_direction = 1
        self.arrow_label.setGeometry(self.arrow_x, 300, 30, 30)


    def reverse(self):
        self.dll.reverse()
        self.update_output_label()
        self.operation_list.addItem("List is reversed")
        self.speak("List is reversed"," ")

    def search(self):
        value = self.value_entry.text()
        if value:
            if self.dll.search(value):
                self.operation_list.addItem(f"Search for {value}: Found")
                self.speak(f"{value} is found in DLL."," ")
                self.show_message(f"{value} is found in DLL",)
            else:
                self.operation_list.addItem(f"Search for {value}: Not Found"," ")
                self.speak(f"{value} is not found in DLL."," ")
                self.show_message(f"{value} is not found in DLL",)
            self.value_entry.clear()
    
    def get_position_input(self):
        position, ok = QInputDialog.getInt(self, "Enter Position", "Position:")
        return position, ok

    def update_output_label(self):
        current = self.dll.head
        display_text = ""
        while current:
            display_text = f"{current.data} <-> " + display_text
            current = current.next
        self.output_label.setText(display_text)
        #self.speak(display_text)

    def speak(self, operation, value):
        if operation:
            engine = pyttsx_init()
            engine.say(f"{operation} {value}")
            engine.runAndWait()

    def show_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("Information")
        msg.exec_()

    def start_quiz(self):
        # Create a new window for the quiz
        quiz_app = QuizApp()
        quiz_app.exec_()


class QuizApp(QMessageBox):
    def __init__(self):
        super().__init__()

        self.current_question_index = 0
        self.quiz_data = [
            {
                'question': 'What is the key characteristic of a Doubly Linked List?',
                'options': ['Bidirectional traversal', 'Unidirectional traversal', 'Circular structure', 'Binary search'],
                'correct_answer': 0
            },
            {
                'question': 'How do you insert a new node at the beginning of a Doubly Linked List?',
                'options': ['Create a new node and set it as the head', 'Set the previous node to point to the new node', 'Iterate through the list and append at the beginning', 'Use a stack to insert at the beginning'],
                'correct_answer': 0
            },
            # Add more quiz questions and answers
        ]
        random.shuffle(self.quiz_data)
        self.user_answers = [-1] * len(self.quiz_data)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Quiz")
        self.setStandardButtons(QMessageBox.NoButton)

        # Create layouts
        main_layout = QVBoxLayout()
        question_layout = QVBoxLayout()
        options_layout = QVBoxLayout()
        buttons_layout = QHBoxLayout()

        # Add question and options to the main layout
        main_layout.addLayout(question_layout)
        main_layout.addLayout(options_layout)

        # Add buttons layout
        main_layout.addLayout(buttons_layout)

        question_data = self.quiz_data[self.current_question_index]
        question_text = question_data['question']
        options = question_data['options']

        question_label = QLabel(question_text)
        question_layout.addWidget(question_label)

        self.radio_buttons = QButtonGroup()
        for i, option in enumerate(options):
            radio_button = QRadioButton(option)
            self.radio_buttons.addButton(radio_button, i)
            options_layout.addWidget(radio_button)

        # Add buttons to the buttons layout
        previous_button = QPushButton("Previous")
        submit_button = QPushButton("Submit")
        next_button = QPushButton("Next")

        buttons_layout.addWidget(previous_button, 0, Qt.AlignLeft)
        buttons_layout.addWidget(submit_button, 0, Qt.AlignCenter)
        buttons_layout.addWidget(next_button, 0, Qt.AlignRight)

        self.setLayout(main_layout)

        previous_button.clicked.connect(self.prev_question)
        submit_button.clicked.connect(self.submit_quiz)
        next_button.clicked.connect(self.next_question)

        self.show_question()
        
    def show_question(self):
        question_data = self.quiz_data[self.current_question_index]
        question_text = question_data['question']
        options = question_data['options']

        self.setText(question_text)

        self.radio_buttons = QButtonGroup()
        for i, option in enumerate(options):
            radio_button = self.addButton(option, QMessageBox.ActionRole)
            self.radio_buttons.addButton(radio_button, i)

        self.addButton("Previous", QMessageBox.YesRole)
        self.addButton("Next", QMessageBox.NoRole)
        self.addButton("Submit", QMessageBox.AcceptRole)

    """def show_question(self):
        question_data = self.quiz_data[self.current_question_index]
        text = f"{question_data['question']}\n"
        self.setText(text)

        for i, option in enumerate(question_data['options']):
            radio_button = self.option_buttons.button(i)
            radio_button.setText(option)
            self.addButton(radio_button)"""
            
    def prev_question(self):
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.show_question()

    def next_question(self):
        if self.current_question_index < len(self.quiz_data) - 1:
            self.current_question_index += 1
            self.show_question()

    def submit_quiz(self):
        correct_answers = 0
        for i, question in enumerate(self.quiz_data):
            if self.user_answers[i] == question['correct_answer']:
                correct_answers += 1

        score_text = f'You scored {correct_answers} out of {len(self.quiz_data)}!'
        self.setText(score_text)
        self.removeButton(self.buttonRole(self.button(QMessageBox.Accept)))
        self.addButton("Close", QMessageBox.AcceptRole)
        self.setDefaultButton(QMessageBox.Accept)

    def get_answer(self, answer):
        self.user_answers[self.current_question_index] = self.option_buttons.id(answer)
        if self.current_question_index < len(self.quiz_data) - 1:
            self.next_question()
        else:
            self.submit_quiz()
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DLLApp()
    window.show()
    sys.exit(app.exec_())
