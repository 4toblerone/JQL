from Lexer import Lexer
from collections import deque, Iterable
import operator
import json

class Node(object):
    """docstring for Node"""
    def __init__(self):
        self.childrens=[]


    def add(self,child):
        self.childrens.append(child)

    def dooperation(self):
        """do operation on childrens, eval"""
        pass


    #probaj generator!
    #ukoliko treba da predje na poslednje dete u listi vraca None, zasto?
    #verovatno neki slucaj (koji ne vidim trenutno) 
    #pri rekurziji nije pokriven
    #Mora funkcija uvek da vrati nesto.

    #da li da menjam str metodu tako da iskuljucuje ako je jedno dete i to token
    #ili da leafnode-ovima dodam atribut token pa da dooperation vraca samo taj attribute 

    #da li da uvedem LeafNode klasu koju ce svi leafnode-ovi nasledjivati i koja ce u odnosu
    #na Node klasu imati samo dodat atribut za smestanje tokena i cija ce doooperation vracati 
    #taj atribut? 

    #Sta je los dizajn? 
    def __str__(self):
        print "<"+self.__class__.__name__+">"
        if len(self.childrens)==0:
            return "Nema vise dece ova grana"
        for child in self.childrens:
            print child.__str__()
        return "to"
class LeafNode(Node):
    def __init__(self,token):
        super(LeafNode,self).__init__()
        self.token = token

    def dooperation(self):
        return self.token

class ExprNode(Node):
    def dooperation(self):
        return self.childrens[0].dooperation()

class QueryNode(Node):
    def dooperation(self):
        return self.childrens[0].dooperation()

class RemoveExprNode(Node):
    def dooperation(self):
        return self.childrens[0].dooperation()

class AddExprNode(Node):
    pass

class UpdateExprNode(Node):
    pass

class GetExprNode(Node):
    pass

class WutNode(Node):
    
    def dooperation(self):

        if len(self.childrens)>1:
            jsonobject = getjsonobject(paramlist, loaded_json_string)
        else:
            pass

class ObjectNode(Node): 
    def dooperation(self):
        """Returns 'path' to the object as a list of keys"""
        lista = []
        for child in self.childrens:
            lista.append(child.dooperation())
        return list(flatten(lista))

class ConditionNode(Node):
    
    def dooperation(self):
        listl=[]
        for child in self.childrens:
            listl.append(child.dooperation())
        return listl
    

class BasicConditionNode(Node):
    
    def dooperation(self):
        """Returns tuple with key to objects child, comparison operator,
            and value to witch it will be later compared to """
        key = self.childrens[0].dooperation()
        value = self.childrens[2].dooperation()
        comparisonop = self.childrens[1].dooperation() 
        return (key, comparisonop, value)



class ValueNode(Node):
    def dooperation(self):
        return self.childrens[0].value

class JsonStringNode(LeafNode):
    pass

class MathExprNode(Node):
    pass

class StringExprNode(Node):
    pass

class ComparisonOpNode(Node):
    
    def dooperation(self):
        return self.childrens[0].dooperation()

class LessNode(LeafNode):

    def dooperation(self):
        return operator.lt

class GreaterNode(LeafNode):

    def dooperation(self):
        return operator.gt

class TwoEqualNode(LeafNode):

    def dooperation(self):
        return operator.eq
    
class LessOrEqualNode(LeafNode):

    def dooperation(self):
        return operator.le

class EqualOrGreaterNode(LeafNode):

    def dooperation(self):
        return operator.ge

class WordNode(LeafNode):
    
    def dooperation(self):
        return self.token.value
        
class OperatorNode(Node):
    
    def dooperation(self):
        return self.childrens[0].dooperation()

class NumberNode(LeafNode):
    
    def dooperation(self):
        return self.childrens[0].value

class PlusNode(LeafNode):
   
    def dooperation(self):
        return operator.add

class MinusNode(LeafNode):
    
    def dooperation(self):
        return operator.sub

class TimesNode(LeafNode):

    def dooperation(self):
        return operator.mul

class DivideNode(LeafNode):

    def dooperation(self):
        return operator.div

def flatten(listl):
        for element in listl:
            if isinstance(element, Iterable) and not isinstance(element,basestring):
                for sub in flatten(element):
                    yield sub
            else:
                yield element

def flattenlistoftuples(listoftuples):
    for element in listoftuples:
            if isinstance(element, Iterable) and not isinstance(element,basestring) \
                and not isinstance(element,tuple):
                
                for sub in flatten(element):
                    yield sub
            else:
                yield element


