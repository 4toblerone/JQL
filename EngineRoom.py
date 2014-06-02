from Lexer import Lexer
from collections import deque, Iterable
import operator
import json


jsonstring = '{"sale":{"kolikijecar":"veliki" , "items" : [{"id" : "prvi" , "ime" : "Sale"},{"id":"drugi","ime" : "Car"}]}}'
json_loaded = json.loads(jsonstring)


class Node(object):
    """docstring for Node"""

    def __init__(self):
        self.childrens = []

    def add(self, child):
        self.childrens.append(child)

    def dooperation(self):
        """do operation on childrens, eval"""
        pass

    def __str__(self):
        print "<" + self.__class__.__name__ + ">"
        if len(self.childrens) == 0:
            return "Nema vise dece ova grana"
        for child in self.childrens:
            print child.__str__()
        return "to"


class LeafNode(Node):
    def __init__(self, token):
        super(LeafNode, self).__init__()
        self.token = token

    def dooperation(self):
        return self.token.value


class BaseExprNode(Node):
    def dooperation(self):
        print "BaseExpr"
        return self.childrens[0].dooperation()


class StrongExprNode(Node):
    def dooperation(self):
        print "StrongExpr"
        return self.childrens[0].dooperation()


class ExprNode(Node):
    def dooperation(self):
        print "Expr "
        return self.childrens[0].dooperation()


class QueryNode(Node):
    def dooperation(self):
        return self.childrens[0].dooperation()


class RemoveExprNode(Node):
    #TODO at end of dooperation replace original json file with one from removeexpr
    #TODO figure out what should you return at and of it, cuz' node above requires something
    def dooperation(self, jsonstring=json_loaded):
        print "Remove expression"
        path_to_object = self.childrens[0].dooperation()
        what_to_delete = self.childrens[1].dooperation()
        print delete_from_json(path_to_object, jsonstring, what_to_delete[0], what_to_delete[1])


class AddExprNode(Node):
    #TODO at end of dooperation replace original json file with one from removeexpr
    def dooperation(self, jsonstring=json_loaded):
        #get object or objects to which you have to add new json object
        path_to_objects = self.childrens[0].dooperation()[0]
        conditions = self.childrens[0].dooperation()[1]
        objects = getjsonobject(path_to_objects, jsonstring, conditions)
        to_add = self.childrens[1].dooperation()
        #transform to_add from string to json
        #check for json input validity
        #input can be new dict , adding to list {"key":"value}
        #or it can be simple addition to existing dict as "key":"value"
        try:
            to_add_json = json.loads(to_add)
        except ValueError:
            raise ValueError('Couldn\'t transform input string into json')
        if type(objects) is list and conditions is None:
            objects.append(to_add_json)
        else:
            for obj in objects:
                for key in to_add_json.keys():
                    obj[key] = to_add_json[key]
        return jsonstring


class UpdateExprNode(Node):
    def dooperation(self, jsonstring=json_loaded):
        #TODO see if it's ok to transforem getjsonobject to generator
        print "updateexpr"
        path_to_objects = self.childrens[0].dooperation()[0]
        conditions = self.childrens[0].dooperation()[1]
        objects = getjsonobject(path_to_objects, jsonstring, conditions)  #this ain't gonna work cuz json is not gonna change, due to immutability of strings
        objects = jsonstring["sale"]["items"]
        to_update_with = self.childrens[1].dooperation()
        for index , obj in enumerate(objects):
            objects[index] = to_update_with

        return jsonstring


class GetExprNode(Node):
    def dooperation(self, jsonstring=json_loaded):
        print "getexpr"
        path_to_object = self.childrens[0].dooperation()
        from_object = getjsonobject(path_to_object, jsonstring)
        print from_object, "from_object"
        #tuple , object we are looking for and conditions if there are any
        what_to_return = self.childrens[1].dooperation()
        return getjsonobject(what_to_return[0], from_object, what_to_return[1])


