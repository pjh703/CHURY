package net.softsociety.chury_sub.service;

import net.softsociety.chury_sub.dao.MyinfoDAO;
import net.softsociety.chury_sub.domain.Myinfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class MyinfoServiceImpl implements MyinfoService{
    @Autowired
    MyinfoDAO myinfodao;

    @Override
    public Myinfo read(int id) {
        Myinfo result = myinfodao.selectMyinfo(id);
        return result;
    }
}
