import re
import tkinter as tk
import tkinter.font as tf
from tkinter.filedialog import askopenfile
from string import digits

"""
Tree part
"""


class Tree:
    """
    define the tree class
    """

    def __init__(self, word):
        self.word = word  # word
        self.leftChild = None  # left child
        self.rightChild = None  # right child
        self.num = 1  # Word frequency

    def judge_word(self, w1, w2):
        # judge which word is bigger ,if w1>w2 return 1,else if w1<w2 return 2,if w1=w2 return 3
        if w1 > w2:
            return 1
        elif w1 < w2:
            return 2
        else:
            return 3

    def judge_l_r(self, n1, n2):
        # n1 is the Original node ,n2 is the new node ,judge n2 should be n1's left or right
        judge = self.judge_word(n1.word, n2.word)  # judge which node's word is bigger
        if judge == 1:  # w1>w2
            n1.insertLeft(n2)
        elif judge == 2:  # w1<w2
            n1.insertRight(n2)
        else:  # w1=w2
            n1.num += 1

    def insertLeft(self, node):
        # insert the left child
        if self.leftChild is None:  # if the tree has no left child
            self.leftChild = node  # add the left child
        else:  # if the tree has left child
            self.judge_l_r(self.leftChild, node)  # judge new node should be Original node's left or right

    def insertRight(self, node):
        # insert the left child
        if self.rightChild is None:  # if the tree has no left child
            self.rightChild = node  # add the left child
        else:  # if the tree has left child
            self.judge_l_r(self.rightChild, node)  # judge new node should be Original node's left or right

    def show(self):
        # show the tree
        # print(self.word, end=" ")
        # print("(", end="")
        if self.leftChild:
            self.leftChild.show()
        if self.rightChild:
            self.rightChild.show()
        # print(")", end="")

    def search(self, node, word):
        if node is None:  # if search no successfully
            return None  # return none
        # search the tree
        if self.judge_word(self.word, word) == 3:  # if search successfully
            return self.num  # return the word frequency

        elif node.judge_word(self.word, word) == 1:
            return node.search(self.leftChild, word)  # search the left child
        else:
            return node.search(self.rightChild, word)  # search the right child

    def normal_leven(self, str1, str2):
        len_str1 = len(str1) + 1
        len_str2 = len(str2) + 1
        # create matrix
        matrix = [0 for n in range(len_str1 * len_str2)]
        # init x axis
        for i in range(len_str1):
            matrix[i] = i
        # init y axis
        for j in range(0, len(matrix), len_str1):
            if j % len_str1 == 0:
                matrix[j] = j // len_str1

        for i in range(1, len_str1):
            for j in range(1, len_str2):
                if str1[i - 1] == str2[j - 1]:
                    cost = 0
                else:
                    cost = 1
                matrix[j * len_str1 + i] = min(matrix[(j - 1) * len_str1 + i] + 1,
                                               matrix[j * len_str1 + (i - 1)] + 1,
                                               matrix[(j - 1) * len_str1 + (i - 1)] + cost)

        return matrix[-1]

    def sort_min_words(self, nums, word):
        for i in range(len(nums) - 1):
            for j in range(len(nums) - i - 1):
                if self.normal_leven(nums[j], word) > self.normal_leven(nums[j + 1], word):
                    nums[j], nums[j + 1] = nums[j + 1], nums[j]
        return nums

    def get_min_words(self, word, min_words):

        # print(len(min_words))

        if len(word) <= 4:  # reduce count time
            if self.normal_leven(self.word, word) <= 2:  # if search successfully
                min_words.append(self.word)  # min_word add word
        else:
            if self.normal_leven(self.word, word) <= 3:  # if search successfully
                min_words.append(self.word)  # min_word add word

        if self.leftChild:
            min_words = self.leftChild.get_min_words(word, min_words)
            # return node.search(self.leftChild,word)
        if self.rightChild:
            min_words = self.rightChild.get_min_words(word, min_words)
        return min_words  # return min_words


with open("corpus.txt", 'r', encoding='utf-8') as f:
    data = f.read()
    # using translate and digits
    remove_digits = str.maketrans('', '', digits)
    res = data.translate(remove_digits)
    data_split = res.split()
print(data_split)


