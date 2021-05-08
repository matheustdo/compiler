from src.definitions.firsts import *

#<Program> follow = {$}
def follow_program():
    return {'$'}

#<Decls> follow = follow(<Program>)
def follow_decls():
    return follow_program()

#<Decl> follow = first(<Decls>) - {ε} U follow(<Decls>)
def follow_decl():
    return first_decls() | follow_decls()

#<Structs> follow = first(<Const Block>) - {ε} U first(<Var Block>) - {ε} U first(<Start Block>)
def follow_structs():
    return first_const_block() | first_var_block() | first_start_block()

#<Struct Block> follow = first(<Structs>) - {ε} U follow(<Structs>)
def follow_struct_block():
    return first_structs() | follow_structs()

#<Extends> follow = {{}
def follow_extends():
    return {'{'}

#<Const Block> follow = first(<Var Block>) - {ε} U first(<Start Block>) U {}}
def follow_const_block():
    return first_var_block() | first_start_block() | {'}'}

#<Var Block> follow = first(<Start Block>) U {}} U first(<Func Stms>) - {ε}
def follow_var_block():
    return first_start_block() | {'}'} | first_func_stms() 

#<Type> follow = {id} U first(<Var>) U first(<Const>) U follow(<Param Type>)
def follow_type():
    return {'id'} | first_var() | first_const() | follow_param_type()

#<Typedef> follow = follow(<Var Decl>) U follow(<Const Decl>)
def follow_typedef():
    return follow_var_decl() | follow_const_decl()

#<Var Decls> follow = {}}
def follow_var_decls():
    return {'}'}

#<Var Decl> follow = first(<Var Decls>) - {ε} U follow(<Var Decls>)
def follow_var_decl():
    return first_var_decls() | follow_var_decls()

#<Var Id> follow = follow(<Var Decl>)
def follow_var_id():
    return follow_var_decl()

#<Var> follow = first(<Var List>) - {ε} U {;} U follow(<Var List>)
def follow_var():
    return first_var_list() | {';'} | follow_var_list()

#<Var List> follow = {;}
def follow_var_list():
    return {';'}

#<Const Decls> follow = {}}
def follow_const_decls():
    return {'}'}

#<Const Decl> follow = first(<Const Decls>) - {ε} U follow(<Const Decls>)
def follow_const_decl():
    return first_const_decls() | follow_const_decls()

#<Const Id> follow = follow(<Const Decl>)
def follow_const_id():
    return follow_const_decl()

#<Const> follow = first(<Const List>)
def follow_const():
    return first_const_list()

#<Const List> follow = follow(<Const Decl>) U {;}
def follow_const_list():
    return follow_const_decl() | {';'}

#<Decl Atribute> follow = {;}
def follow_decl_atribute():
    return {';'}

#<Array Decl> follow = follow(<Decl Atribute>)
def follow_array_decl():
    return follow_decl_atribute()

#<Array Vector> follow = follow(<Array Decl>)
def follow_array_vector():
    return follow_array_decl()

#<Array Def> follow = {}}
def follow_array_def():
    return {'}'}

#<Array Expr> follow = follow(<Array Def>)
def follow_array_expr():
    return follow_array_def()

#<Array> follow = first(<Arrays>) - {ε} U follow(<Arrays>) U first(<Accesses>) - {ε} U first(<Assign>)
def follow_array():
    return first_arrays() | follow_arrays() | first_accesses() | first_assign()

#<Index> follow = {]}
def follow_index():
    return {']'}

#<Arrays> follow = follow(<Var>) U follow(<Const>) U follow(<Access>) U first(<Accesses>) - {ε} U first(<Assign>) U follow(<Id Value>)
def follow_arrays():
    return follow_var() | follow_const() | follow_access() | first_accesses() | first_assign() | follow_id_value()

#<Assign> follow = follow(<Stm Id>) U follow(<Stm Scope>)
def follow_assign():
    return follow_stm_id() | follow_stm_scope()

#<Access> follow = first(<Accesses>) - {ε} U follow(<Accesses>) U first(<Assign>) U follow(<Value>) U follow(<Log Value>)
def follow_access():
    return first_accesses() | follow_accesses() | first_assign() | follow_value() | follow_log_value()

#<Accesses> follow = first(<Assign>) U follow(<Id Value>)
def follow_accesses():
    return first_assign() | follow_id_value()

#<Args> follow = {)}
def follow_args():
    return {')'}

#<Args List> follow = follow(<Args>)
def follow_args_list():
    return follow_args()

#<Func Decl> follow = follow(<Decl>)
def follow_func_decl():
    return follow_decl()

#<Start Block> follow = first(<Decls>) - {ε} U follow(<Program>)
def follow_start_block():
    return first_decls() | follow_program()

#<Proc Decl> follow = follow(<Decl>)
def follow_proc_decl():
    return follow_decl()

#<Param Type> follow = {id}
def follow_param_type():
    return {'id'}

#<Params> follow = {)}
def follow_params():
    return {')'}

#<Param> follow = first(<Params List>) - {ε} U follow(<Params>) U follow(<Params List>)
def follow_param():
    return first_params_list() | follow_params() | follow_params_list()

#<Params List> follow = follow(<Params>)
def follow_params_list():
    return follow_params()

#<Param Arrays> follow = follow(<Param>)
def follow_param_Arrays():
    return follow_param()

#<Param Mult Arrays> follow = follow(<Param Arrays>)
def follow_param_mult_Arrays():
    return follow_param_Arrays()

