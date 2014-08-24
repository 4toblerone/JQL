import unittest
import os
import sys
 
parpath = os.path.join(os.path.dirname(sys.argv[0]), os.pardir)
sys.path.insert(0, os.path.abspath(parpath))

from EngineRoom import ParseText, AST
from lex import LexToken

class EngineRoomTC(unittest.TestCase):
	"""Tests for EngineRoom"""

	def setUp(self):
		print "setting up mock grammar and parser"

		testName = self.shortDescription()

		def createTokenList(tokTypes):
			tokens = []
			for tt in tokTypes:
				token = LexToken()
				token.type = tt
				token.value = "test" 
				token.lineno = 0 
				token.lexpos = 0
				tokens.append(token)
			return tokens
			#return [LexToken().type = tt for tt in tokTypes]

		self.grammar =  {"baseexpr" : [["andmathop"]],
						  "andmathop" : [["mathop", "and","andmathop"],["mathop"]],
						  "mathop": [["number","operator","mathop"],["number"]],
						  "operator":[["plus"],["minus"]]}

		typesOne = ["number", "minus", "number", "and","number","plus","number"]
		self.tokenListOne = createTokenList(typesOne)
		
		if testName == "parse test":
			typesTwo = ["number","plus","number"]
			typesThree = ["number","minus","number","and"]
			self.tokenListTwo = createTokenList(typesTwo)
			self.tokenListThree = createTokenList(typesThree)
		
		self.parser =  ParseText(self.grammar, "baseexpr")
		self.ast_builder =  AST(tokenlist, trace, start_node)

	def tearDown(self):
		print "i m done"

	def test_parse(self):
		"parse test"
		#parse func is expecting list of tokens, not strings
		self.assertTrue(self.parser.parse(self.tokenListOne))
		self.assertTrue(self.parser.parse(self.tokenListTwo))
		self.assertFalse(self.parser.parse(self.tokenListThree))

	def test_build_ast(self):
		"build AST(SDT)"

		pass

if __name__ == '__main__':
	unittest.main()