num = 0
# get tree
root = Tree("begin")
for i in range(len(data_split)):
    w = data_split[i].lower()
    if_word_punctuation = 0
    d = w[-1]  # the word's last letter
    if ((ord("Z") >= ord(d) >= ord("A")) or (ord("z") >= ord(d) >= ord("a"))) == 0:
        # if the word' last letter is punctuation
        w = w[:-1]  # remove the punctuation
    for d in w:
        if ((ord("Z") >= ord(d) >= ord("A")) or (ord("z") >= ord(d) >= ord("a"))) == 0:
            # print(w)
            num += 1
            if_word_punctuation = 1
            break
    if if_word_punctuation == 0:
        node = Tree(w)  # define node
        root.judge_l_r(root, node)  # add the new node into the tree

punctuation = [",", "."]
# punctuations = '''!()[]{};:"\,<>./ ? @ # $%^&*_~'''

for p in punctuation:
    node = Tree(p)  # define node
    root.judge_l_r(root, node)  # add the new node into the tree

"""
tkinter part
"""

window = tk.Tk()  # init

window.title('Wordpad')  # title

window.geometry('500x300')  # window size
ft = tf.Font(family='Times', size=16)  # set font

text_input = tk.Text(window, font=ft)  # input text
text_output = tk.Text(window, font=ft, state=tk.DISABLED)  # output text
text_input.place(width=250, height=250, x=20, y=20)  # place input text
text_output.place(width=180, height=210, x=300, y=60)  # place input text


min_words = []


def check(event):
    min_words.clear()
    text_output["state"] = tk.NORMAL  # set the output can be inserted word
    text_output.delete(1.0, tk.END)  # clean the output text
    word = text_input.get("0.0", "end").split()[-1]  # get the newest word
    print(word)

    if root.search(root, word) is not None:  # if root.search(root, word) != None
        text_output.insert("insert", "right")  # show right
    else:
        text_output.insert("insert", "wrong\n")  # show wrong

        kmin_words = root.sort_min_words(root.get_min_words(word, min_words), word)
        min_words_num = 0  # get the count of min_words show
        for m_w in kmin_words:
            min_words_num += 1
            text_output.insert("insert", m_w + "\n")  # show min_words
            if min_words_num == 5:  # if have showed 10 min_words ,break
                break
    text_output["state"] = tk.DISABLED  # set the output can not be inserted word
    # return min_words


text_input.bind('<space>', check)  # monitor the space


def xFunc1(event):
    print(f"The click coordinates are:x={event.x}y={event.y}")
    text_words = text_input.get("0.0", "end").split()  # get the input text words
    print(max((event.y - 20) // 18, 0))
    right_word = min_words[max((event.y - 20) // 18, 0)]  # get right word
    text_words[-1] = right_word  # renew input text
    text_input.delete(1.0, tk.END)  # clean the input text
    for t_word in text_words:
        text_input.insert("insert", t_word + " ")  # show the new input text word


text_output.bind("<Button-1>", xFunc1)


def browse_file():
    file = askopenfile(mode='r', filetypes=[('Text Flies', '*.txt'), ('Document Files', '*.doc')])
    if file is not None:
        content = file.read()


b2 = tk.Button(window, text='Open file', font=ft, command=browse_file)  # set button to openfile the
b2.place(width=100, height=30, x=370, y=20)


def check_all():
    text = text_input.get("0.0", "end").lower()
    res = re.sub(r'[^\w\s]', '', text)

    text_words = res.split()  # get the input text word
    text_input.delete(1.0, tk.END)  # clean the input text
    for t_word in text_words:
        if root.search(root, t_word):
            text_input.insert("insert", t_word + " ")  # show the new input text word
        else:
            ft = tf.Font(family='Times', size=15, weight=tf.BOLD, slant=tf.ITALIC,
                         underline=1, overstrike=1)  # set wrong font
            text_input.tag_config('tag', foreground='red', font=ft)  # set tag
            text_input.insert("insert", t_word, 'tag')  # show the new input text word,wrong word,
            text_input.insert("insert", ' ')  # show space


b = tk.Button(window, text='check', font=ft, command=check_all)  # set button to check the
b.place(width=60, height=30, x=300, y=20)

window.mainloop()
