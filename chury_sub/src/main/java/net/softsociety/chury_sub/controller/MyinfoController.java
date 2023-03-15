package net.softsociety.chury_sub.controller;

import lombok.extern.slf4j.Slf4j;
import net.softsociety.chury_sub.domain.Myinfo;
import net.softsociety.chury_sub.service.MyinfoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
@Slf4j
public class MyinfoController {
    @Autowired
    MyinfoService myinfoService;

    @GetMapping({"/", ""})
    public String index(int id, Model model) {
        Myinfo result = myinfoService.read(id);

        model.addAttribute("myinfo", result);
        return "myinfoView";
    }

}