class WutNode(Node):
    def dooperation(self):
        """Should return path to the request object and 
            optional list of conditions"""
        print "wut node do"
        path_to_object = self.childrens[0].dooperation()
        print path_to_object, "putanja"
        try:
            conditions = flattenlistoftuples(self.childrens[1].dooperation())
        except IndexError:
            conditions = None
        return (path_to_object, conditions)


class ObjectNode(Node):
    def dooperation(self):
        """Returns 'path' to the object as a list of keys"""
        lista = []
        for child in self.childrens:
            lista.append(child.dooperation())
        return list(flatten(lista))


class ConditionNode(Node):
    def dooperation(self):
        listl = []
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


class VariableNode(Node):
    def dooperation(self):
        return self.childrens[0].dooperation()


class ValueNode(Node):
    def dooperation(self):
        return self.childrens[0].dooperation()


class JsonStringNode(LeafNode):
    pass


class MathExprNode(Node):
    pass


class StringExprNode(Node):
    pass


class ComparisonOpNode(Node):
    def dooperation(self):
        return self.childrens[0].dooperation()


class EqualNode(LeafNode):
    def dooperation(self):
        #find way to have assignment function
        #or maybe i don't even need it
        return "gonna be"


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
        if isinstance(element, Iterable) and not isinstance(element, basestring):
            for sub in flatten(element):
                yield sub
        else:
            yield element


def flattenlistoftuples(listoftuples):
    for element in listoftuples:
        if isinstance(element, Iterable) and not isinstance(element, basestring) \
                and not isinstance(element, tuple):

            for sub in flatten(element):
                yield sub
        else:
            yield element


def getjsonobject(paramlist, loaded_json_string, conditions=None, func=None):
    """Returns json object, where paramlist is 'path' to it. 
        If path to it is not valid a.k.a object doesn't exists
        it will return None"""
    #TODO refactor this method , so it will use func(which can be append or del) instead append
    #TODO refactor it so it will become generator and thus make result redundant
    jsonobject = reduce(dict.get, paramlist, loaded_json_string)
    if conditions is not None:
        result = []
        for jo in jsonobject:
            evaluated_conditions = [condition[1](getjsonobject(condition[0], jo), condition[2]) \
                                    for condition in conditions]
            if all(evaluated_conditions) and evaluated_conditions:
                print jo, "ovde se desava neka magija"
                result.append(jo)
        return result
    else:
        return jsonobject


def delete_from_json(path_to_object, json_object, what_to_delete, conditions=None):
    """

    :rtype : dict
    """
    jsonobject = reduce(dict.get, path_to_object + what_to_delete, json_object)
    if conditions is not None:
        to_delete = []
        for index, jo in enumerate(jsonobject):
            evaluated_conditions = [condition[1](getjsonobject(condition[0], jo), condition[2])
                                    for condition in conditions]
            if all(evaluated_conditions) and evaluated_conditions:
                print jo, "ovo se brise"
                #del jo #throws RuntimeError: dictionary changed size during iteration
                to_delete.append(index)
        for todel in to_delete:
            del jsonobject[todel]
        return json_object
    else:
        del jsonobject
        return json_object


def createnode(class_name, *args):
    node_class = globals()[class_name]
    instance = node_class(*args)
    return instance


def createleaf(rule, tokenvalue):
    leafnode = createnode(nodes[rule], tokenvalue)
    return leafnode