def createnode(class_name,*args):
    node_class = globals()[class_name]
    instance = node_class(*args)
    return instance

def createleaf(rule,tokenvalue):
    leafnode = createnode(nodes[rule],tokenvalue)
    return leafnode

def getjsonobject(paramlist, loaded_json_string,conditions=None):
    """Returns json object, where paramlist is 'path' to it. 
        If path to it is not valid a.k.a object doesn't exists
        it will return None"""   
    list_of_objects = reduce(dict.get,paramlist,loaded_json_string)

    #create filter function which will evalute using by key and comparison operator
    #from conditions
        
    return list_of_objects

def checkallconditions():
    #to use any or to use reduce which doesn't shortcircuit 
    pass


def filter(listtofilter):
    pass

def proba():
    lista  = [1,2,3,6]
    ops = [operator.le, operator.lt]
    for x in lista:
        for op in ops:
            if op(x,3):
                yield x



jsonstring='{"dict1":{"dict2":{"ime":"sale" , "titula" : "car"}}}'

nodes={"expr" : "ExprNode", 
        "queryexpr" : "QueryNode",
        "removeexpr" : "RemoveExprNode",
        "addexpr" : "AddExprNode",
        "updateexpr" : "UpdateExprNode",
        "getexpr" : "GetExprNode",
        "wut" : "WutNode",
        "object": "ObjectNode",
        "condition": "ConditionNode",
        "basiccondition" : "BasicConditionNode",
        "value" : "ValueNode",
        "jsonstring" : "JsonStringNode",
        "mathexpr" : "MathExprNode",
        "stringexpr" : "StringExprNode",
        
        "comparisonop" : "ComparisonOpNode",
        "less" : "LessNode",
        "greater" : "GreaterNode",
        "lessorequal" : "LessOrEqualNode",
        "equalorgreater" : "EqualOrGreaterNode",
        "twoequal" : "TwoEqualNode",

        "word": "WordNode",
        "number":"NumberNode",
        
        "operator" : "OperatorNode",
        "plus": "PlusNode",
        "minus": "MinusNode",
        "times" : "TimesNode",
        "divide" : "DivideNode"
        }

grammar={"expr":[["queryexpr"] , ["mathexpr"] , ["stringexpr"]],#there is a need for "cushion" rule for some reasone parser wont parserwont parse it directly
        "queryexpr" : [["removeexpr"],["addexpr"],["updateexpr"],["getexpr"]],
        "removeexpr" : [["object"]],#[["from", "wut", "remove" , "object"]],
        "getexpr" : [["from","object","get","wut"]],
        "addexpr" : [["to","object","add","jsonstring_start","jsonstring","jsonstring_end"]],
        "updateexpr" : [["update" , "wut", "to" , "value"]],
        "object" : [["word","arrow","object"], ["word"]],
        "condition" : [["basiccondition", "and","condition"], ["basiccondition"]],
        "basiccondition" : [["object", "comparisonop","value"]],
        "value" : [["word"],["number"]],
        "wut" : [["object", "where", "condition"], ["object"]],
        "comparisonop" : [["less"],["greater"],["twoequal"],["lessorequal"],["greaterorequal"]],
        "mathexpr" : [["number", "operator", "mathexpr"], ["number"]],
        "operator" : [["plus"],["minus"],["times"],["divide"]],
        "stringexpr" : [[]]
        }

# grammar={"expr":[["mathop"]],
#            "mathop":[["number", "operator" , "mathop"] , ["number"]],
#            "operator": [["plus"],["minus"]] }

tokenList = Lexer().breakDownStringToTokens("nekiobjekat->deteobjekta->unuceobjekta")

izbaceni={} 

print tokenList

def resetfileds(fn):
        def wrapper(self, arg):
            result = fn(self,arg)
            self.__init__()
            return result 
        return wrapper

