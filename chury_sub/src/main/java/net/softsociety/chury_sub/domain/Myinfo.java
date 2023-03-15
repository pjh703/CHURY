package net.softsociety.chury_sub.domain;

import lombok.*;

@AllArgsConstructor
@NoArgsConstructor
@Getter @Setter
@ToString
public class Myinfo {
    private int id;
    private String username;
    private String date_joined;
    private String email;
    private int email_confirm;
    private int regist;
    private String reg_date;
    private int bookcnt;
}
