import operator
import json
from collections import Iterable
from EngineRoom import AST, ParseText,createnode,createleaf
from Lexer import Lexer

jsonstring = '{"tim":{"nazivtima":"BobRock" , "igraci" : [{"id" : "prvi" , "ime" : "Sale"},{"id":"drugi","ime" : "Dzoni"}]}}'
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
        #print "BaseExpr"
        return self.childrens[0].dooperation()


class StrongExprNode(Node):
    def dooperation(self):
        #print "StrongExpr"
        return self.childrens[0].dooperation()


class ExprNode(Node):
    def dooperation(self):
        return self.childrens[0].dooperation()


class QueryNode(Node):
    def dooperation(self):
        return self.childrens[0].dooperation()


class RemoveExprNode(Node):
    #TODO at end of dooperation replace original json file with one from removeexpr
    #TODO figure out what should you return at and of it, cuz' node above requires something
    def dooperation(self, jsonstring=json_loaded):
        path_to_object = self.childrens[0].dooperation()
        what_to_delete = self.childrens[1].dooperation()
        return delete_from_json(path_to_object, jsonstring, what_to_delete[0], what_to_delete[1])


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
        #print "updateexpr"
        path_to_objects = self.childrens[0].dooperation()[0]
        conditions = self.childrens[0].dooperation()[1]
        objects = getjsonobject(path_to_objects, jsonstring,
                                conditions)  #this ain't gonna work cuz json is not gonna change, due to immutability of strings
        #objects = jsonstring["sale"]["items"]
        to_update_with = self.childrens[1].dooperation()
        for obj in objects:
            #objects[index] = to_update_with
            obj.clear()
            obj.update(json.loads(to_update_with))
        #print jsonstring
        return jsonstring


class GetExprNode(Node):
    def dooperation(self, jsonstring=json_loaded):
        #print "getexpr"
        path_to_object = self.childrens[0].dooperation()
        from_object = getjsonobject(path_to_object, jsonstring)
        #tuple , object we are looking for and conditions if there are any
        what_to_return = self.childrens[1].dooperation()
        return getjsonobject(what_to_return[0], from_object, what_to_return[1])


class WutNode(Node):
    def dooperation(self):
        """Should return path to the request object and 
            optional list of conditions"""
        #print "wut node do"
        path_to_object = self.childrens[0].dooperation()
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

class MathOpNode(Node):
    def dooperation(self):
        op_func = self.childrens[1].dooperation()
        arg_1 = self.childrens[0].dooperation()
        arg_2 = self.childrens[2].dooperation()
        return op_func(arg_1,arg_2)

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
                #print jo, "ovde se desava neka magija"
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
                #print jo, "ovo se brise"
                #del jo #throws RuntimeError: dictionary changed size during iteration
                to_delete.append(index)
        for todel in to_delete:
            del jsonobject[todel]
        return json_object
    else:
        del jsonobject
        return json_object


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

def __main__():
   print "fsd"
   print "ovo je nesto"


print "yo"
p = ParseText(grammar, "baseexpr")
tokenlist = Lexer.breakDownStringToTokens("from tim remove igraci where id == prvi")
print tokenlist, "lista tokena"
print p.parse(tokenlist)

if __name__ == '__main__':
    __main__()