nodes = {"baseexpr": "BaseExprNode",
         "strongexpr": "StrongExprNode",
         "expr": "ExprNode",
         "queryexpr": "QueryNode",
         "removeexpr": "RemoveExprNode",
         "addexpr": "AddExprNode",
         "updateexpr": "UpdateExprNode",
         "getexpr": "GetExprNode",
         "wut": "WutNode",
         "object": "ObjectNode",
         "condition": "ConditionNode",
         "basiccondition": "BasicConditionNode",
         "value": "ValueNode",
         "jsonstring": "JsonStringNode",
         "mathexpr": "MathExprNode",
         "stringexpr": "StringExprNode",
         "variable": "VariableNode",

         "comparisonop": "ComparisonOpNode",
         "less": "LessNode",
         "greater": "GreaterNode",
         "lessorequal": "LessOrEqualNode",
         "equalorgreater": "EqualOrGreaterNode",
         "twoequal": "TwoEqualNode",
         "equal": "EqualNode",

         "word": "WordNode",
         "number": "NumberNode",

         "operator": "OperatorNode",
         "plus": "PlusNode",
         "minus": "MinusNode",
         "times": "TimesNode",
         "divide": "DivideNode"
}


#there is a need for "cushion" node
grammar = {"baseexpr": [["strongexpr"]],
           "strongexpr": [["variable", "equal", "lcurlyb", "expr", "rcurlyb"], ["expr"]],  #fix this shit
           "expr": [["queryexpr"], ["mathexpr"], ["stringexpr"]],
           "variable": [["var", "word"]],
           "queryexpr": [["removeexpr"], ["addexpr"], ["updateexpr"], ["getexpr"]],
           "removeexpr": [["from", "object", "remove", "wut"]],
           "getexpr": [["from", "object", "get", "wut"]],
           "addexpr": [["to", "wut", "add", "jsonstring_start", "jsonstring", "jsonstring_end"]],
           "updateexpr": [["update", "wut", "to", "jsonstring_start", "jsonstring", "jsonstring_end"]],
           "object": [["word", "arrow", "object"], ["word"]],
           "condition": [["basiccondition", "and", "condition"], ["basiccondition"]],
           "basiccondition": [["object", "comparisonop", "value"]],
           "value": [["word"], ["number"]],
           "wut": [["object", "where", "condition"], ["object"]],
           "comparisonop": [["less"], ["greater"], ["twoequal"], ["lessorequal"], ["greaterorequal"]],
           "mathexpr": [["number", "operator", "mathexpr"], ["number"]],
           "operator": [["plus"], ["minus"], ["times"], ["divide"]],
           "stringexpr": [[]],
}

# grammar={"expr":[["andmathopop"]],
#            "andmathopop" :[["andmathop","word", "andmathop"]],
#            "andmathop":[["mathop","and","andmathop"],["mathop"]],
#            "mathop":[["number","operator", "mathop"],["number"]],
#            "operator": [["plus"]] }

#tokenList = Lexer().breakDownStringToTokens(" 7 + 7 and 7+ 7 and 7 + 7 edeste 7+7 ")
#tokenList = Lexer().breakDownStringToTokens("from nekibojekat->nekarec get nekidrugiobjeat->nestonesto where nesto == nesto and nesto == nesto ")
#tokenList = Lexer().breakDownStringToTokens("to sale->items where id == prvi add '{\"nekistring\" : \"drugistring\"}'")
tokenList = Lexer().breakDownStringToTokens("update sale->items where id == prvi to '{\"hejovoje\":\"nestonovo\"}'")
print tokenList
#self.izbaceni={}

print tokenList


def resetfileds(fn):
    def wrapper(self, arg):
        result = fn(self, arg)
        self.__init__()
        return result

    return wrapper


def tryit(func):
    def wrapit(*args):
        try:
            return func(*args)
        except:
            "Some error happend and there is 99%% chance it is syntax related"

    return wrapit


