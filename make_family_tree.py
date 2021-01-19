import numpy as np
from matplotlib import pyplot as plt


class Person:
    def __init__(self,
        first_name,
        last_name = None,
        birthdate = None,
        deathdate = None,
        parent1 = None,
        parent2 = None,
        parents = None,
        children = None,
        ID = None,
        spouses=None,
    ):
        # set up name
        self.first_name = first_name
        
        if last_name:
            self.name = ' '.join([first_name,last_name])
            self.last_name = last_name
        else:
            self.name = first_name
            self.last_name = None
        
        # set up unique identifier
        if ID is None:
            num = str.encode(self.name)
            self.ID = int.from_bytes(num,byteorder='big',signed=False)
        else:
            self.ID = ID

        # set up parents
        if parents:
            self.parents = parents
        else:
            self.parents = []
            if parent1: 
                self.parents.append(parent1)
                self.mother = parent1
            if parent2: 
                self.parents.append(parent2)
                self.father = parent2
       
        # set up children
        self.children = []
        if children:
            self.add_children(children)

        # set up spouses
        self.spouses = []
        if spouses:
            self.add_spouses(spouses)

    def add_child(self,child):
        self.children.append(child)
    
    def add_children(self,children):
        for child in children:
            self.add_child(child) 

    def add_spouse(self,spouse):
        self.spouses.append(spouse)
    
    def add_spouses(self,spouses):
        for spouse in spouses:
            self.add_spouse(spouse)

    def add_parent(self,parent):
        self.parents.append(parent)
    
    def add_parents(self,parents):
        for parent in parents:
            self.add_parent(parent)

    def get_oldest_ancestors(self):
        ancestors = []
        if self.parents is None:
            return [self]
        else:
            for parent in self.parents:
                ancestors.extend(parent.get_oldest_ancestors())
        return ancestors

    def get_number_of_generations_of_decendants(self):
        if len(self.children) == 0:
            return 0 
        else:
            return 1 + max([child.get_number_of_generations_of_decendants() for child in self.children])

def draw_parents_tree(person1,person2=None,figax=None):
    if figax is None:
        fig,ax = plt.subplots()
    if person2 is None:
        ax.text(0.5,0.8,person1.name,transform=ax.transAxes)
    else:
        ax.text(0.3,0.8,person1.name,transform=ax.transAxes)
        ax.text(0.7,0.8,person2.name,transform=ax.transAxes)
    n_children = 0
    for child in person1.children:
        if person2 is None:
            if person1 in child.parents:
                n_children += 1
        else:
            if (person1 in child.parents) and (person2 in child.parents):
                n_children += 1
    for i in range(n_children):
        ax.axvline(1./(2.*n_children) + float(i)/n_children,0,0.6)
    return fig,ax    

def draw_tree(people):
    ancestors = np.unique([person.get_oldest_ancestors() for person in people])
    
    # find number of generations and number 
    # of cousins at bottom of tree to size figure
    generations = max([person.get_number_of_generations_of_decendants() for person in ancestors])

if __name__=="__main__":
    mom = Person("mom")
    dad = Person("dad")
    bro = Person("bro")
    sis = Person("sis")
    mom.add_children([bro,sis])
    dad.add_children([bro,sis])
    mom.add_spouse(dad)
    dad.add_spouse(mom)
    bro.add_parents([mom,dad])
    sis.add_parents([mom,dad])
    fig,ax = draw_parents_tree(mom,dad)
    fig.savefig('test.png')
