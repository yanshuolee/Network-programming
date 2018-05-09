import java.net.*;
import java.util.*;

public class ip_query{
    public static void main(String[] args){
        try{
            Scanner scn = new Scanner(System.in);
            InetAddress client_add = InetAddress.getLocalHost();
            System.out.println(client_add);
            String ip_add = scn.next();
            InetAddress addr = InetAddress.getByName(ip_add);
            System.out.println(addr);
            scn.close();

        }catch(UnknownHostException e){
            System.out.println("Unable to connect");
        }
    }
}