class ParseText:
    def __init__(self):
        self.cacastack = ['baseexpr']
        self.helperstack = [['baseexpr', 0]]
        self.gdejestao = {'baseexpr': [[0, 0,
                                        0]]}  #3. int sluzi za broja tokena tj da bi se znalo koliko unazad da se vrati u slucaju da ne naidje na odgvarajuce pravilo
        #2. int oznacava odabrano prailo
        #sta je 1. predjeno pravilo u ovom slucaju token , tj pomeraj u pravilo listi
        self.gdejebio = [createnode(nodes["baseexpr"])]
        self.x = 0
        self.izbaceni = {}

    def addnewtohs(self, pravilo):
        self.helperstack.append([pravilo, 0])

    def uphelperstack(self):
        for upstairrule in self.helperstack:
            upstairrule[1] += 1

    def removefromhs(self):
        tocut = self.helperstack[-1][1]
        del self.helperstack[-1]
        for upstairrule in self.helperstack:
            upstairrule[1] -= tocut
        return tocut

    def downsizehs(self):
        tocut = self.helperstack[-1][1]
        for node in self.helperstack:
            node[1] -= self.helperstack[-1][1]
        return tocut


    def deletelasths(self):
        del self.helperstack[-1]

    def move_forward(self):
        self.gdejestao[self.cacastack[-1]][-1][1] += 1
        self.gdejestao[self.cacastack[-1]][-1][0] = 0
        self.gdejestao[self.cacastack[-1]][-1][2] = 0

    #@resetfileds
    @tryit
    def parse(self, tokenList):
        #TODO get rid of the need for cushion node

        listapravila = grammar[self.cacastack[-1]][self.gdejestao[self.cacastack[-1]][-1][1]]
        #ovde provera da li je dosao i do kraja pravila
        if len(listapravila[self.gdejestao[self.cacastack[-1]][-1][0]:]) == 0:
            if len(self.cacastack) > 1:
                self.cacastack.pop()
                return self.parse(tokenList)
            elif len(tokenList) > self.x:
                print self.cacastack, self.gdejestao, self.gdejebio
                return False

        #da li je presao sve tokene u listi, ako jeste
        if self.x == len(tokenList):
            if len(self.cacastack) == 1:
                self.gdejestao = mergeall(self.izbaceni, self.gdejestao)
                print "stae ovo", self.gdejestao
                return True
            else:
                #proveri da li ima jos listi pravila, ako ima prebaci na sledecu listu i smanji self.x
                if self.gdejestao[self.cacastack[-1]][-1][1] < len(grammar[self.cacastack[-1]]):
                    self.gdejestao = mergeall(self.izbaceni, self.gdejestao)
                    self.izbaceni.clear()
                    while self.helperstack[-1][0] is not self.cacastack[-1]:
                        #mora se smanjiti i na self.izbacenima ukupan broj...
                        del self.gdejestao[self.helperstack[-1][0]][-1]

                        if self.helperstack[-1][0] in self.izbaceni:
                            self.izbaceni[self.helperstack[-1][0]][0] -= 1
                        self.x -= self.removefromhs()

                    self.move_forward()
                    return self.parse(tokenList)

                if self.gdejestao[self.cacastack[-1]][-1][0] == len(
                        grammar[self.cacastack[-1]][self.gdejestao[self.cacastack[-1]][-1][1]]) - 1:
                    if len(self.cacastack) > 1:
                        #ne moze da se vrati skroz do kraja , tj moze samo do expr
                        if len(self.gdejestao[self.cacastack[-1]]) > 1:
                            poslednji = self.gdejestao[self.cacastack[-1]].pop()
                            self.izbaceni[self.cacastack[-1]].append((self.izbaceni[self.cacastack[-1]][0], poslednji))
                            #del self.gdejestao[self.cacastack[-1]][-1]
                        self.cacastack.pop()
                        return self.parse(tokenList)
                return False

        # ako je na pocetku odredjene grupe pravila (jedno pravilo moze da ima vise grupa pravila)
        # i ako je duzina te grupe pravila veca oda broja preostalih tokena koje treba preci
        if self.gdejestao[self.cacastack[-1]][-1][0] == 0 and len(listapravila) > len(tokenList) - self.x:
            #ako je broj grupa pravila koja proizilazi iz poslednjeg na stack-u veca od broja predjenih grupa
            #tj ako nije presao sve grupe pravila
            if len(grammar[self.cacastack[-1]]) - 1 > self.gdejestao[self.cacastack[-1]][-1][1]:
                #prebaci na sledecu grupu pravila
                self.move_forward()
                #ovde izbrisi sa gdejebio poslednji i obrisi decu njegovog caleta
                self.x -= self.downsizehs()
                return self.parse(tokenList)
            elif len(self.cacastack) > 1:  #ukoliko cacastack predzadnji nije na poslednjem pravilu

                #print "drugo","x je ",self.x, self.cacastack , self.gdejebio, self.gdejestao
                #print "e ", self.helperstack, listapravila
                #ukoliko je presao sve grupe pravila , obrisi sve sa helperstacka do c
                del self.cacastack[-1]
                while self.helperstack[-1][0] is not self.cacastack[-1]:
                    if len(self.izbaceni[self.helperstack[-1][0]]) > 1 and self.izbaceni[self.helperstack[-1][0]][-1][
                        0] == self.izbaceni[self.helperstack[-1][0]][0]:
                        del self.izbaceni[self.helperstack[-1][0]][-1]
                    else:
                        del self.gdejestao[self.helperstack[-1][0]][-1]
                    self.izbaceni[self.helperstack[-1][0]][0] -= 1
                    self.x -= self.removefromhs()
                self.x -= self.downsizehs()
                self.move_forward()
                return self.parse(tokenList)
            else:
                return False

        for index, pravilo in enumerate(listapravila[self.gdejestao[self.cacastack[-1]][-1][0]:]):
            #proveri da li je list/terminal i da li je jednak tipu tokena
            print self.x, pravilo
            self.gdejebio.append(pravilo)
            if pravilo not in grammar.keys():  #and pravilo==tokenList[x].type:
                #za svaki sledeci pomeri pokazivac
                #mora posle ovo jer se na 81 liniji gleda nova verzija a ne treba
                self.gdejestao[self.cacastack[-1]][-1][0] += 1
                #znaci da je list, proveri da li je to taj tip tokena (vodi racuna na velika/mala slova)
                if self.x <= len(tokenList) - 1 and pravilo == tokenList[self.x].type.lower():
                    #napravi Node objekat za terminal ovde i dodaj ga kao dete poslednjem sa caca stack-a
                    self.x += 1
                    print "povecao je x za jedan ", self.x, pravilo
                    self.gdejestao[self.cacastack[-1]][-1][2] += 1
                    self.uphelperstack()
                    #da li je presao jednu listu pravila , ako jeste i ako na cacastack-u ima vise od jednog
                    if self.gdejestao[self.cacastack[-1]][-1][0] == len(listapravila):
                        if len(self.cacastack) > 1:  #reason for cushion!
                            #ne moze da se vrati skroz do kraja , tj moze samo do expr
                            if len(self.gdejestao[self.cacastack[-1]]) > 1:
                                poslednji = self.gdejestao[self.cacastack[-1]].pop()
                                self.izbaceni[self.cacastack[-1]].append(
                                    (self.izbaceni[self.cacastack[-1]][0], poslednji))
                            self.cacastack.pop()
                            #self.deletelasths()
                            return self.parse(tokenList)
                        else:
                            print "trece"
                            return False
                            #print "436"

                elif self.x <= len(tokenList) - 1 and pravilo != tokenList[self.x].type.lower():
                    if len(grammar[self.cacastack[-1]]) - 1 > self.gdejestao[self.cacastack[-1]][-1][1]:
                        print "da li je i ovde usao a trebalo bi", self.x
                        self.gdejestao[self.cacastack[-1]][-1][1] += 1
                        #resetuj gde je stao tj x == 0
                        self.gdejestao[self.cacastack[-1]][-1][0] = 0
                        #smanjujem x za sve pronadjene u tom pravilu
                        """ovde x treba umanjiti za poslednji sa helperstack-a , popovati helperstack-a da bi se
                        pravi 'poslednji' uzimao u obzir"""
                        #dodaj provere za izbacene ako nema ni jednog u njima i smanjuj kako ih izbacujes
                        while self.helperstack[-1][0] is not self.cacastack[-1]:
                            if len(self.izbaceni[self.helperstack[-1][0]]) > 1 and \
                                            self.izbaceni[self.helperstack[-1][0]][-1][0] == \
                                            self.izbaceni[self.helperstack[-1][0]][0]:
                                del self.izbaceni[self.helperstack[-1][0]][-1]
                            else:
                                del self.gdejestao[self.helperstack[-1][0]][-1]
                            self.izbaceni[self.helperstack[-1][0]][0] -= 1
                            self.x -= self.removefromhs()  #ne odradi downsize do kraja tj do andmathopa # ili remove pa na kraju downsize?
                            #i kako brises sa helperstacka tako brisi poslednjeg sa gdejestao+self.izbaceni stacka
                        self.x -= self.downsizehs()
                        self.gdejestao[self.cacastack[-1]][-1][2] = 0
                        print self.x
                        #del self.gdejestao[self.cacastack[-1]][-1]   #baca out ouf range na 87 i ovde je problem
                        #i ovde smanji za jedan u self.izbacenima
                        #self.izbaceni[self.cacastack[-1]][0]-=1
                        return self.parse(tokenList)
                    elif len(self.cacastack) > 1:

                        while self.helperstack[-1][0] is not self.cacastack[-1]:
                            if len(self.izbaceni[self.helperstack[-1][0]]) > 1 and \
                                            self.izbaceni[self.helperstack[-1][0]][-1][0] == \
                                            self.izbaceni[self.helperstack[-1][0]][0]:
                                del self.izbaceni[self.helperstack[-1][0]][-1]
                            else:
                                del self.gdejestao[self.helperstack[-1][0]][-1]
                            self.izbaceni[self.helperstack[-1][0]][0] -= 1
                            self.x -= self.removefromhs()
                        self.x -= self.downsizehs()  #ovde mora da poizbacuje sve do cacastacka
                        #zameni mesta del sa self.cacastack-a i 467 i mosdef obrisati poslednji sa gde je stao stacka-a
                        self.gdejestao[self.cacastack[-1]][-1][2] = 0  #da li obrisati ovo?
                        # i ovde takodje smanji izbacene
                        del self.gdejestao[self.cacastack[-1]][-1]
                        self.izbaceni[self.cacastack[-1]][0] -= 1
                        del self.cacastack[-1]
                        #ukoliko je nije dosao do poslednje liste pravila, tj. ukoliko imas jos listi pravila
                        if len(grammar[self.cacastack[-1]]) - 1 > self.gdejestao[self.cacastack[-1]][-1][1]:
                            self.move_forward()
                            #downsize sve na helperstacku za onoliko koliko ima na poslednjem, s tim da ne treba obrisati poslednji
                            #self.x-=self.removefromhs()
                            self.x -= self.downsizehs()
                            self.deletelasths()
                        else:
                            #stavi da je dosao do kraja pravila u gdejestao jer ako je == samo ce da predje na sledece pravilo a ne niz pravila
                            print grammar[self.cacastack[-1]][self.gdejestao[self.cacastack[-1]][-1][1]]
                            self.gdejestao[self.cacastack[-1]][-1][0] = len(
                                grammar[self.cacastack[-1]][self.gdejestao[self.cacastack[-1]][-1][1]])
                        return self.parse(tokenList)

                else:
                    return False
            #ako nije list/terminal nadji listu sa tim key-em u dictionary-u i dodaj ga na caca stack
            else:
                #gdejestao[cacastack[-1]][0]=index+1 #nije tu stao, jer index uvek krece od nule
                self.gdejestao[self.cacastack[-1]][-1][0] += 1
                self.cacastack.append(pravilo)
                self.addnewtohs(pravilo)

                if pravilo not in self.gdejestao:
                    self.gdejestao[pravilo] = []
                self.gdejestao[pravilo].append([0, 0, 0])
                self.izbaceni[pravilo] = self.izbaceni.get(pravilo, [-1])
                self.izbaceni[pravilo][0] = len(self.gdejestao[pravilo]) + len(self.izbaceni[pravilo]) - 2
                return self.parse(tokenList)


