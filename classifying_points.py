import pandas as pd
import simpleaudio as sa
import numpy as np

file = 'data.csv'
file_reader = pd.read_csv(file)

x_axis = file_reader['Duration']
y_axis = file_reader['Pulse']

# use a hashtable to create nodes (based on x value) with all of the data from each node
class LinkedList:
  class Node:
    def __init__(self, xval, yval, prior = None, next = None):
      def calc_frequency(self):
        offset = 32676
        allowed_freqeuncies = [8000, 11025, 16000, 22050, 32000, 44100, 48000, 88200, 96000, 192000]
        if self.y_val is None:
          frequency = None
        elif (self.y_val <= offset):
          frequency = allowed_freqeuncies[0]
        elif (self.y_val <= (offset * 10**3)):
          frequency = allowed_freqeuncies[1]
        elif (self.y_val <= (offset * 10**6)):
          frequency = allowed_freqeuncies[2]
        elif (self.y_val <= (offset * 10**9)):
          frequency = allowed_freqeuncies[3]
        elif (self.y_val <= (offset * 10**12)):
          frequency = allowed_freqeuncies[4]
        elif (self.y_val <= (offset * 10**15)):
          frequency = allowed_freqeuncies[5]
        elif (self.y_val <= (offset * 10**18)):
          frequency = allowed_freqeuncies[6]
        elif (self.y_val <= (offset * 10**21)):
          frequency = allowed_freqeuncies[7]
        elif (self.y_val <= (offset * 10**24)):
          frequency = allowed_freqeuncies[8]
        else:
          frequency = allowed_freqeuncies[9]
        return frequency
      
      def calc_byte_sample(self):
        if (self.y_val is None):
          byte_samp = 0
        elif (self.x_val >= 0 and self.y_val >= 0):
          byte_samp = 2
        elif (self.x_val < 0 and self.y_val >= 0):
          byte_samp = 1
        elif (self.x_val >= 0 and self.y_val < 0):
          byte_samp = 3
        else:
          byte_samp = 4
        return byte_samp
      
      self.x_val = xval
      self.y_val = yval
      self.frequency = calc_frequency(self)
      self.byte_sample = calc_byte_sample(self)
      self.prior = prior
      self.next = next
  
  def __init__(self):
    self.size = 0
    self.head = LinkedList.Node(None, None) # dummy node
    self.head.next = self.head
    self.head.prior = self.head
  
  def prepend(self, xval, yval):
    self.size += 1
    n = LinkedList.Node(xval, yval, prior = self.head, next = self.head.next)
    self.head.next.prior = n
    self.head.next = n

  def append(self, xval, yval):
    self.size += 1
    node = LinkedList.Node(xval, yval, prior = self.head.prior, next = self.head)
    self.head.prior.next = node
    self.head.prior = node
  
  def insert(self, xval, yval):
    if (self.head.prior.x_val is None):
      self.append(xval, yval)
    elif (xval > self.head.prior.x_val):
      self.append(xval, yval)
    elif (xval < self.head.next.x_val):
      self.prepend(xval, yval)
    else:
      current = self.head.next
      while (xval > current.x_val):
        current = current.next
      while ((current.next != self.head) and (current.x_val == xval) and (current.y_val < yval)):
        current = current.next
      node = LinkedList.Node(xval, yval, prior = current, next = current.next)
      current.next.prior = node
      current.next = node
      self.size += 1
  
  def __str__(self):
    return '[' + ', '.join(str(x) for x in self) + ']'
  
  def __len__(self):
    return self.size
  
  def __iter__(self):
    node = self.head.next
    while node is not self.head:
      yield [node.x_val, node.y_val, node.frequency, node.byte_sample]
      node = node.next

#use pattern detection in class to sort through and create a dictionary with matching frequency, channels, and bytes
def record_pattern(linked):
  pattern_dict = {}
  current_guess = 0
  space = 0
  time =  200
  current = linked.head.next
  while (current is not linked.head):
    if (current.prior == linked.head):
      pattern_dict[current_guess] = np.zeros((time * (len(linked) - 1), 2))
    else:
      if ((current.frequency != current.prior.frequency) or (current.byte_sample != current.prior.byte_sample)):
        space = 0
        current_guess += 1
        pattern_dict[current_guess] = np.zeros((time * (len(linked) - 1), 2))
      pattern_dict[current_guess][(time*space):(time*(space + 1)), 0] = round(current.y_val)
      pattern_dict[current_guess][(time*space):(time*(space + 1)), 1] = round(current.x_val)
      space += 1
    current = current.next
  return pattern_dict


# method to edit the points in each of the numpy arrays
def edit_points(pattern_dict):
  for nump in pattern_dict:
    pattern_dict.get(nump)[0] *= round((32767 / max(pattern_dict.get(nump)[0])), 0)
    pattern_dict.get(nump)[1] *= round((32767 / max(pattern_dict.get(nump)[1])), 0)
  return pattern_dict


#plays the edited points
def play_points(pattern_dict):
  for nump in pattern_dict:
    play_obj = sa.play_buffer(pattern_dict.get(nump), 2, 2, 8000)
    play_obj.wait_done()

# create a linked list with the x and y values from the data
def create_linked():
  data = LinkedList()
  for i in range(len(x_axis)):
    data.insert(x_axis[i], y_axis[i])
  play_points(edit_points(record_pattern(data)))

# call the create dict and edit
create_linked()