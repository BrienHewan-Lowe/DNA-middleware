import kivy
import re
import math


from kivy.app import App
import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

"""
This is a quick function I made to help set the
X axis increments for the graph later in the program. This function will take a number 
and round it up to the nearest 100th.
For example the number 1476 will be
rounded up to 1500.
"""
def roundup(x):
    return int(math.ceil(x/100.0)) * 100

#This class will handle the functions of the main window
class MainWindow(Screen):
    """
    The parse_clusters function parse the X and Y positions
    from the sequence identifier patterns and then create the graph
    that will display the data.
    """
    def parse_clusters(self):
        """
        The re.search function will search for matches
        of the regular expression in both sequence
        identifier strings and the result will be stored in
        the result1 and result2 variables.
        """
        result1 = re.search("(:\d+)(:\d+)\s", self.ids.seq_ID_1.text)
        result2 = re.search("(:\d+)(:\d+)\s", self.ids.seq_ID_2.text)
        """
        Then using the re.sub() function from the re library,
        the colons and whitespaces in the strings will be removed
        and the remaining pieces of the strings will be put in the
        x_pos1, y_pos1, x_pos2 and y_pos2 variables.
        """
        x_pos1 = re.sub('[^A-Za-z0-9]+', '', result1.group(1))
        y_pos1 = re.sub('[^A-Za-z0-9]+', '', result1.group(2))
        x_pos2 = re.sub('[^A-Za-z0-9]+', '', result2.group(1))
        y_pos2 = re.sub('[^A-Za-z0-9]+', '', result2.group(2))
        """
        The plt.scatter functions will then plot the results on
        a scatter plot.
        """
        plt.scatter(int(x_pos1), int(y_pos1), s=45, edgecolors="black",
                    label="Sequence 1( "+ x_pos1 + ",  " + y_pos1 + ")",
                    marker= 'h', c='r')
        plt.scatter(int(x_pos2), int(y_pos2), s=45, edgecolors="black",
                    label="Sequence 2( " + x_pos2 + ",  " + y_pos2 + ")",
                    marker= 'h', c='g')

        """This will make the x axis increment start at 0."""
        plt.xlim(xmin=0)

        """
        This next line will make the y axis start at 0 and
        the maximum increment will be the bigger number 
        between y_pos1 and y_pos2 rounded up to the nearest 100.
        """
        plt.ylim(0,roundup(max(int(y_pos1), int(y_pos2))))
        plt.xlabel('X Cluster')
        plt.ylabel('Y Cluster')
        plt.title('Sequence Comparisons')

        """
        This will add a grid line to graph background.
        """
        plt.grid()

        """
        The next 3 lines will position the graph 
        and the legend.
        """
        chartBox = plt.subplot().get_position()
        plt.subplot().set_position([chartBox.x0, chartBox.y0, chartBox.width * 0.6, chartBox.height])
        plt.legend(bbox_to_anchor=(1.05, .9), loc=2, borderaxespad=0.)

    """
    The press_submit function will handle what happens 
    after the SUBMIT button is pressed. 
    """
    def press_submit(self):
        """
        The re.search function will check to see if the sequence identifier
        in the seq_ID_1 and seq_ID_2 text input variables match the regular
        expression.
        """
        seq1 = re.search("^@\w+:?\d+:?[^:]+[:?\d+]+\s\d:+[N|Y]:+[0|2468]:?.+",
                         self.ids.seq_ID_1.text)
        seq2 = re.search("^@\w+:?\d+:?[^:]+[:?\d+]+\s\d:+[N|Y]:+[0|2468]:?.+",
                         self.ids.seq_ID_2.text)
        """
        If the value stored in seq1 or seq2 is None then the 
        sequence identifier pattern is not valid and 
        Sequence Error Popup will be called.
        If the lengths of the Sequence Identifier, Nucleotide Sequence,
        or Quality Score text inputs are equal to 0 then the Empty
        Error Popup will be called.   
        If none of the above conditions are true then the 
        parse_clusters function will be called and the
        scatter plot will be created.   
        """
        if seq1 == None or seq2 == None:
           SequenceErrorPopup.popup.open()
        elif len(self.ids.seq_ID_1.text) == 0 or len(self.ids.seq_ID_2.text) == 0:
            EmptyErrorPopup.popup.open()
        elif len(self.ids.nuc_Seq_1.text) == 0 or len(self.ids.nuc_Seq_2.text) == 0:
          EmptyErrorPopup.popup.open()
        elif len(self.ids.quality_Score_1.text) == 0 or len(self.ids.quality_Score_2.text) == 0:
          EmptyErrorPopup.popup.open()
        else:
            self.parse_clusters()
            plt.show()

class WindowManager(ScreenManager):
    pass

"""
This is the first of the two popup classes.
The SequenceErrorPopup will display a popup if the 
text input of the two Sequence Identifier boxes
do not match the sequence identifier pattern.
"""
class SequenceErrorPopup(Popup):
    button1 = Button(text='Close', size_hint_y=(.4))
    label1 = Label(text='Please enter a correct sequence identifier pattern')
    box1 = BoxLayout(orientation="vertical")
    box1.add_widget(label1)
    box1.add_widget(button1)
    content = box1
    popup = Popup(title='Error', content=content,
                  size_hint=(None, None), size=(800, 350))

    button1.bind(on_press=popup.dismiss)

"""
This is the second popup classes.
The EmptyErrorPopup class will display a popup if 
any of the text input boxes are empty.
"""
class EmptyErrorPopup(Popup):
    button1 = Button(text='Close', size_hint_y=(.4))
    label1 = Label(text='Please fill empty values')
    box1 = BoxLayout(orientation="vertical")
    box1.add_widget(label1)
    box1.add_widget(button1)
    content = box1
    popup = Popup(title='Error', content=content,
                  size_hint=(None, None), size=(600, 350))

    button1.bind(on_press=popup.dismiss)


class DNAMiddlewareKVApp(App):
    def build(self):
        global sm
        sm = ScreenManager()
        sm.add_widget(MainWindow(name='input'))
        return sm

if __name__ == "__main__":
    DNAMiddlewareKVApp().run()
