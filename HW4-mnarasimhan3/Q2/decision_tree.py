from util import entropy, information_gain, partition_classes
import numpy as np 
import ast

class DecisionTree(object):
    def __init__(self):
        # Initializing the tree as an empty dictionary or list, as preferred
        #self.tree = []
        #self.tree = {}
        self.tree_sub = np.array([])
        self.tree_main = np.array([])
        

    def learn(self, X, y):
        # TODO: Train the decision tree (self.tree) using the the sample X and labels y
        # You will have to make use of the functions in utils.py to train the tree
        
        # One possible way of implementing the tree:
        #    Each node in self.tree could be in the form of a dictionary:
        #       https://docs.python.org/2/library/stdtypes.html#mapping-types-dict
        #    For example, a non-leaf node with two children can have a 'left' key and  a 
        #    'right' key. You can add more keys which might help in classification
        #    (eg. split attribute and split value)
     
        tree=np.array([])
        if X.shape[0] <= 1:
       
            res = np.array([1000,y,9999, 9999])
            res = np.reshape(res, (1,4))
            self.tree_sub = res
            return res
        elif np.unique(y).size == 1:
            res = np.array([1000,np.mean(y),9999,9999])
            res = np.reshape(res, (1,4))
            self.tree_sub = res
            return res
        else:
        
              max_inf_gain = 0
              split_attribute = 0
              splitVal = np.median(X[:,split_attribute],axis=0)
              for i in range(X.shape[1]):
                  temp = np.median(X[:,i],axis=0)
                  X_l, X_r, y_l, y_r = partition_classes(X,y,i,temp)
                  inf_gain = information_gain(y, [y_l, y_r])
                  if inf_gain > max_inf_gain:
                      max_inf_gain = inf_gain
                      splitVal = temp
                      split_attribute = i
                      
              X_left, X_right, y_left, y_right = partition_classes(X,y,split_attribute,splitVal)
       
              
              if np.array_equal(X_left, X):
                  res = np.array([1000,np.mean(y),9999,9999])
                  res = np.reshape(res,(1,4))
                  return res
              
              lefttree = self.learn(X_left, y_left)
              righttree = self.learn(X_right, y_right)
        
              root = [split_attribute, splitVal, 1, lefttree.shape[0]+1]
          
              tree = np.hstack((tree,root))
            
              for i in range(lefttree.shape[0]):
                  temp = np.ravel(lefttree[i]).tolist()
                  tree = np.hstack((tree,temp))
            
              for i in range(righttree.shape[0]):
                  temp = np.ravel(righttree[i]).tolist()
                  tree = np.hstack((tree,temp))  
           
              tree = np.reshape(tree, (int(tree.shape[0]/4),4))    
              self.tree_main = tree
              
        
              return tree
            

    def classify(self, record):
        # TODO: classify the record using self.tree and return the predicted label
            
        if self.tree_main.size == 0 and self.tree_sub.size>0:
                self.tree_main = self.tree_sub
     
        index = 0
      
        while self.tree_main[index,0] != 1000:
            if (record[int(self.tree_main[index,0])]) <= self.tree_main[index,1]:
                index = index + int(self.tree_main[index,2])
            else:
                
                index = index + int(self.tree_main[index,3])
                 
 
        return self.tree_main[index,1]
             
            