def mergeall(izbaceni, gdejestao):
    def merge(popeditems, key):

        lista = []
        i = 0
        gdejestaodeo = deque(gdejestao[key])
        length = len(popeditems) + len(gdejestaodeo)  #3
        while i < length:  #ne moze plus jer ako nista nema toliko u vecoj listi
            if popeditems and i == popeditems[0][0]:
                print i
                lista.append(popeditems[0][1])
                del popeditems[0]
            elif len(gdejestaodeo) > 0:
                lista.append(gdejestaodeo[0])
                del gdejestaodeo[0]
            #dodataks
            else:
                lista.append(popeditems[0][1])
                del popeditems[0]
            i += 1
        return lista

    for key, value in izbaceni.iteritems():
        if len(value) > 1:
            gdejestao[key] = merge(value[1:], key)
    return gdejestao


#print p.gdejestao

#ovo treba u zasebnoj klasi, cini mi se da je bolje nego closure
#promeni imena atributa, daj nesto smisleno, prvi i stack nisu bas
#p.gdejestao i trace , pogledaj razlike tj da li ih ima
class AST(object):
    def __init__(self, tokenlist, trace):
        self.stack = [BaseExprNode()]
        self.stack2 = []
        self.dek = deque(tokenlist)
        self.trace = trace

    def createtree(self, key):
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
                    print "dek", self.dek
                    self.stack[-1].add(createleaf(pravilo, self.dek.popleft()))
                    if index == len(grammar[key][rulenum]) - 1 and len(self.stack) > 1:
                        self.stack.pop()
                        del self.trace[key][0]
                else:
                    node = createnode(nodes[pravilo])
                    self.stack[-1].add(node)
                    if index == len(grammar[key][rulenum]) - 1:
                        if len(self.stack) == 1:
                            self.stack2.append(self.stack.pop())
                        else:
                            self.stack.pop()
                        del self.trace[key][0]

                    self.stack.append(node)
                    self.createtree(pravilo)
            else:
                self.dek.popleft()


