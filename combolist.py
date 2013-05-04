#-*- coding: utf8 -*-
'''
Created on 2013-5-2
分页获取混合列表中各个子列表
@author: gl
'''

class ComboList():
    
    def __init__(self,*list_names):
        #列表的列表，列表中各个列表的顺序代表了分页中出现的先后顺序
        assert len(list_names) >= 1
        self._list_names = list_names
        self._totalfn_dict = dict()
        self._fetchfn_dict = dict()
        self._totalfn_param_dict = dict()
        self._fetchfn_param_dict = dict()
        
    def set_total_fn(self,list_name,total_fn,*args,**kwargs):
        self._totalfn_dict[list_name] = total_fn
        self._totalfn_param_dict[list_name] = (args,kwargs)
        
    def set_fetch_fn(self,list_name,fetch_fn,*args,**kwargs):
        self._fetchfn_dict[list_name] = fetch_fn
        self._fetchfn_param_dict[list_name] = (args,kwargs)
    
    def _check(self):
        for t in self._list_names:
            if self._totalfn_dict[t] == None or self._fetchfn_dict[t] == None :
                raise Exception(u'必须提供相应的函数')
            
    def _page_range(self,page=1,count=20):
        if not page:
            page =1 
        start = (int(page)-1)*count
        return start, start + count
 
            
    def join(self,pagenum,pagesize):
        '''
           获取某页中各个子列表的组成，返回tuple(list1,list2,...listN) 
        '''
        self._check()
        assert isinstance(pagenum,int)
        assert isinstance(pagesize,int)
        
        _combolist = []
        #已经取到的记录个数
        fetch_count = 0 
        #列表的索引号
        list_index = -1 
        #下一个集合要取的个数
        next_list_fetch_limit = pagesize
        #列表项总数
        item_count = 0
        for list_name in self._list_names :
            list_index += 1
            t_params = self._fetchfn_param_dict[list_name]
            item_count += self._totalfn_dict[list_name](*t_params[0],**t_params[1])
            if item_count > (pagenum-1)*pagesize:
                if (list_index == 0):
                    start,end = self._page_range(pagenum, pagesize)
                else:
                    start,end = 0,next_list_fetch_limit
                params = self._fetchfn_param_dict[list_name]
                _sublist = self._fetchfn_dict[list_name](start=start,end=end,*params[0],**params[1]) or []
                _combolist.append(_sublist)
                fetch_count += len(_sublist)
                if fetch_count >= next_list_fetch_limit:
                    break
                else:
                    next_list_fetch_limit = pagesize-fetch_count
            else:
                _combolist.append([])
        
        for _ in xrange(len(self._list_names)-list_index-1):
            _combolist.append([])       
        return tuple(_combolist)
            
        

        
def test():        
    def get_total():
        return 10

    def fetch(start=0,end=10,type=6):
        print '======type======',type
        a = [1,2,3,4,5,6,7,8,9,10]
        return a[start:end] 
    list = ['aaa','bbb','ccc']
    maxed_list = ComboList(*list)
    maxed_list.set_total_fn('aaa', get_total)
    maxed_list.set_fetch_fn('aaa', fetch,6)
    maxed_list.set_total_fn('bbb', get_total)
    maxed_list.set_fetch_fn('bbb', fetch)
    maxed_list.set_total_fn('ccc', get_total)
    maxed_list.set_fetch_fn('ccc', fetch)
    print maxed_list.join(1, 14)

if __name__ == '__main__':
    test()