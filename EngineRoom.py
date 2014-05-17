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
    
    def dooperation(self):
        path_to_object = self.childrens[0].dooperation()
        from_object = getjsonobject(path_to_object, jsonstring)
        result = self.childrens[1].dooperation(from_object)
        return result


class WutNode(Node):
    
    def dooperation(self,jsonstring):
        path_to_object = self.childrens[0].dooperation()
        try:
            conditions = flattenlistoftuples(self.childrens[1])
        except IndexError:
            conditions=None
        jsonobject = getjsonobject(path_to_object, jsonstring, conditions)
        return jsonobject

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

def getjsonobject(paramlist, loaded_json_string,conditions=None):
    """Returns json object, where paramlist is 'path' to it. 
        If path to it is not valid a.k.a object doesn't exists
        it will return None"""
    jsonobject = reduce(dict.get,paramlist,loaded_json_string)
    if conditions is not None:
        result = []
        for jo in jsonobject:
            evaluated_conditions = [condition[1](getjsonobject(condition[0],jo),condition[2]) \
                                    for condition in conditions]
            if all(evaluated_conditions):
                result.append(jo)
        return result
    else:
        return jsonobject

def createnode(class_name,*args):
    node_class = globals()[class_name]
    instance = node_class(*args)
    return instance

def createleaf(rule,tokenvalue):
    leafnode = createnode(nodes[rule],tokenvalue)
    return leafnode


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

# grammar={"expr":[["queryexpr"] , ["mathexpr"] , ["stringexpr"]],#there is a need for "cushion" rule for some reasone parser wont parserwont parse it directly
#         "queryexpr" : [["removeexpr"],["addexpr"],["updateexpr"],["getexpr"]],
#         "removeexpr" : [["from", "wut", "remove" , "object"]],
#         "getexpr" : [["from","object","get","wut"]],
#         "addexpr" : [["to","object","add","jsonstring_start","jsonstring","jsonstring_end"]],
#         "updateexpr" : [["update" , "wut", "to" , "value"]],
#         "object" : [["word","arrow","object"], ["word"]],
#         "condition" : [["basiccondition", "and","condition"], ["basiccondition"]],
#         "basiccondition" : [["object", "comparisonop","word"]],
#         "value" : [["word"],["number"]],
#         "wut" : [["object", "where", "basiccondition"], ["object"]],
#         "comparisonop" : [["less"],["greater"],["twoequal"],["lessorequal"],["greaterorequal"]],
#         "mathexpr" : [["number", "operator", "mathexpr"], ["number"]],
#         "operator" : [["plus"],["minus"],["times"],["divide"]],
#         "stringexpr" : [[]]
#         }

grammar={"expr":[["andmathop"]],
           "andmathop":[["mathop","and","andmathop"],["mathop"]],
           "mathop":[["number", "operator", "mathop"],["number"]],
           "operator": [["plus"]] }