class SymboleTable(object):
    def __init__(self):
        self.table = dict()


p = ParseText()
print p.parse(tokenList)
print p.gdejestao
print "**************"

ast = AST(tokenList, p.gdejestao)
ast.createtree("baseexpr")
print ast.stack2[0]
print ast.stack2[0].dooperation(), "e ovo vraca"

obj = getjsonobject(["sale", "kolikijecar"], json_loaded)
print obj
obj = "josveci"
print obj, json_loaded
#for each in ast.stack2[0].dooperation():
#print each["ime"]000000----------0000000000000000000000000000000000000000000
#print json.loads(jsonstring1)
# print ast.stack2[0].dooperation(),"printaj listu"
# # print ast.stack2[0].childrens[0].childrens[1].dooperation()
# #napravi tree walker metodu , tj interpretera koja ce da obidje celo stablo pozivajuci dooperation




# jsonstring='{"dit1":{"dit2":{"ime":"sale" , "titula" :[{"car":"gospodar","lastname":"univer"},{"car":"eee","lastname":"sveta
# print getjsonobject(["sale"], json.loads(jsonstring1)),"fdsdsfsdfsdfdsfsd"

# #jsonstring = '{"employees": [{ "firstName":"John" , "lastName":"Doe" }, { "firstName":"Anna" , "lastName":"Smith" },]}'
# conditions = [(["car"], operator.le ,"ee")]
# a = getjsonobject(["dit1","dit2","titula"], json.loads(jsonstring),conditions)

# print a,"bravo"
#print getjsonobject(["dit1","dit2","titula"], json.loads(jsonstring), conditions) , "printaj"