#<Func Block> follow = follow(<Func Decl>) U follow(<Start Block>) U follow(<Proc Decl>)
def follow_func_block():
    return follow_func_decl() | follow_start_block() | follow_proc_decl()

#<Func Stms> follow = {}}
def follow_func_stms():
    return {'}'}

#<Func Stm> follow = first(<Func Stms>) - {ε} U follow(<Func Stms>) U first(<Else Stm>) - {ε} U first(<Func Stm>)
def follow_func_stm():
    return first_func_stms() | follow_func_stms() | first_else_stm() | first_func_stm()

#<Else Stm> follow = first(<Func Stm>)
def follow_else_stm():
    return first_func_stm()

#<Func Normal Stm> follow = follow(<Func Stm>)
def follow_func_normal_stm():
    return follow_func_stm()

#<Var Stm> follow = follow(<Func Normal Stm>)
def follow_var_stm():
    return follow_func_normal_stm()

#<Stm Id> follow = follow(<Var Id>) U follow(<Const Id>) U follow(<Var Stm>)
def follow_stm_id():
    return follow_var_id() | follow_const_id() | follow_var_stm()

#<Stm Scope> follow = follow(<Var Decl>) U follow(<Const Decl>) U follow(<Var Stm>)
def follow_stm_scope():
    return follow_var_decl() | follow_const_decl() | follow_var_stm()

#<Stm Cmd> follow = follow(<Var Stm>)
def follow_stm_cmd():
    return follow_var_stm()

#<Expr> follow = follow(<Decl Atribute>) U first(<Array Expr>) - {ε} U follow(<Array Def>) U follow(<Index>) U first(<Args List>) - {ε} U follow(<Args>) U follow(<Args List>) U {;, )}
def follow_expr():
    return follow_decl_atribute() | first_array_expr() | follow_array_def() | follow_index() | first_args_list() | follow_args() | follow_args_list() | {';', ')'}

#<Or> follow = follow(<Expr>)
def follow_or():
    return follow_expr()

#<Or_> follow = follow(<Or>)
def follow_or_():
    return follow_or()

#<And> follow = first(<Or_>) - {ε} U follow(<Or_>) U follow(<Or>)
def follow_and():
    return first_or_() | follow_or_() | follow_or()

#<And_> follow = follow(<And>)
def follow_and_():
    return follow_and()

#<Equate> follow = first(<And_>) - {ε} U follow(<And_>) U follow(<And>)
def follow_equate():
    return first_and_() | follow_and_() | follow_and()

#<Equate_> follow = follow(<Equate>)
def follow_equate_():
    return follow_equate()

#<Compare> follow = first(<Equate_>) - {ε} U follow(<Equate_>) U follow(<Equate>)
def follow_compare():
    return first_equate_() | follow_equate_() | follow_equate()

#<Compare_> follow = follow(<Compare>)
def follow_compare_():
    return follow_compare()

#<Add> follow = first(<Compare_>) - {ε} U follow(<Compare_>) U follow(<Compare>)
def follow_add():
    return first_compare_() | follow_compare_() | follow_compare()

#<Add_> follow = follow(<Add>)
def follow_add_():
    return follow_add()

#<Mult> follow = first(<Add_>) - {ε} U follow(<Add_>) U follow(<Add>)
def follow_mult():
    return first_add_() | follow_add_() | follow_add()

#<Mult_> follow = follow(<Mult>)
def follow_mult_():
    return follow_mult()

#<Unary> follow = first(<Mult_>) - {ε} U follow(<Mult_>) U follow(<Mult>)
def follow_unary():
    return first_mult_() | follow_mult_() | follow_mult()

#<Value> follow = follow(<Unary>)
def follow_value():
    return follow_unary()

#<Id Value> follow = follow(<Value>) U follow(<Log Value>)
def follow_id_value():
    return follow_value() | follow_log_value()

#<Log Expr> follow = {)}
def follow_log_expr():
    return {')'}

#<Log Or> follow = follow(<Log Expr>)
def follow_log_or():
    return follow_log_expr()

#<Log Or_> follow = follow(<Log Or>)
def follow_log_or_():
    return follow_log_or()

#<Log And> follow = first(<Log Or_>) - {ε} U follow(<Log Or_>) U follow(<Log Or>)
def follow_log_and():
    return first_log_or_() | follow_log_or_() | follow_log_or()

#<Log And_> follow = follow(<Log And>)
def follow_log_and_():
    return follow_log_and()

#<Log Equate> follow = first(<Log And_) - {ε} U follow(<Log And_>) U follow(<Log And>)
def follow_log_equate():
    return first_log_and_() | follow_log_and_() | follow_log_and()

#<Log Equate_> follow = follow(<Log Equate>)
def follow_log_equate_():
    return follow_log_equate()

#<Log Compare> follow = first(<Log Equate_>) - {ε} U follow(<Log Equate_>) U follow(<Log Equate>)
def follow_log_compare():
    return first_log_equate_() | follow_log_equate_() | follow_log_equate()

#<Log Compare_> follow = follow(<Log Compare>)
def follow_log_compare_():
    return follow_log_compare()

#<Log Unary> follow = first(<Log Compare_>) - {ε} U follow(<Log Compare_>) U follow(<Log Compare_>)
def follow_log_unary():
    return first_log_compare_() | follow_log_compare_() | follow_log_compare()

#<Log Value> follow = follow(<Log Unary>)
def follow_log_value():
    return follow_log_unary()
