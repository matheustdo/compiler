'''
This file contains the firsts of language grammar.
'''
    
# <Program> first = first(<Structs>) U first(<Const Block>) U first(<Var Block>) U first(<Start Block>)
def first_program():
    return first_structs() | first_const_block() | first_var_block() | first_start_block() 

# <Decls> first = first(<Decl>)
def first_decls():
    return first_decl()

# <Decl> first = first(<Func Decl>) U first(<Proc Decl>)
def first_decl():
    return first_func_decl() | first_proc_decl()

# <Structs> first = first(<Struct Block>) 
def first_structs():
    return first_struct_block()

# <Struct Block>	first = {struct}
def first_struct_block():
    return {'struct'}

# <Extends> first = {extends}
def first_extends():
    return {'extends'} 

# <Const Block> first = {const}
def first_const_block():
    return {'const'}

# <Var Block> first = {var}
def first_var_block():
    return {'var'}

# <Type> first = {int, real, boolean, string, struct}
def first_type():
    return {'int', 'real', 'boolean', 'string', 'struct'}

# <Typedef> first = {typedef}
def first_typedef():
    return {'typedef'}

# <Var Decls> first = first(<Var Decl>)
def first_var_decls():
    return first_var_decl()

# <Var Decl> first = first(<Type>) U first(<Typedef>) U first(<Stm Scope>) U {id}
def first_var_decl():
    return first_type() | first_typedef() | first_stm_scope() | {'id'}

# <Var Id> first = first(<Var>) U first(<Stm Id>)
def first_var_id():
    return first_var() | first_stm_id()

# <Var> first = {id}
def first_var():
    return {'id'}

# <Var List> first = {,}
def first_var_list():
    return {','}

# <Const Decls> first = first(<Const Decl>)
def first_const_decls():
    return first_const_decl()

# <Const Decl> first = first(<Type>) U first(<Typedef>) U first(<Stm Scope>) U {id}
def first_const_decl():
    return first_type() | first_typedef() | first_stm_scope() | {'id'}

# <Const Id> first = first(<Const>) U first(<Stm Id>)
def first_const_id():
    return first_const() | first_stm_id()

# <Const> first = {id}
def first_const():
    return {'id'}

# <Const List> first = {,, =}
def first_const_list():
    return {',', '='}

# <Decl Atribute> first = first(<Array Decl>) U first(<Expr>)
def first_decl_atribute():
    return first_array_decl() | first_expr()

# <Array Decl> first = {'{'}
def first_array_decl():
    return {'{'}

# <Array Vector> first = {','}
def first_array_vector():
    return {','}

# <Array Def> first = first(<Expr>)
def first_array_def():
    return first_expr()

# <Array Expr> first = {','}
def first_array_expr():
    return {','}

# <Array> first = {[}
def first_array():
    return {'['}

# <Index> first = first<Expr>
def first_index():
    return first_expr()

# <Arrays> first = first(<Array>)
def first_arrays():
    return first_array()

# <Assign> first = {=, ++, --}
def first_assign():
    return {'=', '++', '--'}

# <Access> first = {.}
def first_access():
    return {'.'}

# <Accesses> first = first(<Access>)
def first_accesses():
    return first_access()

# <Args> first = first(<Expr>)
def first_args():
    return first_expr()

# <Args List> first = {,}
def first_args_list():
    return {','}

# <Func Decl> first = {function}
def first_func_decl():
    return {'function'}

# <Start Block> first = {procedure}
def first_start_block():
    return {'procedure'}

# <Proc Decl> first = {procedure}
def first_proc_decl():
    return {'procedure'}

# <Param Type> first = first(<Type>) U {id}
def first_param_type():
    return first_type() | {'id'}

# <Params> first = first(<Param>)
def first_params():
    return first_param()

# <Param> first = first(<Param Type>)
def first_param():
    return first_param_type()

# <Params List> first = {,}
def first_params_list():
    return {','}