class ParseText:    

    def __init__(self):
        self.cacastack  = ['expr']
        self.gdejestao =  {'expr':[[0,0,0]]} #3. int sluzi za broja tokena tj da bi se znalo koliko unazad da se vrati u slucaju da ne naidje na odgvarajuce pravilo
                              #2. int oznacava odabrano prailo
                              #sta je 1. predjeno pravilo u ovom slucaju token , tj pomeraj u pravilo listi
        self.gdejebio=[createnode(nodes["expr"])]
        self.x=0

    #@resetfileds
    def parse(self,tokenList):
    
        listapravila = grammar[self.cacastack[-1]][self.gdejestao[self.cacastack[-1]][-1][1]]
        #ovde provera da li je dosao i do kraja pravila
        if len(listapravila[self.gdejestao[self.cacastack[-1]][-1][0]:])==0: 
            if len(self.cacastack)>1:
                self.cacastack.pop()
                return self.parse(tokenList)
            elif len(tokenList)>self.x:
                return False

        if self.x == len(tokenList):
            if len(self.cacastack)==1 : 
                return True
            else: 
                return False
        
        if self.gdejestao[self.cacastack[-1]][-1][0]==0 and len(listapravila) > len(tokenList)-self.x:
       
            if len(grammar[self.cacastack[-1]])-1>self.gdejestao[self.cacastack[-1]][-1][1]:
            #prebaci na sledece pravilo 
                self.gdejestao[self.cacastack[-1]][-1][1]+=1
                #ovde izbrisi sa gdejebio poslednji i obrisi decu njegovog caleta   
                return self.parse(tokenList)
            else:
                return False
        
        for index, pravilo in enumerate(listapravila[self.gdejestao[self.cacastack[-1]][-1][0]:]): 
        #proveri da li je list/terminal i da li je jednak tipu tokena
            self.gdejebio.append(pravilo)
            if pravilo not in grammar.keys(): #and pravilo==tokenList[x].type:
                #za svaki sledeci pomeri pokazivac
                #mora posle ovo jer se na 81 liniji gleda nova verzija a ne treba
                self.gdejestao[self.cacastack[-1]][-1][0]+=1
                #znaci da je list, proveri da li je to taj tip tokena (vodi racuna na velika/mala slova)
                if self.x <=len(tokenList)-1 and pravilo==tokenList[self.x].type.lower():
                    #napravi Node objekat za terminal ovde i dodaj ga kao dete poslednjem sa caca stack-a
                    # terminalnode = createnode(pravilo)
                    # gdejebio[-1].add(terminalnode)
                    self.x+=1
                    self.gdejestao[self.cacastack[-1]][-1][2]+=1
                    #da li je presao jednu listu pravila , ako jeste i ako na cacastack-u ima vise od jednog
                    if self.gdejestao[self.cacastack[-1]][-1][0]==len(listapravila):
                        if len(self.cacastack)>1:
                            #ne moze da se vrati skroz do kraja , tj moze samo do expr
                            if len(self.gdejestao[self.cacastack[-1]])>1:
                                poslednji = self.gdejestao[self.cacastack[-1]].pop()
                                izbaceni[self.cacastack[-1]].append((izbaceni[self.cacastack[-1]][0],poslednji))
                                #del self.gdejestao[self.cacastack[-1]][-1]
                            self.cacastack.pop()
                            return self.parse(tokenList)
                        else:
                            return False
                elif self.x <=len(tokenList)-1 and pravilo!=tokenList[self.x].type.lower():
                    if len(grammar[self.cacastack[-1]])-1>self.gdejestao[self.cacastack[-1]][-1][1]: 
                        
                        self.gdejestao[self.cacastack[-1]][-1][1]+=1
                        #resetuj gde je stao tj x == 0  
                        self.gdejestao[self.cacastack[-1]][-1][0]=0
                        #smanjujem x za sve pronadjene u tom pravilu
                        self.x-=self.gdejestao[self.cacastack[-1]][-1][2]   
                        #popuje ovaj, tj poslednji
                        self.gdejestao[self.cacastack[-1]][-1][2]=0     
                        #del gdejestao[cacastack[-1]][-1]   #baca out ouf range na 87
                        return self.parse(tokenList)
                    elif len(self.cacastack)>1:
                        self.x-=self.gdejestao[self.cacastack[-1]][-1][2] 
                        self.gdejestao[self.cacastack[-1]][-1][2]=0
                       
                        del self.cacastack[-1]
            
                        if len(grammar[self.cacastack[-1]])-1>self.gdejestao[self.cacastack[-1]][-1][1]:
                           
                            self.gdejestao[self.cacastack[-1]][-1][1]+=1
                            self.gdejestao[self.cacastack[-1]][-1][0]=0
                            self.x-=self.gdejestao[self.cacastack[-1]][-1][2] 
                            self.gdejestao[self.cacastack[-1]][-1][2]=0
                        else:
                            #stavi da je dosao do kraja pravila u gdejestao jer ako je == samo ce da predje na sledece pravilo a ne niz pravila
                            print grammar[self.cacastack[-1]][self.gdejestao[self.cacastack[-1]][-1][1]]
                            self.gdejestao[self.cacastack[-1]][-1][0]=len(grammar[self.cacastack[-1]][self.gdejestao[self.cacastack[-1]][-1][1]])    
                        
                        return self.parse(tokenList)

                else:
                    return False
            #ako nije list/terminal nadji listu sa tim key-em u dictionary-u i dodaj ga na caca stack
            else:
                #gdejestao[cacastack[-1]][0]=index+1 #nije tu stao, jer index uvek krece od nule 
                self.gdejestao[self.cacastack[-1]][-1][0]+=1
                self.cacastack.append(pravilo)

                if pravilo not in self.gdejestao:
                    self.gdejestao[pravilo]=[]
                self.gdejestao[pravilo].append([0,0,0])
                izbaceni[pravilo]=izbaceni.get(pravilo,[-1]) 
                izbaceni[pravilo][0]+=1#poveca brojac ukupnih "cvorova" jednog tipa za jedan
                return self.parse(tokenList)