tokenList = Lexer().breakDownStringToTokens(" 7 + 7 and 7")
print tokenList
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
        self.helperstack =[['expr',0]]
        self.gdejestao =  {'expr':[[0,0,0]]} #3. int sluzi za broja tokena tj da bi se znalo koliko unazad da se vrati u slucaju da ne naidje na odgvarajuce pravilo
                              #2. int oznacava odabrano prailo
                              #sta je 1. predjeno pravilo u ovom slucaju token , tj pomeraj u pravilo listi
        self.gdejebio=[createnode(nodes["expr"])]
        self.x=0


    def addnewtohs(self,pravilo):
        self.helperstack.append([pravilo,0])


    def uphelperstack(self):
        for upstairrule in self.helperstack:
            upstairrule[1]+=1

    def removefromhs(self):
        tocut = self.helperstack[-1][1]
        del self.helperstack[-1]
        for upstairrule in self.helperstack:
            upstairrule[1]-=tocut
        #dodatak
        return tocut


    def deletelasths(self):
        del self.helperstack[-1]

    #@resetfileds
    def parse(self,tokenList):
    
        listapravila = grammar[self.cacastack[-1]][self.gdejestao[self.cacastack[-1]][-1][1]]
        #ovde provera da li je dosao i do kraja pravila
        if len(listapravila[self.gdejestao[self.cacastack[-1]][-1][0]:])==0: 
            print "a"
            if len(self.cacastack)>1:
                self.cacastack.pop()
                return self.parse(tokenList)
            elif len(tokenList)>self.x:
                print "nulto"
                print self.cacastack, self.gdejestao, self.gdejebio
                return False

        #da li je presao sve tokene u listi, ako jeste 
        if self.x == len(tokenList):
            print "b"
            if len(self.cacastack)==1 : 
                # print listapravila, self.x , self.cacastack
                print "gde je stao ", self.gdejestao
                # print "gde je bio ", self.gdejebio
                print "izbaceni", izbaceni

                return True
            else:
                print "*************"
                print self.gdejestao[self.cacastack[-1]][-1][0] , len(grammar[self.cacastack[-1]][self.gdejestao[self.cacastack[-1]][-1][1]])-1
                if self.gdejestao[self.cacastack[-1]][-1][0]==len(grammar[self.cacastack[-1]][self.gdejestao[self.cacastack[-1]][-1][1]])-1:
                    print "e desi yooooooooooooooo"
                    if len(self.cacastack)>1:
                        #ne moze da se vrati skroz do kraja , tj moze samo do expr
                        if len(self.gdejestao[self.cacastack[-1]])>1:
                            poslednji = self.gdejestao[self.cacastack[-1]].pop()
                            izbaceni[self.cacastack[-1]].append((izbaceni[self.cacastack[-1]][0],poslednji))
                            #del self.gdejestao[self.cacastack[-1]][-1]
                        self.cacastack.pop()
                        print "yooo"
                        return self.parse(tokenList)
                print listapravila, self.x , self.cacastack
                print "gde je stao ", self.gdejestao
                print "gde je bio ", self.gdejebio
                #vidi da li je dosao do kraja pravila ako jeste popni ga gore
                return False
        
        # ako je na pocetku odredjene grupe pravila (jedno pravilo moze da ima vise grupa pravila)
        # i ako je duzina te grupe pravila veca oda broja preostalih tokena koje treba preci
        if self.gdejestao[self.cacastack[-1]][-1][0]==0 and len(listapravila) > len(tokenList)-self.x:
            #ako je broj grupa pravila koja proizilazi iz poslednjeg na stack-u veca od broja predjenih grupa
            #tj ako nije presao sve grupe pravila
            print "mwua",self.x
            print self.cacastack
            if len(grammar[self.cacastack[-1]])-1>self.gdejestao[self.cacastack[-1]][-1][1]:
                #prebaci na sledecu grupu pravila 
                self.gdejestao[self.cacastack[-1]][-1][1]+=1
                #ovde izbrisi sa gdejebio poslednji i obrisi decu njegovog caleta
                self.gdejestao[self.cacastack[-1]][-1][0]=0
                print 396
                #self.x-=self.gdejestao[self.cacastack[-1]][-1][2]

                self.x-=self.removefromhs()
                self.gdejestao[self.cacastack[-1]][-1][2]=0
                print "desi bebo"
                return self.parse(tokenList)
            else:
                print "drugo","x je ",self.x, self.cacastack , self.gdejebio, self.gdejestao
                print "e ", self.helperstack, listapravila
                return False
        
        for index, pravilo in enumerate(listapravila[self.gdejestao[self.cacastack[-1]][-1][0]:]): 
        #proveri da li je list/terminal i da li je jednak tipu tokena
            print self.x, pravilo
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
                    print "povecao je x za jedan ",self.x , pravilo
                    self.gdejestao[self.cacastack[-1]][-1][2]+=1
                    self.uphelperstack()
                    #da li je presao jednu listu pravila , ako jeste i ako na cacastack-u ima vise od jednog
                    if self.gdejestao[self.cacastack[-1]][-1][0]==len(listapravila):
                        #print "423"
                        if len(self.cacastack)>1:
                            #ne moze da se vrati skroz do kraja , tj moze samo do expr
                            if len(self.gdejestao[self.cacastack[-1]])>1:
                                poslednji = self.gdejestao[self.cacastack[-1]].pop()
                                izbaceni[self.cacastack[-1]].append((izbaceni[self.cacastack[-1]][0],poslednji))
                                #del self.gdejestao[self.cacastack[-1]][-1]
                            self.cacastack.pop()
                            #self.deletelasths()
                            return self.parse(tokenList)
                        else:
                            print "trece"
                            return False
                    #print "436"

                """U OVOM DELU TREBA SKINUTI SA GDE JE STAO STACKA!!!"""
                #ukoliko nije dosao do poslednjeg tokena i trenutno pravilo nije jednako trenutnom tokenu
                elif self.x <=len(tokenList)-1 and pravilo!=tokenList[self.x].type.lower():
                    print "usao je u if",pravilo

                    #ukoliko duzina liste pravila koja proizilazi iz poslednjeg sa cacastack-a 
                    #veca od
                    if len(grammar[self.cacastack[-1]])-1>self.gdejestao[self.cacastack[-1]][-1][1]: 
                        print "da li je i ovde usao a trebalo bi",self.x
                        self.gdejestao[self.cacastack[-1]][-1][1]+=1
                        #resetuj gde je stao tj x == 0  
                        self.gdejestao[self.cacastack[-1]][-1][0]=0
                        #smanjujem x za sve pronadjene u tom pravilu
                        """ovde x treba umanjiti za poslednji sa helperstack-a , popovati helperstack-a da bi se 
                        pravi 'poslednji' uzimao u obzir"""
                        print 449 , self.x#, self.removefromhs()
                        #self.x-=self.gdejestao[self.cacastack[-1]][-1][2]  
                        print self.helperstack
                        self.x-= self.removefromhs()
                        #popuje ovaj, tj poslednji

                        self.gdejestao[self.cacastack[-1]][-1][2]=0    
                        print self.x 
                        #del gdejestao[cacastack[-1]][-1]   #baca out ouf range na 87
                        return self.parse(tokenList)
                    elif len(self.cacastack)>1:
                        print 458
                        #self.x-=self.gdejestao[self.cacastack[-1]][-1][2] 
                        self.x-=self.removefromhs()
                        self.gdejestao[self.cacastack[-1]][-1][2]=0
                        print "prvi elif"
                        del self.cacastack[-1]
            
                        if len(grammar[self.cacastack[-1]])-1>self.gdejestao[self.cacastack[-1]][-1][1]:
                            print "drugi elif"
                            self.gdejestao[self.cacastack[-1]][-1][1]+=1
                            self.gdejestao[self.cacastack[-1]][-1][0]=0
                            print 468
                            #self.x-=self.gdejestao[self.cacastack[-1]][-1][2] 
                            self.x-=self.removefromhs()
                            self.gdejestao[self.cacastack[-1]][-1][2]=0
                        else:
                            #stavi da je dosao do kraja pravila u gdejestao jer ako je == samo ce da predje na sledece pravilo a ne niz pravila
                            print "dsfsdfsdfsd"
                            print grammar[self.cacastack[-1]][self.gdejestao[self.cacastack[-1]][-1][1]]
                            self.gdejestao[self.cacastack[-1]][-1][0]=len(grammar[self.cacastack[-1]][self.gdejestao[self.cacastack[-1]][-1][1]])    
                        
                        return self.parse(tokenList)

                else:
                    print "cetvrto"
                    return False
            #ako nije list/terminal nadji listu sa tim key-em u dictionary-u i dodaj ga na caca stack
            else:
                #gdejestao[cacastack[-1]][0]=index+1 #nije tu stao, jer index uvek krece od nule 
                self.gdejestao[self.cacastack[-1]][-1][0]+=1
                self.cacastack.append(pravilo)
                self.addnewtohs(pravilo)


                if pravilo not in self.gdejestao:
                    self.gdejestao[pravilo]=[]
                self.gdejestao[pravilo].append([0,0,0])
                print "printaj  sta dodaje " , pravilo 
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