# <Param Arrays> first = {[}
def first_param_arrays():
    return {'['}

# <Param Mult Arrays> first = {[}
def first_param_mult_arrays():
    return {'['}

# <Func Block> first = {{}
def first_func_block():
    return {'{'}

# <Func Stms> first = first(<Func Stm>)
def first_func_stms():
    return first_func_stm()

# <Func Stm> first = {if, while} U first(<Func Normal Stm>)
def first_func_stm():
    return {'if', 'while'} | first_func_normal_stm()

# <Else Stm> first = {else}
def first_else_stm():
    return {'else'}

# <Func Normal Stm> first = {{, ;, return} U first(<Var Stm>)
def first_func_normal_stm():
    return {'{', ';', 'return'} | first_var_stm()

# <Var Stm> first = first(<Stm Scope>) U {id} U first(<Stm Cmd>)
def first_var_stm():
    return first_stm_scope() | {'id'} | first_stm_cmd()

# <Stm Id> first = first(<Assign>) U first(<Array>) U first(<Access>) U {(}
def first_stm_id():
    return first_assign() | first_array() | first_access() | {'('}

# <Stm Scope> first = {local, global}
def first_stm_scope():
    return {'local', 'global'}

# <Stm Cmd> first = {print, read}
def first_stm_cmd():
    return {'print', 'read'}

# <Expr> first = first(<Or>)
def first_expr():
    return first_or()

# <Or> first = first(<And>)
def first_or():
    return first_and()

# <Or_> first = {||}
def first_or_():
    return {'||'}

# <And> first = first(<Equate>)
def first_and():
    return first_equate()

# <And_> first = {&&}
def first_and_():
    return {'&&'}

# <Equate> first = first(<Compare>)
def first_equate():
    return first_compare()

# <Equate_> first = {==, =}
def first_equate_():
    return {'==', '!='}

# <Compare> first = first(<Add>)
def first_compare():
    return first_add()

# <Compare_> first = {<, >, <=, >=}
def first_compare_():
    return {'<', '>', '<=', '>='}

# <Add> first = first(<Mult>)
def first_add():
    return first_mult()

# <Add_> first = {+, -}
def first_add_():
    return {'+', '-'}

# <Mult> first = first(<Unary>)
def first_mult():
    return first_unary()

# <Mult_> first = {*, /}
def first_mult_():
    return {'*', '/'}

# <Unary> first = {!} U first(<Value>)
def first_unary():
    return {'!'} | first_value()

# <Value> first = {num, str, true, false, local, global, id, (}
def first_value():
    return {'num', 'str', 'true', 'false', 'local', 'global', 'id', '('}

# <Id Value> first = {(} U first(<Arrays>) U first(<Accesses>)
def first_id_value():
    return {'('} | first_arrays() | first_accesses()

# <Log Expr> first = first(<Log Or>)
def first_log_expr():
    return first_log_or()

# <Log Or> first = first(<Log And>)
def first_log_or():
    return first_log_and()

# <Log Or_> first = {||}
def first_log_or_():
    return {'||'}

# <Log And> first = first(<Log Equate>)
def first_log_and():
    return first_log_equate()

# <Log And_> first = {&&}
def first_log_and_():
    return {'&&'}

# <Log Equate> first = first(<Log Compare>)
def first_log_equate():
    return first_log_compare()

# <Log Equate_> first = {==, =}
def first_log_equate_():
    return {'==', '!='}

# <Log Compare> first = first(<Log Unary>)
def first_log_compare():
    return first_log_unary()

# <Log Compare_> first = {<, >, <=, >=}
def first_log_compare_():
    return {'<', '>', '<=', '>='}

# <Log Unary> first = {!} U first(<Log Value>)
def first_log_unary():
    return {'!'} | first_log_value()

# <Log Value> first = {num, str, true, false, local, global, id, (}
def first_log_value():
    return {'num', 'str', 'true', 'false', 'local', 'global', 'id', '('}

