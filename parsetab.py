
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftDOTleftLAMBDAleftVARDOT LAMBDA LPAREN RPAREN VARexpr : VARexpr : expr exprexpr : LAMBDA VAR DOT exprexpr : LPAREN expr RPAREN'
    
_lr_action_items = {'VAR':([0,1,2,3,4,5,7,8,9,10,],[2,2,-1,6,2,2,2,2,-4,2,]),'LAMBDA':([0,1,2,4,5,7,8,9,10,],[3,3,-1,3,3,3,3,-4,3,]),'LPAREN':([0,1,2,4,5,7,8,9,10,],[4,4,-1,4,4,4,4,-4,-3,]),'$end':([1,2,5,9,10,],[0,-1,-2,-4,-3,]),'RPAREN':([2,5,7,9,10,],[-1,-2,9,-4,-3,]),'DOT':([6,],[8,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expr':([0,1,4,5,7,8,10,],[1,5,7,5,5,10,5,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expr","S'",1,None,None,None),
  ('expr -> VAR','expr',1,'p_expr_var','apl_project.py',69),
  ('expr -> expr expr','expr',2,'p_expr_func_arg','apl_project.py',73),
  ('expr -> LAMBDA VAR DOT expr','expr',4,'p_expr_lambda_expr','apl_project.py',77),
  ('expr -> LPAREN expr RPAREN','expr',3,'p_expr_parens','apl_project.py',81),
]
