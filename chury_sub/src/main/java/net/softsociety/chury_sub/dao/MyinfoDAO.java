package net.softsociety.chury_sub.dao;

import net.softsociety.chury_sub.domain.Myinfo;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface MyinfoDAO {
    public Myinfo selectMyinfo(int id);
}