def mergeall(izbaceni, gdejestao):

    def merge(popeditems, key):
        
        lista = []
        i=0
        gdejestaodeo=deque(gdejestao[key])
        length = len(popeditems)+len(gdejestaodeo)#3
        while i<length:#ne moze plus jer ako nista nema toliko u vecoj listi
            if popeditems and i==popeditems[0][0]:
                print i
                lista.append(popeditems[0][1])
                del popeditems[0]
            elif len(gdejestaodeo)>0:
                lista.append(gdejestaodeo[0])
                del gdejestaodeo[0]
            i+=1
        return lista
    
    for key,value in izbaceni.iteritems():
        if len(value)>1:
            gdejestao[key]=merge(value[1:],key)
    return gdejestao
#print p.gdejestao

#ovo treba u zasebnoj klasi, cini mi se da je bolje nego closure
#promeni imena atributa, daj nesto smisleno, prvi i stack nisu bas
#p.gdejestao i trace , pogledaj razlike tj da li ih ima
class AST(object):

    def __init__(self,tokenlist,trace):
        self.stack = [ExprNode()]
        self.stack2  = []
        self.dek = deque(tokenlist)
        self.trace = trace

    def createtree(self,key):
        rulenum = self.trace[key][0][1]
        #print "createit", grammar[key][rulenum],rulenum
        for index, pravilo in enumerate(grammar[key][rulenum]):
            #print "yooooooooooo",pravilo
            if pravilo in nodes:
                #print pravilo,"usao ovdeee"
                if pravilo not in grammar:
                #stack[-1].add(createnode(nodes[pravilo]))
                #dynamicly create leafNodes which are not in the nodes dict
                #example the word "for" has no real value inside queryexpr 
                #or maybe it is better no to have it at all as a node?
                #if it isn't in nodes just skip it
                #make sure that nodes contains 
                    print "dek" , self.dek
                    self.stack[-1].add(createleaf(pravilo, self.dek.popleft() )) #pop stack2, i kopiraj listu tokena
                    if index == len(grammar[key][rulenum])-1 and len(self.stack)>1:
                        self.stack.pop()
                        del self.trace[key][0]
                else:
                    #print"yo",pravilo
                    node = createnode(nodes[pravilo])
                    self.stack[-1].add(node)
                    if index == len(grammar[key][rulenum])-1:
                        if len(self.stack)==1:
                            self.stack2.append(self.stack.pop())
                        else:
                            self.stack.pop()
                        del self.trace[key][0]

                    self.stack.append(node)
                    self.createtree(pravilo)
            else:
                self.dek.popleft()

#u svim LeafNode-ovima ide plus token, index+=1 deo mora da je problem
#da li da odradim kopiju sa deque i da radim popleft(sigurno je manje efikasno od indexa) ili pogledam ovo sa indexom
# mergeall(izbaceni,p.gdejestao)
# p.gdejestao = mergeall(izbaceni, p.gdejestao)
# print p.gdejestao
p = ParseText()
print p.parse(tokenList)
# print nodes['number']
# print globals()[nodes['number']]
# #createnode("number", "probica")
ast =  AST(tokenList,mergeall(izbaceni, p.gdejestao))
ast.createtree("expr")
print ast.stack2[0].dooperation(),"printaj listu"
# print ast.stack2[0].childrens[0].childrens[1].dooperation()
#napravi tree walker metodu , tj interpretera koja ce da obidje celo stablo pozivajuci dooperation