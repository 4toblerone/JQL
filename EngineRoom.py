import lex
import TokenDef
from collections import deque  



def breakDownStringToTokens(text, module = TokenDef):
        lexer = lex.lex(module)
        lexer.input(text)
        tokenList = []
        while True:
            tok = lexer.token()
            if not tok:
                break
            tokenList.append(tok)
        return tokenList


# def createnode(class_name, *args):
#     """Creates SDT('Syntax Directed Translation') node
#        NOTE : It doesn't work as expected cuz globals 
#        are related to the module they are called in!
#        So this function can only be used in this module
#        aka module it is defined in!!!
#     """
#     node_class = globals()[class_name]
#     instance = node_class(*args)
#     return instance


# def createleaf(rule, tokenvalue):
#     """Creates SDT('Syntax Directed Translation') leaf node"""
#     leafnode = createnode(nodes[rule], tokenvalue)
#     return leafnode


def resetfileds(fn):
    """Decorator for reseting object's fields"""

    def wrapper(self, *args):
        result = fn(self, *args)
        self.__init__()
        return result

    return wrapper


# TODO do proper exception on this
def tryit(func):
    """Decorator which encloses every other exception 
       and raises SyntaxException"""
    def wrapit(*args):
        try:
            func(*args)
        except Exception as e:
            raise SyntaxException("Code is not syntactically correct!")
        finally:
            print "finali"
    return wrapit


