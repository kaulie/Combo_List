Combo_List
==========

分页显示多个子列表构成的大的列表；


举例：


有N个列表 list1,list2,list3,...listN
get_listN_count 返回记录总条数；
get_listN_list 返回记录的对象列表；


初始化

def initialize():

    comboList = ComboList(['list1', 'list2', 'list3'])
    comboList.set_total_fn('list1', get_list1_count)
    comboList.set_total_fn('list1', get_list1_list)

    comboList.set_total_fn('list2', get_list2_count)
    comboList.set_total_fn('list2', get_list2_list)

    comboList.set_total_fn('list3', get_list3_count)
    comboList.set_total_fn('list3', get_list3_list)



def do_get(pagenum,pagesize):
    total,(lst_1,lst_2,lst_3) =  comboList.join(pagenum,pagesize)
    
    


调用:

initialize()
do_get(1,10)