p = ParseText()
print p.parse(tokenList)
print p.gdejestao
p.gdejestao = mergeall(izbaceni, p.gdejestao)
print p.gdejestao
# print nodes['number']
# print globals()[nodes['number']]
# #createnode("number", "probica")
# ast =  AST(tokenList,mergeall(izbaceni, p.gdejestao))
# ast.createtree("expr")
# print ast.stack2
# print ast.stack2[0].dooperation(),"printaj listu"
# # print ast.stack2[0].childrens[0].childrens[1].dooperation()
# #napravi tree walker metodu , tj interpretera koja ce da obidje celo stablo pozivajuci dooperation




# jsonstring='{"dit1":{"dit2":{"ime":"sale" , "titula" :[{"car":"gospodar","lastname":"univer"},{"car":"eee","lastname":"sveta"}]}}}'
# jsonstring1='{"sale":"car"}'
# print getjsonobject(["sale"], json.loads(jsonstring1)),"fdsdsfsdfsdfdsfsd"

# #jsonstring = '{"employees": [{ "firstName":"John" , "lastName":"Doe" }, { "firstName":"Anna" , "lastName":"Smith" },]}'
# conditions = [(["car"], operator.le ,"ee")]
# a = getjsonobject(["dit1","dit2","titula"], json.loads(jsonstring),conditions)

# print a,"bravo"
#print getjsonobject(["dit1","dit2","titula"], json.loads(jsonstring), conditions) , "printaj"