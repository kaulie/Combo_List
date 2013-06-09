#-*- coding: utf8 -*-
'''
Created on 2013-5-2
分页获取混合列表中各个子列表
@author: gl
'''
import logging

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
    
    
    def _getTotal(self,listname):
        assert listname in self._list_names
        params = self._totalfn_param_dict[listname]
        list_total = self._totalfn_dict[listname](*params[0],**params[1])
        return list_total
    
    def _getList(self,listname,start,end):
        assert listname in self._list_names
        params = self._fetchfn_param_dict[listname]
        _sublist = self._fetchfn_dict[listname](start=start,end=end,*params[0],**params[1])
        return _sublist
            
    def join(self,pagenum,pagesize):
        '''
           获取列表总数和单页中各个子列表的组成，
           total,tuple(list1,list2,...listN) 
        '''
        self._check()
        
        _combolist = []
        #已经取到的记录个数
        fetch_count = 0 
        #列表的索引号
        _index = -1 
        #下一个集合要取的个数
        next_list_fetch_limit = pagesize
        #列表项总数
        total = 0
        for list_name in self._list_names :
            _index += 1
            #单个列表
            sub_total = self._getTotal(list_name)
            total += sub_total
            
            #列表start = item_count - 
            if total > (pagenum-1)*pagesize:
                if (_index == 0):
                    start,end = self._page_range(pagenum, pagesize)
                else:
                    offset = (pagenum-1)*pagesize-(total-sub_total)
                    start = max((offset,0))
                    end = start + next_list_fetch_limit
                    
                _sublist = self._getList(list_name,start,end) or []
                _combolist.append(_sublist)
                
                fetch_count += len(_sublist)
                if fetch_count >= next_list_fetch_limit:
                    break
                else:
                    next_list_fetch_limit = pagesize-fetch_count
            else:
                _combolist.append([])
        
        #补齐其余列表
        left_list_num = len(self._list_names)-_index-1
        for _ in xrange(left_list_num):
            _index += 1
            list_name = self._list_names[_index]
            total += self._getTotal(list_name)
            _combolist.append([])
                   
        return total,tuple(_combolist)
            
        