class SyntaxException(Exception):
    """"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class ParseText:

    def __init__(self, grammar, start_nonterminal):
        """
        Keywords arguments:
        grammar -- dictionary representing language grammar
        start_nonterminal -- grammar's start symbol/nonterminal 
        """
        self.grammar = grammar
        self.start_nonterminal = start_nonterminal
        #self._initialize(start_nonterminal)
    
        
    def _initialize(self):
        #self.start_nonterminal = start_nonterminal
        self.cacastack = [self.start_nonterminal]
        self.helperstack = [[self.start_nonterminal, 0]]
        self.gdejestao = {self.start_nonterminal: [[0, 0, 0]]}
        # 3. int sluzi za broja tokena tj da bi se znalo koliko unazad
        # da se vrati u slucaju da ne naidje na odgvarajuce pravilo
        # 2. int oznacava odabrano prailo
        # sta je 1. predjeno pravilo u ovom slucaju token , tj pomeraj u pravilo listi
        self.x = 0
        self.izbaceni = {}

    def addnewtohs(self, rule):
        self.helperstack.append([rule, 0])

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

    def parse(self, tokenList):
        self._initialize()
        try:
            print "parsiramo"
            print self._validate(tokenList)
            return self._validate(tokenList)
        except Exception as e:
            #raise SyntaxException("Not madafakin valid!")
            print "deste"
            return False
        finally:
            print "doin dis shiat"
            #this ain't gonna work cuz we need self.gdejestao
            #to build , so this should be before try/except
            #self._initialize(self.start_nonterminal)

    # TODO get rid of the need for cushion node
    # what if token type defined doesn't exists in grammar dict?
    # add position 'x' of the token i token list so user can
    # have information where exception occured
    # What about context menager? Ain't gonna work
    #@resetfileds doesn't work cuz of recursion
    #@tryit , replaced by putting it in proper parse method
    def _validate(self, tokenList):
        """Checks if given stream of tokens can be 
        generated from a given grammar. 

        Keywords arguments:
        tokenList -- list of tokens
        """
        listapravila = self.grammar[self.cacastack[-1]][
            self.gdejestao[self.cacastack[-1]][-1][1]]
        # ovde provera da li je dosao i do kraja pravila
        if len(listapravila[self.gdejestao[self.cacastack[-1]][-1][0]:]) == 0:
            if len(self.cacastack) > 1:
                self.cacastack.pop()
                return self._validate(tokenList)
            elif len(tokenList) > self.x:
                return False
        # da li je presao sve tokene u listi, ako jeste
        if self.x == len(tokenList):
            if len(self.cacastack) == 1:
                self.gdejestao = mergeall(self.izbaceni, self.gdejestao)
                return True
            else:
                # proveri da li ima jos listi pravila, ako ima prebaci na
                # sledecu listu i smanji self.x
                if self.gdejestao[self.cacastack[-1]][-1][1] < len(self.grammar[self.cacastack[-1]]):
                    self.gdejestao = mergeall(self.izbaceni, self.gdejestao)
                    self.izbaceni.clear()
                    while self.helperstack[-1][0] is not self.cacastack[-1]:
                        # mora se smanjiti i na self.izbacenima ukupan broj...
                        del self.gdejestao[self.helperstack[-1][0]][-1]
                        if self.helperstack[-1][0] in self.izbaceni:
                            self.izbaceni[self.helperstack[-1][0]][0] -= 1
                        self.x -= self.removefromhs()
                    self.move_forward()
                    return self._validate(tokenList)

                if self.gdejestao[self.cacastack[-1]][-1][0] == len(
                        self.grammar[self.cacastack[-1]][self.gdejestao[self.cacastack[-1]][-1][1]]) - 1:
                    if len(self.cacastack) > 1:
                        # ne moze da se vrati skroz do kraja , tj moze samo do
                        # expr
                        if len(self.gdejestao[self.cacastack[-1]]) > 1:
                            poslednji = self.gdejestao[
                                self.cacastack[-1]].pop()
                            self.izbaceni[self.cacastack[-1]].append(
                                (self.izbaceni[self.cacastack[-1]][0], poslednji))
                            #del self.gdejestao[self.cacastack[-1]][-1]
                        self.cacastack.pop()
                        return self._validate(tokenList)
                return False
        # ako je na pocetku odredjene grupe pravila (jedno pravilo moze da ima vise grupa pravila)
        # i ako je duzina te grupe pravila veca oda broja preostalih tokena
        # koje treba preci
        if self.gdejestao[self.cacastack[-1]][-1][0] == 0 and len(listapravila) > len(tokenList) - self.x:
            # ako je broj grupa pravila koja proizilazi iz poslednjeg na stack-u veca od broja predjenih grupa
            # tj ako nije presao sve grupe pravila
            if len(self.grammar[self.cacastack[-1]]) - 1 > self.gdejestao[self.cacastack[-1]][-1][1]:
                # prebaci na sledecu grupu pravila
                self.move_forward()
                # ovde izbrisi sa gdejebio poslednji i obrisi decu njegovog
                # caleta
                self.x -= self.downsizehs()
                return self._validate(tokenList)
            # ukoliko cacastack predzadnji nije na poslednjem pravilu
            elif len(self.cacastack) > 1:
                # ukoliko je presao sve grupe pravila , obrisi sve sa
                # helperstacka do c
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
                return self._validate(tokenList)
            else:
                return False
        for index, pravilo in enumerate(listapravila[self.gdejestao[self.cacastack[-1]][-1][0]:]):
            # proveri da li je list/terminal i da li je jednak tipu tokena
            if pravilo not in self.grammar.keys():
                # za svaki sledeci pomeri pokazivac
                self.gdejestao[self.cacastack[-1]][-1][0] += 1
                # znaci da je list, proveri da li je to taj tip tokena (vodi
                # racuna na velika/mala slova)
                if self.x <= len(tokenList) - 1 and pravilo == tokenList[self.x].type.lower():
                    self.x += 1
                    self.gdejestao[self.cacastack[-1]][-1][2] += 1
                    self.uphelperstack()
                    # da li je presao jednu listu pravila , ako jeste i ako na
                    # cacastack-u ima vise od jednog
                    if self.gdejestao[self.cacastack[-1]][-1][0] == len(listapravila):
                        if len(self.cacastack) > 1:  # reason for cushion!
                            # ne moze da se vrati skroz do kraja , tj moze samo
                            # do expr
                            if len(self.gdejestao[self.cacastack[-1]]) > 1:
                                poslednji = self.gdejestao[
                                    self.cacastack[-1]].pop()
                                self.izbaceni[self.cacastack[-1]].append(
                                    (self.izbaceni[self.cacastack[-1]][0], poslednji))
                            self.cacastack.pop()
                            # self.deletelasths()
                            return self._validate(tokenList)
                        else:
                            return False
                elif self.x <= len(tokenList) - 1 and pravilo != tokenList[self.x].type.lower():
                    if len(self.grammar[self.cacastack[-1]]) - 1 > self.gdejestao[self.cacastack[-1]][-1][1]:
                        # print "da li je i ovde usao a trebalo bi", self.x
                        self.gdejestao[self.cacastack[-1]][-1][1] += 1
                        # resetuj gde je stao tj x == 0
                        self.gdejestao[self.cacastack[-1]][-1][0] = 0
                        # smanjujem x za sve pronadjene u tom pravilu
                        # dodaj provere za izbacene ako nema ni jednog u njima
                        # i smanjuj kako ih izbacujes
                        while self.helperstack[-1][0] is not self.cacastack[-1]:
                            if len(self.izbaceni[self.helperstack[-1][0]]) > 1 and \
                                self.izbaceni[self.helperstack[-1][0]][-1][0] == \
                                self.izbaceni[self.helperstack[-1][0]][0]:
                                del self.izbaceni[self.helperstack[-1][0]][-1]
                            else:
                                del self.gdejestao[self.helperstack[-1][0]][-1]
                            self.izbaceni[self.helperstack[-1][0]][0] -= 1
                            # ne odradi downsize do kraja tj do andmathopa #
                            # ili remove pa na kraju downsize?
                            self.x -= self.removefromhs()
                            # i kako brises sa helperstacka tako brisi
                            # poslednjeg sa gdejestao+self.izbaceni stacka
                        self.x -= self.downsizehs()
                        self.gdejestao[self.cacastack[-1]][-1][2] = 0
                        # del self.gdejestao[self.cacastack[-1]][-1]   #baca out ouf range na 87 i ovde je problem
                        # i ovde smanji za jedan u self.izbacenima
                        return self._validate(tokenList)
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
                        # ovde mora da poizbacuje sve do cacastacka
                        self.x -= self.downsizehs()
                        # zameni mesta del sa self.cacastack-a i 467 i mosdef
                        # obrisati poslednji sa gde je stao stacka-a
                        # da li obrisati ovo?
                        self.gdejestao[self.cacastack[-1]][-1][2] = 0
                        # i ovde takodje smanji izbacene
                        del self.gdejestao[self.cacastack[-1]][-1]
                        self.izbaceni[self.cacastack[-1]][0] -= 1
                        del self.cacastack[-1]
                        # ukoliko je nije dosao do poslednje liste pravila, tj.
                        # ukoliko imas jos listi pravila
                        if len(self.grammar[self.cacastack[-1]]) - 1 > self.gdejestao[self.cacastack[-1]][-1][1]:
                            self.move_forward()
                            # downsize sve na helperstacku za onoliko koliko ima na poslednjem,
                            # s tim da ne treba obrisati poslednji
                            self.x -= self.downsizehs()
                            self.deletelasths()
                        else:
                            # stavi da je dosao do kraja pravila u gdejestao jer ako je == samo ce da
                            # predje na sledece pravilo a ne niz pravila
                            # grammar[self.cacastack[-1]][self.gdejestao[self.cacastack[-1]][-1][1]]
                            self.gdejestao[self.cacastack[-1]][-1][0] = len(
                                self.grammar[self.cacastack[-1]][self.gdejestao[self.cacastack[-1]][-1][1]])
                        return self._validate(tokenList)
                else:
                    return False
            # ako nije list/terminal nadji listu sa tim key-em u dictionary-u i
            # dodaj ga na caca stack
            else:
                # gdejestao[cacastack[-1]][0]=index+1 #nije tu stao, jer index
                # uvek krece od nule
                self.gdejestao[self.cacastack[-1]][-1][0] += 1
                self.cacastack.append(pravilo)
                self.addnewtohs(pravilo)
                if pravilo not in self.gdejestao:
                    self.gdejestao[pravilo] = []
                self.gdejestao[pravilo].append([0, 0, 0])
                self.izbaceni[pravilo] = self.izbaceni.get(pravilo, [-1])
                self.izbaceni[pravilo][0] = len(
                    self.gdejestao[pravilo]) + len(self.izbaceni[pravilo]) - 2
                return self._validate(tokenList)


def mergeall(izbaceni, gdejestao):

    def merge(popeditems, key):

        lista = []
        i = 0
        gdejestaodeo = deque(gdejestao[key])
        length = len(popeditems) + len(gdejestaodeo)  # 3
        while i < length:
            if popeditems and i == popeditems[0][0]:
                lista.append(popeditems[0][1])
                del popeditems[0]
            elif len(gdejestaodeo) > 0:
                lista.append(gdejestaodeo[0])
                del gdejestaodeo[0]
            else:
                lista.append(popeditems[0][1])
                del popeditems[0]
            i += 1
        return lista

    for key, value in izbaceni.iteritems():
        if len(value) > 1:
            gdejestao[key] = merge(value[1:], key)
    return gdejestao


class AST(object):

    def __init__(self, tokenlist, start_node,grammar, nodes):
        """
        Keyword arguments:

        tokenList -- List of tokens
        trace -- Dictionary which represents trace parser left while
                 moving 'through' the language grammar
        start_node -- Instace of class associated with start rule
        """
        #self.stack = [BaseExprNode()]
        self.start_node = start_node
        self.tokenlist = tokenlist
        self.stack = [self.start_node]
        self.stack2 = []
        self.dek = deque(self.tokenlist)
        self.grammar = grammar
        self.nodes = nodes

    def _initialize(self):
        self.stack = [self.start_node]
        self.stack2 = []
        self.dek = deque(self.tokenlist)

    # TODO initialize before tree creation starts
    # TODO think about generators

    def createnode(self,class_ref, *args):

        return class_ref(*args)

    def createleaf(self,class_ref, token_value):

        return self.createnode(class_ref, token_value)

    def createtree(self, key, trace):
        """
        Recursively creates SDT tree using language grammar
        and trace left by parse function

        Keyword arguments:
        key -- leftside nonterminal 
        grammar -- dictionary representing language grammar
        nodes -- dictionary connecting certain (non)terminals 
        and theirs corresponding classes

        createleaf and createnode only works in this module,
        cuz' of the globals() func which returns m 
        """
        rulenum = trace[key][0][1]
        for index, rule in enumerate(self.grammar[key][rulenum]):
            if rule in self.nodes:
                if rule not in self.grammar:
                    self.stack[-1].add(self.createleaf(self.nodes[rule], self.dek.popleft()))
                    if index == len(self.grammar[key][rulenum]) - 1 and len(self.stack) > 1:
                        self.stack.pop()
                        del trace[key][0]
                else:
                    node = self.createnode(self.nodes[rule])
                    self.stack[-1].add(node)
                    if index == len(self.grammar[key][rulenum]) - 1:
                        if len(self.stack) == 1:
                            self.stack2.append(self.stack.pop())
                        else:
                            self.stack.pop()
                        del trace[key][0]
                    self.stack.append(node)
                    self.createtree(rule,trace)
            else:
                self.dek.popleft()


if __name__ == '__main__':
   print "e desi"
